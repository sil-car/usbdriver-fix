import logging
import sys
import tkinter as tk
import tkinter.ttk as ttk
from os import getenv
from pathlib import Path
from queue import Queue
from sys import platform
from threading import Thread
from tkinter import filedialog
from tkinter import messagebox

from . import host
from . import usb


class App(tk.Tk):
    def __init__(self, runmode, **kwargs):
        super().__init__(**kwargs)
        self.style = ttk.Style()
        self.runmode = runmode
        if self.runmode == 'frozen':
            self.data_dir = Path(sys._MEIPASS) / 'data'
        else:
            self.data_dir = Path(__file__).parents[2] / 'data'
        iconfile = str(self.data_dir / 'icon.png')
        self.iconphoto(True, tk.PhotoImage(file=iconfile))


class ActionPickerLayout(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid(column=0, row=0)
        self.config(borderwidth=10)
        self.parent = parent
        self.parent.title("Fix USBDriver.exe")
        self.parent.minsize(300, 0)

        self.label = ttk.Label(self, text="Effectuer réparation de :")
        self.usb_button = ttk.Button(
            self,
            text="Clé",
            command=self.on_usb_released
        )
        self.sys_button = ttk.Button(
            self,
            text="Système",
            command=self.on_sys_released
        )
        for c in self.winfo_children():
            c.grid_configure(padx=5, pady=5)

        self.label.grid(column=0, row=0)
        self.usb_button.grid(column=0, row=1)
        self.sys_button.grid(column=1, row=1)


class ActionPicker(ActionPickerLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.platform = platform

        # Set platform-specific config.
        if self.platform.startswith('linux'):
            self.parent.style.theme_use('default')
            self.start_dir = f'/media/{getenv("USER")}'
            self.sys_button.state(['disabled'])
        elif 'win' in self.platform:
            self.parent.style.theme_use('winnative')
            self.start_dir = Path.home()
        elif self.platform == 'darwin':
            self.parent.style.theme_use('aqua')
            self.sys_button.state(['disabled'])
            self.start_dir = Path.home()

        # Define events and queues.
        self.prog_evt = '<<ProgDone>>'
        self.usb_q = Queue()
        self.usb_evt = '<<UsbDone>>'
        self.sys_q = Queue()
        self.sys_evt = '<<SysDone>>'
        self.bind(self.prog_evt, self.on_usb_finish)

    def on_usb_released(self):
        dir_path = filedialog.askdirectory(
            title="Sélection de la clé USB",
            initialdir=self.start_dir,
        )
        if len(dir_path) < 1:  # user cancelled USB selection
            return
        else:
            t = Thread(target=usb.fix, args=(dir_path, self), daemon=True)
            t.start()
            ProgressWindow(self)

    def on_usb_finish(self, evt=None):
        result = self.usb_q.get()
        if isinstance(result, str):
            messagebox.showerror(title="Échec", message=result)
        else:
            messagebox.showinfo(title="Succès", message="Clé nettoyée !")

    def on_sys_released(self):
        result = host.fix()
        if isinstance(result, str):
            messagebox.showerror(title="Échec", message=result)
        else:
            messagebox.showinfo(title="Succès", message="Système nettoyé !")


class ProgressWindow(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.title = ''
        self.minsize(200, 0)
        self.grid_columnconfigure(0, weight=1)
        self.prog = ttk.Progressbar(self, mode='indeterminate')
        self.prog.grid(column=0, row=0, sticky='we')
        self.parent.bind(self.parent.usb_evt, self.on_end)
        self.prog.start()

    def on_end(self, evt=None):
        self.withdraw()
        self.parent.event_generate(self.parent.prog_evt)
        self.destroy()


def main():
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    date_format = '%H:%M:%S'
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        runmode = 'frozen'
        logging.basicConfig(
            filename=Path(sys.executable).parent / 'Fix USBDriver.log',
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
        )
    else:
        runmode = 'script'
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
        )
    classname = 'fixusbdriver'
    app = App(className=classname, runmode=runmode)
    ActionPicker(app, class_=classname)
    app.mainloop()


if __name__ == '__main__':
    main()
