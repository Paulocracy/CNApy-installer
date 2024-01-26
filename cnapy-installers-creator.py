import subprocess
import os
import sys
import urllib.request
from tkinter import messagebox
from tkinter import filedialog
from zipfile import ZipFile, ZIP_LZMA

# If you just want to update the CNApy version, you just have to edit the following string
# and run the CNApy installers creator:
CNAPY_VERSION = "1.1.10"
# Here, select your wished Miniconda installer .exe
MINICONDA_EXE_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

# Start the actual GUI program
answer = messagebox.askyesno(
    "Welcome to the CNApy installers creator!",
    f"This program will create the installers for CNApy version {CNAPY_VERSION}.\n"
    "Do you want to proceed?"
)
if not answer:
    sys.exit(0)

messagebox.showinfo(
    "Choose the CNApy installers folder",
    "In the next step, choose an folder (e.g., a newly created folder) on your computer "
    "where you want the CNApy installers to be created."
)

selected_folder = filedialog.askdirectory(
    title="Choose CNApy installation folder",
    initialdir="C:\\Program Files",
)
selected_folder = selected_folder.replace("/", "\\")
if not selected_folder.endswith("\\"):
    selected_folder += "\\"

if (selected_folder == "") or (not os.path.isdir(selected_folder)):
    messagebox.showerror(
        "No valid folder selected",
        "It appears that you didn't select a valid installation folder.\n"
        "Please try the CNApy installers installation process again in a different folder "
        "and without clicking on 'Cancel'."
    )
    sys.exit(0)
if len(os.listdir(selected_folder)) > 0:
    new_folder_name = "CNApy_Installers"
    if os.path.exists(f"{selected_folder}{new_folder_name}"):
        counter = 2
        while os.path.exists(f"{selected_folder}{new_folder_name}"):
            new_folder_name = f"CNApy_Installers{counter}"
            counter += 1
    selected_folder += new_folder_name + "\\"

    answer = messagebox.askyesno(
        "Confirm folder for CNApy installers",
        "Your selected folder is not empty. Since the CNApy installers need to be installed in an empty folder,"
        f"the new empty subfolder {selected_folder} will be created and, therefore, the installers will be "
        "installed in the following full folder path:\n"
        f"{selected_folder}\n"
        f"Are you ok with this procedure?"
    )
    if not answer:
        messagebox.showerror(
            "Error in folder selection",
            "Please retry the installation with a different folder."
        )
        sys.exit(0)
    try:
        os.mkdir(selected_folder)
    except Exception:
        messagebox.showerror(
            "Error with folder creation",
            "The new empty folder could not be created. Please make sure that you are allowed to have "
            "access to your provided installation folder. E.g., this might be the case in the folder 'Programs' or 'Program Files'. "
            "If this error persists, please retry the installation "
            "in a different folder, e.g. in a new empty folder that you created."
        )
        sys.exit(0)

answer = messagebox.askyesno(
    "Choosing folder successful",
    "Now, the installers are going to be installed. This may take a while.\n"
    "Please be patient until a new message appears.\n"
    "Do you want to proceed with the CNApy installers creation?"
)
if not answer:
    sys.exit(0)

miniconda_exe_name = "miniconda.exe"
miniconda_exe_path = f"{selected_folder}{miniconda_exe_name}"
try:
    urllib.request.urlretrieve(MINICONDA_EXE_URL, miniconda_exe_path)
except Exception:
    messagebox.showerror(
        "Error while downloading",
        "An error occurred in a download process of the installation.\n"
        "Please make sure that your internet connection works and retry the installation."
    )
    sys.exit(0)

miniconda_install_path = f"{selected_folder}\\CNApy\\miniconda\\"
if os.path.exists(miniconda_install_path):
    messagebox.showerror(
        "The installers seem to be already downloaded in this folder",
        "It looks like the installers were already downloaded in the given folder.\n"
        "Please install the installers in a new folder.\n"
    )
    sys.exit(0)

# As per https://stackoverflow.com/questions/39984611/
miniconda_command =  f'cd "{selected_folder}" && {miniconda_exe_name} /S /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /NoRegistry=1 /D={miniconda_install_path}'

try:
    has_run_error = subprocess.check_call(
        miniconda_command,
        shell=True
    )  # The " are introduces in order to handle paths with blank spaces
except subprocess.CalledProcessError:
    has_run_error = True
if has_run_error:
    messagebox.showerror(
        "Error while running installation process",
        "Error during the execution of the installation process.\n"
        "Please make sure that you have full access permissions on the selected "
        "installation folder."
    )
    sys.exit(0)

conda_path = f"{miniconda_install_path}\\condabin\\conda"
clean_command = f'"{conda_path} clean -a --yes'

os.system(clean_command)
os.remove(miniconda_exe_path)

with open(f"{selected_folder}\\CNApy\\INSTALL_CNAPY.bat", "w") as f:
    f.write(
        f"./miniconda/condabin/conda create -n cnapy-{CNAPY_VERSION} -c Gurobi -c IBMDecisionOptimization -c conda-forge -c cnapy cnapy={CNAPY_VERSION} --yes"
    )

with open(f"{selected_folder}\\INSTALL_CNAPY.bat", "w") as f:
    f.write(
        f"./CNApy/miniconda/condabin/conda create -n cnapy-{CNAPY_VERSION} -c Gurobi -c IBMDecisionOptimization -c conda-forge -c cnapy cnapy={CNAPY_VERSION} --yes"
    )

with open(f"{selected_folder}\\cnapy-assistant-script.sh", "w") as f:
    f.write(
        "#!/bin/sh\n"
        f"./conda create -n cnapy-{CNAPY_VERSION} -c Gurobi -c IBMDecisionOptimization -c conda-forge -c cnapy cnapy={CNAPY_VERSION} --yes"
    )

"""
path = f"{selected_folder}\\CNApy"
with ZipFile(f"{selected_folder}\\cnapy_windows_installer.zip", 'w', ZIP_LZMA) as zip_obj:
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_obj.write(os.path.join(root, file),
                          os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))
    zip_obj.write(f"{selected_folder}\\INSTALL_CNAPY.bat", "./INSTALL_CNAPY.bat")

os.remove(f"{selected_folder}\\INSTALL_CNAPY.bat")
os.remove(f"{selected_folder}\\CNApy")
"""

messagebox.showinfo(
    "Successful installers generation",
    f"The installers were succesfully generated in {selected_folder}."
    "Remaining step: put the Windows installer (the .bat file and the CNApy subfolder) into a .zip file."
)
