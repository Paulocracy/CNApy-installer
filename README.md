# CNApy-installer

## Introduction

This is the Windows .exe installer for [CNApy](https://github.com/cnapy-org/CNApy) since CNApy version 1.0.9. You can find the installer for each CNApy version in [CNApy's release assets](https://github.com/cnapy-org/CNApy/releases).

## Development instructions (only needed for developers of the installer itself)

This installer uses tkinter as GUI toolkit and Python as programming lanugage.

In order to develop with cnapy-installer, create and activate its associated conda environment:

```sh
conda env create -n cnapy-installer -f environment.yml
conda activate cnapy-installer
```

In order to create an .exe file out of this installer's script cnapy-installer.py, run
the following command within cnapy-installer's conda environment:

```sh
pyinstaller cnapy-installer.py --onefile --noconsole -i app.ico
```

Now, you can find the cnapy-installer.exe under the subfolder "./dist".
