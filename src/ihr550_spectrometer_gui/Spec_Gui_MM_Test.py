'''test script for m.moull to workj on gui interface'''


import tkinter as tk
''
import ttkbootstrap as tb

from ttkbootstrap.constants import *
from time import sleep

from spcs_instruments import HoribaiHR550
from spcs_instruments.spcs_instruments_utils import load_config
import toml
from pathlib import Path



master = tb.Window(themename="mmoull")
master.geometry('500x350')
            
initialise_spec = tb.Button(master, text='Initialise')
initialise_spec.pack(pady=20)

master.mainloop()