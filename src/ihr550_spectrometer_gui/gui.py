import tkinter as tk

import ttkbootstrap as tb

from ttkbootstrap.constants import *
from time import sleep

from spcs_instruments import HoribaiHR550
from spcs_instruments.spcs_instruments_utils import load_config
import toml
from pathlib import Path
style = tb.Style()
theme_path = Path(__file__).parent / "theme.json"
style.load_user_themes(theme_path)
style.theme_use('gruvbox')
master = style.master
master.iconbitmap(Path(__file__).parent / "spectra.ico")
master.title('Horiba Spectrometer Control')
pane = tk.Frame(master)
pane.grid(row=0, column=0, padx=10, pady=5)
pane2 = tk.Frame(master)
pane2.grid(row=0, column=1, padx=10, pady=5)
pane3 = tk.Frame(master)
pane3.grid(row=1, column=0, padx=10, pady=5)
pane4 = tk.Frame(master)
pane4.grid(row=1, column=1, padx=10, pady=5)


def run_app():
    master.mainloop()

if __name__ == "__main__":
    run_app()