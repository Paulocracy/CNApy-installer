# CNApy-installer

## Introduction

This is the Windows .exe installer for [CNApy](https://github.com/cnapy-org/CNApy) since CNApy version 1.0.9. You can find the installer for each CNApy version in [CNApy's release assets](https://github.com/cnapy-org/CNApy/releases).

## Development instructions for the installer (only needed for developers of the installer itself)

This installer uses tkinter as GUI toolkit and Python as programming lanugage.

In order to develop with cnapy-installer, create and activate its associated conda environment and pip install a package which cannot be found in conda-forge:

```sh
conda env create -n cnapy-installer -f environment.yml
conda activate cnapy-installer
pip install elevate
```

In order to create an .exe file out of this installer's script cnapy-installer.py, run
the following command within cnapy-installer's conda environment:

```sh
pyinstaller cnapy-installer.py --onefile --noconsole -i app.ico
```

Now, you can find the cnapy-installer.exe under the subfolder "./dist".

## Development instructions for the uninstaller (only needed for developers of the uninstaller itself)

The uninstaller, which is added to the CNApy folder at the end of the installation process and is created such that the user is directly asked for elevated user rights, can be created in its .exe form as follows:

```sh
pyinstaller cnapy-uninstaller.py --onefile --noconsole -i app.ico
```
