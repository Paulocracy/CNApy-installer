import subprocess
import os
import sys
import urllib.request
from tkinter import Tk, messagebox
from tkinter import filedialog

# If you just want to update the CNApy version, you just have to edit the following string:
CNAPY_VERSION = "1.0.8"

main = Tk()
main.withdraw()

answer = messagebox.askyesno(
    "CNApy installer",
    "This program will install the latest CNApy version for you.\n"
    "Do you want to proceed with the CNApy installation?"
)

if not answer:
    sys.exit(0)

messagebox.showinfo(
    "Choose the CNApy installation folder",
    "In the next step, choose the folder on your computer\n"
    "where you want CNApy to be installed."
)

selected_folder = filedialog.askdirectory(
    title="Choose CNApy installation folder",
)

if selected_folder == "":
    messagebox.showerror(
        "No valid CNApy installation folder selected",
        "It appears that you didn't select a valid CNApy installation folder.\n"
        "Please try the CNApy installation process again in a different folder "
        "and without clicking on 'Cancel'."
    )
    sys.exit(0)

selected_folder = selected_folder.replace("/", "\\")
if not selected_folder.endswith("\\"):
    selected_folder += "\\"

answer = messagebox.askyesno(
    "Choosing folder successful",
    "Now, CNApy is going to be installed. This may take alot of time.\n"
    "Please be patient until a new message appears.\n"
    "Do you want to proceed with the CNApy installation?"
)
if not answer:
    sys.exit(0)

MINICONDA_EXE_URL = "https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Windows-x86_64.exe"
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

miniconda_install_path = f"{selected_folder}miniconda\\"
if os.path.exists(miniconda_install_path):
    messagebox.showerror(
        "CNApy seems to be already downloaded in this folder",
        "It looks like CNApy is already downloaded in the given folder.\n"
        "Please install this version of CNApy in a new folder.\n"
        "Alternatively, uninstall the other CNApy version by using the 'UNINSTALL_CNAPY.bat'\n"
        "in the respective folder."
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
        "Unknown error during the execution of the installation process.\n"
        "Please make sure that you have full access permissions on the selected installation folder."
    )
    sys.exit(0)

conda_path = f"{miniconda_install_path}\\condabin\\conda"
ibm_command = f'"{conda_path}" config --add channels IBMDecisionOptimization'
gurobi_command = f'"{conda_path}" config --add channels Gurobi'
cnapy_command = f'"{conda_path}" create -n cnapy-{CNAPY_VERSION} -c conda-forge -c cnapy cnapy={CNAPY_VERSION} --yes'

os.system(ibm_command)
os.system(gurobi_command)
os.system(cnapy_command)

os.remove(miniconda_exe_path)

uninstaller_path = f"{selected_folder}UNINSTALL_CNAPY.bat"
with open(uninstaller_path, "w") as f:
    f.write(
        "cd miniconda\n"
        "Uninstall-Miniconda3.exe"
    )

messagebox.showinfo(
    "Success!",
    "CNApy was installed successfully. In order to start it, click on the respective\n"
    "newly created CNApy icon on your desktop or in the start menu. You can also search\n"
    "for CNApy using the task bar.\n"
    "NOTE: In order to deinstall CNApy, go to the folder where you installed CNApy, click on the\n"
    "'UNINSTALL_CNAPY.bat' script and follow the deinstallation instructions (which are branded for miniconda)."
)
