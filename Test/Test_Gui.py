# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 08:04:38 2025

@author: micha
"""

from tkinter import *
import ttkbootstrap as tb

root = tb.Window(themename="superhero")

root.title("TTK Test")
root.geometry('500x350')


spec_wavelength = 900.00

def spec_set_wavelength():
    global spec_wavelength
    spec_wavelength = wavelength_input.get()
    test_label.config(text=str(spec_wavelength))

def set_wavelength_increment():
    wavelength_input['increment'] = set_delim.get()

def enter_wavelength():
    global spec_wavelength
    spec_wavelength=wavelength_input.get()
    test_label.config(text=str(spec_wavelength))


def enter_increment():
    wavelength_input['increment'] = set_delim.get()







test_label = tb.Label(root, text=str(spec_wavelength))
test_label.pack(pady=10)

wavelength_input = tb.Spinbox(root, bootstyle="success",from_=0.00,to=1800.00, format="%.2f",
                  command=spec_set_wavelength)
wavelength_input.pack(pady=5)
wavelength_input.set(spec_wavelength)


set_delim = tb.Spinbox(root, from_=0,to=5, increment=0.01,command=set_wavelength_increment)
set_delim.pack(pady=5)
set_delim.set(0.10)

enter_wavelength_button = tb.Button(root, text='Enter',command=enter_wavelength)
enter_wavelength_button.pack(pady=5)

enter_increment_button = tb.Button(root, text='Enter',command=enter_increment)
enter_increment_button.pack(pady=5)


root.mainloop()