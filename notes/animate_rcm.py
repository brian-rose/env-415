import numpy as np
from matplotlib import pyplot, animation
import xarray as xr
import climlab


def get_tendencies(model):
    '''Pack all the subprocess tendencies into xarray.Datasets
    and convert to units of K / day'''
    tendencies_atm = xr.Dataset()
    tendencies_sfc = xr.Dataset()
    for name, proc, top_proc in climlab.utils.walk.walk_processes(model, topdown=False):
        if proc.time_type is not 'diagnostic':
            tendencies_atm[name] = proc.tendencies['Tatm'].to_xarray()
            tendencies_sfc[name] = proc.tendencies['Ts'].to_xarray()
    for tend in [tendencies_atm, tendencies_sfc]:
        #  convert to K / day
        tend *= climlab.constants.seconds_per_day
    return tendencies_atm, tendencies_sfc

yticks = np.array([1000., 750., 500., 250., 100., 50., 20., 10., 5.])

#  We will plot temperatures with respect to log(pressure) to get a height-like coordinate
def zstar(lev):
    return -np.log(lev / climlab.constants.ps)

def setup_figure():
    fig, axes = pyplot.subplots(1,2,figsize=(12,4))
    axes[1].set_xlabel('Temperature tendency (K/day)', fontsize=14)
    axes[1].set_xlim(-6,6)
    axes[0].set_xlim(190,320)
    axes[0].set_xlabel('Temperature (K)', fontsize=14)
    for ax in axes:
        ax.set_yticks(zstar(yticks))
        ax.set_yticklabels(yticks)
        ax.set_ylabel('Pressure (hPa)', fontsize=14)
        ax.grid()
    twinax = axes[0].twiny()
    twinax.set_xlim(0,15)
    twinax.set_title('Specific humidity (g/kg)')
    axes = np.append(axes, twinax)
    fig.suptitle('Radiative-Convective Model with RRTMG radiation and Emanuel moist convection', fontsize=14)
    return fig, axes

def init_figure():
    lines = []
    lines.append(axes[0].plot(model.Tatm, zstar(model.lev), color='red', animated=True)[0])
    lines.append(axes[0].plot(model.Ts, 0, 'o', markersize=8, color='red', animated=True)[0])
    lines.append(axes[2].plot(model.q*1000, zstar(model.lev), color='blue', animated=True)[0])

    ax = axes[1]
    color_cycle=['g','b','r','y','k','c','m','orange']
    tendencies_atm, tendencies_sfc = get_tendencies(model)
    num_tendencies = 0
    for i, name in enumerate(tendencies_atm.data_vars):
        lines.append(ax.plot(tendencies_atm[name], zstar(model.lev), label=name, color=color_cycle[i])[0])
        num_tendencies += 1
    for i, name in enumerate(tendencies_sfc.data_vars):
        lines.append(ax.plot(tendencies_sfc[name], 0, 'o', markersize=8, color=color_cycle[i])[0])
    ax.legend(loc='center right');
    lines.append(axes[0].text(250, zstar(100.), 'Day {}'.format(int(model.time['days_elapsed']))))
    return lines, num_tendencies

def update_frame():
    lines[0].set_xdata(np.array(model.Tatm))
    lines[1].set_xdata(np.array(model.Ts))
    lines[2].set_xdata(np.array(model.q)*1E3)
    tendencies_atm, tendencies_sfc = get_tendencies(model)
    for i, name in enumerate(tendencies_atm.data_vars):
        lines[3+i].set_xdata(tendencies_atm[name])
    for i, name in enumerate(tendencies_sfc.data_vars):
        lines[3+num_tendencies+i].set_xdata(tendencies_sfc[name])

    lines[-1].set_text('Day {}'.format(int(model.time['days_elapsed'])))

def advance_simulation(step):
    for n in range(steps_per_frame):
        model.step_forward()
    update_frame()
    return lines

def build_rcm(num_lev=30, water_depth=2.5):
    # Temperatures in a single column
    state = climlab.column_state(num_lev=num_lev, water_depth=water_depth)
    #  Initialize a nearly dry column (small background stratospheric humidity)
    state['q'] = np.ones_like(state.Tatm) * 5.E-6
    #  ASYNCHRONOUS COUPLING -- the radiation uses a much longer timestep
    short_timestep = climlab.constants.seconds_per_hour
    #  Radiation coupled to water vapor
    rad = climlab.radiation.RRTMG(name='Radiation',
                        state=state,
                        specific_humidity=state.q,
                        albedo=0.2,
                        timestep=24*short_timestep)
    #  Convection scheme -- water vapor is a state variable
    conv = climlab.convection.EmanuelConvection(name='Convection',
                                  state=state,
                                  timestep=short_timestep,
                                  ALPHA=0.1,)
    #  Surface heat flux processes
    shf = climlab.surface.SensibleHeatFlux(name='SHF',
                                  state=state, Cd=0.5E-3, U=10.,
                                  timestep=short_timestep)
    lhf = climlab.surface.LatentHeatFlux(name='LHF',
                                  state=state, Cd=0.5E-3, U=10.,
                                  timestep=short_timestep)
    #  Couple all the submodels together
    turb = climlab.couple([shf,lhf], name='Turbulent')
    model = climlab.couple([rad, conv, turb], name='RadiativeConvectiveModel')
    for proc in [rad, conv, shf, lhf]:
        model.add_subprocess(proc.name, proc)
    return model

model = build_rcm()
model.step_forward()
print(model)
num_prognostic = 0
for name, proc, top_proc in climlab.utils.walk.walk_processes(model, topdown=False):
    if proc.time_type is not 'diagnostic':
        num_prognostic += 1

fig, axes = setup_figure()
lines, num_tendencies = init_figure()
steps_per_frame = 48
model_run = animation.FuncAnimation(fig, advance_simulation, blit=True)
pyplot.show()
