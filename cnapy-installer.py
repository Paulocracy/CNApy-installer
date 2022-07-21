
import subprocess
import os
import sys
import urllib.request
from elevate import elevate
from tkinter import Tk, messagebox, Label, Button
from tkinter import filedialog
# See https://stackoverflow.com/questions/39948588/non-blocking-file-read
from concurrent.futures import ThreadPoolExecutor

g_selected_folder = ""
installation_successful = False


def on_cnapy_installation_finish(future) -> None:
    global main
    global g_selected_folder
    global installation_successful

    if not installation_successful:
        sys.exit(0)

    main.withdraw()
    messagebox.showinfo(
        "Success!",
        "CNApy was installed successfully. In order to start CNApy, click on the respective "
        "newly created CNApy icon on your desktop or in the start menu.\n"
        "NOTE 1: It is recommended to download the CNApy example projects (including interactive maps of models "
        "such as ECC2, iML1515 and many more) by starting CNApy and clicking on 'Download CNApy example projects...' "
        "in the 'Projects' menu entry.\n"
        "NOTE 2: In order to deinstall CNApy, go to the folder where you installed CNApy, click on the "
        "'UNINSTALL_CNAPY.bat' script and follow the deinstallation instructions "
        "(which are branded for miniconda).\n"
        "You installed CNApy in the following folder:\n"
        f"{g_selected_folder}\n"
    )
    sys.exit(0)


def run_cnapy_installation(selected_folder: str) -> None:
    MINICONDA_EXE_URL = "https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Windows-x86_64.exe"
    miniconda_exe_name = "miniconda.exe"
    miniconda_exe_path = f"{selected_folder}{miniconda_exe_name}"
    try:
        urllib.request.urlretrieve(MINICONDA_EXE_URL, miniconda_exe_path)
    except Exception:
        main.withdraw()
        messagebox.showerror(
            "Error while downloading",
            "An error occurred in a download process of the installation.\n"
            "Please make sure that your internet connection works and retry the installation."
        )
        sys.exit(0)

    miniconda_install_path = f"{selected_folder}miniconda\\"
    if os.path.exists(miniconda_install_path):
        main.withdraw()
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
        main.withdraw()
        messagebox.showerror(
            "Error while running installation process",
            "Error during the execution of the installation process.\n"
            "Please make sure that you have full access permissions on the selected installation folder."
        )
        sys.exit(0)

    conda_path = f"{miniconda_install_path}\\condabin\\conda"
    ibm_command = f'"{conda_path}" config --add channels IBMDecisionOptimization'
    gurobi_command = f'"{conda_path}" config --add channels Gurobi'
    cnapy_command = f'"{conda_path}" create -n cnapy-{CNAPY_VERSION} -c conda-forge -c cnapy cnapy={CNAPY_VERSION} --yes'
    clean_command = f'"{conda_path} clean -a --yes'

    os.system(ibm_command)
    os.system(gurobi_command)
    os.system(cnapy_command)
    os.system(clean_command)

    os.remove(miniconda_exe_path)

    uninstaller_path = f"{selected_folder}UNINSTALL_CNAPY.bat"
    with open(uninstaller_path, "w") as f:
        f.write(
            "cd miniconda\n"
            "Uninstall-Miniconda3.exe"
        )
    installation_successful = True


def installation_process() -> None:
    button.pack_forget()
    label.config(
        text="Please follow the instructions in the message pop-up boxes of this installer"
    )
    main.withdraw()

    messagebox.showinfo(
        "Choose the CNApy installation folder",
        "In the next step, choose an folder (e.g., a newly created folder) on your computer "
        "where you want CNApy to be installed."
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
            "No valid CNApy installation folder selected",
            "It appears that you didn't select a valid CNApy installation folder.\n"
            "Please try the CNApy installation process again in a different folder "
            "and without clicking on 'Cancel'."
        )
        sys.exit(0)
    if len(os.listdir(selected_folder)) > 0:
        new_folder_name = "CNApy"
        if os.path.exists(f"{selected_folder}{new_folder_name}"):
            counter = 2
            while os.path.exists(f"{selected_folder}{new_folder_name}"):
                new_folder_name = f"CNApy{counter}"
                counter += 1
        selected_folder += new_folder_name + "\\"

        answer = messagebox.askyesno(
            "Confirm folder for CNApy installation",
            "Your selected folder is not empty. Since CNApy needs to be installed in an empty folder,"
            f"the new empty subfolder {selected_folder} will be created and, therefore, CNApy will be "
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
        "Now, CNApy is going to be installed. This may take a while.\n"
        "Please be patient until a new message appears.\n"
        "Do you want to proceed with the CNApy installation?"
    )
    label.config(
        text="CNApy installation running...\n"
        "Please be patient until a new pop-up message appears"
    )
    main.deiconify()
    if not answer:
        sys.exit(0)

    global g_selected_folder
    g_selected_folder = selected_folder

    executor = ThreadPoolExecutor(1)
    future_installation = executor.submit(run_cnapy_installation, selected_folder)
    future_installation.add_done_callback(on_cnapy_installation_finish)


# If you just want to update the CNApy version, you just have to edit the following string:
CNAPY_VERSION = "1.0.9"

# Request elevated user rights
# Found thanks to
# https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
try:
    elevate()
except Exception:
    messagebox.showinfo(
        "No administrator rights given",
        "The CNApy installer did not get administrator rights. This means that you cannot install "
        "CNApy in many folders, e.g. 'Program Files'. You can still try to install CNApy "
        "in other folders."
    )

# Start the actual GUI program
main = Tk()
main.title("CNApy installer")
label = Label(
    main,
    text="Welcome to the CNApy installer! "
    f"This program will install the latest CNApy version ({CNAPY_VERSION}) for you.\n"
    "Click on the 'Start installation process' button in order to run CNApy's installation:"
)
button = Button(
    text="Start installation process",
    command=installation_process,
)
label.pack()
button.pack()
main.mainloop()
