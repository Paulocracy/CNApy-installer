# CNApy installers creator

## Introduction

This is the automatic creator for CNApy's Windows installer as well as Linux and MacOS X installation assistant scripts.

## Development instructions for the installer (only needed for developers of the installer itself)

This installer uses tkinter as GUI toolkit and Python as programming lanugage.

In order to develop with cnapy-installer, create and activate its associated conda environment and pip install a package which cannot be found in conda-forge:

```sh
conda env create -n cnapy-installer -f environment.yml
conda activate cnapy-installer
```

In order to create the installers, run cnapy-installers-creator.py in the new cnapy-instller Anaconda environment which will lead you through the process.

To update the installer creator to CNApy's newest version, change the variable in "cnapy-installers-creator.py" to the current version.
