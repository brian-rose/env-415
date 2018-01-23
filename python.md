---
layout: page
title: Python
permalink: /python/
---
## About Python

In this course we will be working extensively with a computer programming language called Python.

Python is a general-purpose high-level interpreted language that is now being used by many people in the geosciences. Benefits of Python include:

- It's easy to learn.
- The code tends to be simple and easy to read.
- It can run on just about any computer, maybe even your smartphone.
- You can run your code interactively, so it's great for exploring and learning about your data.
- Lots of packages are available for powerful scientific computing and graphics.
- It's completely free and open-source.


## Anaconda Python

To get started, you need to install Python on your computer. We are going to use a program called **Anaconda**. Anaconda is a complete scientific Python environment including Python itself, a handy editor for reading and writing code, an interactive "shell" where you can run your code, and access to all the scientific Python libraries we will need.

To download and install Anaconda, [go to this page](https://www.continuum.io/downloads). Installers and instructions are available for Windows, Mac and Linux. **IMPORTANT**: You will see the option to install either Python 2.7 or Python 3.6. **Choose Python 3.6**. *This is the latest version*


## Using the JupyterHub

As an alternative to running everything on your own laptop, it will be possible to run Python code on a central server called a `JupyterHub`. This system allows you to log in through a web browser and run [Jupyter notebooks](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) on the server.

To log in to the JupyterHub: https://lore.atmos.albany.edu:8000

You will need your regular UAlbany credentials.

### Getting notebook files onto your JupyterHub space

When you log in to the JupyterHub you will see a file browser showing the contents of your `home` directory on the departmental linux space. You should see a folder called `0notebooks` at the top of the list. Click on this. Inside `0notebooks` you should find a class folder called `ENV415`. This is where you should save notebook files for this course.

Sometimes you will be creating your own notebook files. However for in-class work the instructor will often distribute pre-made notebooks with some sample code or instructions. These files will be available on the [handouts page](({{ site.baseurl }}/handouts)).

To upload these files to your JupyterHub space:

- Right-click on the file to download and save the file locally on your laptop. *Make sure it is saved as a *.ipynb file*. Some browsers might try to change the file extension.
- *I recommend using Firefox for this -- some other browsers are causing problems with unwanted extra file extensions.*
- Log into the JupyterHub and navigate to your `ENV415` folder.
- Click the `Upload` button on the JupyterHub page.
- Browse for your locallly saved notebook file
- The file will now appear at the top of the JupyterHub browser.
- Click the blue `Upload` button to confirm.
- The file is now saved on your JuptyerHub space.
- Click on the notebook file to launch the notebook server and begin working.

###  Saving your work on the JupyterHub

When you are finished working on a notebook file:

- Choose `Save and Checkpoint` from the `File` menu on the JupyterHub. This will create a backup or checkpoint that you can revert back to if you mess something up later.
- From the same menu, choose `Close and Halt`. This will kill the Python kernel and avoid clogging up the JupyterHub with stale processes.
- Close your browser window and you're done.


## Python resources

Here are some links to useful Python-related resources.

- [A Hands-On Introduction to Using Python in the Atmospheric and Oceanic Sciences](http://www.johnny-lin.com/pyintro/), by Johnny Wei-Bing Lin. *A very nice short course in Python written specifically for students and researchers in Atmospheric and Oceanic Sciences.
The entire book is available as free pdf downloads from the website (the author requests donations, and a print version is also for sale).*
- [Principles of Planetary Climate](http://geosci.uchicago.edu/~rtp1/PrinciplesPlanetaryClimate/), by Raymond T. Pierrehumbert. *The website companion to a comprehensive textbook on climate physics. A lot of climate-related python code can be found here under "Courseware".*
- [Learn Python the Hard Way](http://learnpythonthehardway.org), by Zed A. Shaw. *A great introduction to Python for beginners with little or no programming experience. Not specific to atmospheric science. [This introductory note](http://learnpythonthehardway.org/book/intro.html) spells out the importance of trial and error, and avoiding the temptation to copy and paste code (which tends to teach you very little).*

## Learning Python the Hard Way
I happen to think that learning any kind of programming is best done by trial and error, and I will structure the assignments accordingly. [The advice on this page](http://learnpythonthehardway.org/book/intro.html) sums up my feelings quite well: "The Hard Way is Easier"
