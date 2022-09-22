from elevate import elevate
import os
from tkinter import Tk, messagebox

try:
    elevate()
except Exception:
    main = Tk()
    main.withdraw()
    messagebox.showinfo(
        "No administrator rights given",
        "The CNApy uninstaller did not get administrator rights. This may make it necessary to "
        "uninstall this folder manually by slecting it and deleting it with the delete button."
    )

os.system("start ./miniconda/Uninstall-Miniconda3.exe")
