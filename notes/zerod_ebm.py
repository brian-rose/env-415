'''
Some code to implement the zero-dimensional Energy Balance Model
introduced at the beginning of ENV 415
using the Python modeling package climlab

See <http://climlab.readthedocs.io/en/latest/>

Usage:
```
from zerod_ebm import ZeroD_EBM
# create a model instance with default parameters
ebm = ZeroD_EBM()
#  examing the model object:
print(ebm)
#  Take a single timestep forward
ebm.step_forward
#  Look at all the diagnostics computed by the model
ebm.diagnostics
#  integrate out to quasi-equilibrium
ebm.integrate_years(20)
#  Check for energy balance
print(ebm.ASR - ebm.OLR)
```

Brian E. J. Rose
University at Albany
'''
import climlab

class ShortwaveEBM(climlab.process.EnergyBudget):
    '''A class for the shortwave radiation process in the EBM.
    Contains the insolation and albedo subprocesses, and computes the ASR from
    insolation * (1-albedo).'''
    def __init__(self, Q=341., albedo=0.3, **kwargs):
        super(ShortwaveEBM, self).__init__(**kwargs)
        self.param['Q'] = Q
        self.param['albedo'] = albedo
        #  insolation subprocess
        dom = self.Ts.domain
        ins = climlab.radiation.FixedInsolation(domains=dom, S0=self.param['Q'])
        self.add_subprocess('insolation', ins)
        #  albedo subprocess
        alb = climlab.surface.ConstantAlbedo(state=self.state, albedo=self.param['albedo'])
        self.add_subprocess('albedo', alb)
        #  Define a diagnostic quantity called ASR
        self.add_diagnostic('ASR', 0.*self.Ts)
        #  Flag to compute subprocesses first each timestep
        self.topdown = False
    def _compute_heating_rates(self):
        '''This function will get called every timestep and compute current SW heating in W/m2.'''
        self.ASR = (1.-self.subprocess['albedo'].albedo)*self.subprocess['insolation'].insolation
        self.heating_rate['Ts'] = self.ASR


class ZeroD_EBM(climlab.TimeDependentProcess):
    '''A class for the zero-dimensional energy balance model as defined in ENV 415 lecture notes.

    Input parameters:
    - water_depth: depth of the slab ocean in meters (default = 50.)
    - Q: global mean insolation in W/m**2 (default = 341.)
    - albedo: global mean albedo, dimensionless (default = 0.3)
    - tau: atmospheric longwave transmissivity, dimensionless (default = 0.612)
    '''
    def __init__(self,
                 water_depth = 100,
                 Q = 341.,
                 albedo = 0.3,
                 tau = 0.612,
                 **kwargs):
        if 'state' not in kwargs:
            state = climlab.surface_state(num_lat=1, water_depth=water_depth)
            sfc = state.Ts.domain
            kwargs.update({'state': state, 'domains':{'sfc':sfc}})
        super(ZeroD_EBM, self).__init__(**kwargs)
        self.param['Q'] = Q
        self.param['S0'] = Q
        self.param['tau'] = tau
        self.param['albedo'] = albedo
        self.param['eps'] = 1.
        self.param['water_depth'] = water_depth
        olr = climlab.radiation.Boltzmann(state=self.state, **self.param)
        asr = ShortwaveEBM(state=self.state, **self.param)
        self.add_subprocess('OLR', olr)
        self.add_subprocess('ASR', asr)
