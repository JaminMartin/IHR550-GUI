'''Michael Moull - Designed gui for the ihr550 spectrometer.'''




import tkinter as tk
''
import ttkbootstrap as tb

from ttkbootstrap.constants import *
import time
import threading
from spcs_instruments import HoribaiHR550 as ihr
from spcs_instruments.spcs_instruments_utils import load_config
import toml
from pathlib import Path




'''List all globals'''

spec_is_busy = False
spec = None
spec_wavelength = 900
entrance_slit=None
entrance_slit_width=None
exit_slit=None
exit_slit_width=None
grating=None


'''Config for spectrometer initialization'''
config = { "device": {"iHR550": {
    "grating" : "VIS",
    "step_size" : 0.1,
    "initial_wavelength" : 500,
    "final_wavelength" : 600,  
    "slits" : { "Entrance_Front" : 0.0, "Entrance_Side" : 0.0, "Exit_Front" : 0.0, "Exit_Side" : 0.0},
    "mirrors" : {
        "Entrance" : "front",
        "Exit" : "side",
    }
    }}} 

with open(Path(__file__).parent / "config.toml", "w") as f:
                toml.dump(config, f)

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
pane5 = tk.Frame(master)
pane5.grid(row=3, column=0, padx=10, pady=5)
pane6 = tk.Frame(master)
pane6.grid(row=3, column=1, padx=10, pady=5)


'''Initialize spec function'''

def initialize_spec_thread():
    global spec
    global spec_is_busy
    spec = ihr(config=Path(__file__).parent / "config.toml", connect_to_pyfex=False, bypass_homing= True)
    #time.sleep(10)
    spec_is_busy = False
    status_label.config(text='Spec Ready',background='green')


def initialize_spec():
    global spec
    global spec_is_busy
    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        spec_is_busy = True
        print('Initializing spectrometer')
        status_label.config(text='Spec Initializing',background='red')
        threading.Thread(target=initialize_spec_thread).start()
        grating_select.current(0)
        if entrance_slit_front_check.get() == 0:
            entrance_slit_front_check.set(1)
        else:
            pass
        if entrance_slit_side_check.get() == 1:
            entrance_slit_side_check.set(0)
        else:
            pass
        if exit_slit_side_check.get() == 0:
            exit_slit_side_check.set(1)
        else:
            pass
        if exit_slit_front_check.get() == 1:
            exit_slit_front_check.set(0)    
        else:
            pass
        wavelength_input.set(500) 
        exit_slit_width_select.current(0)
        entrance_slit_width_select.current(0)


        #spec = ihr(config=Path(__file__).parent / "config.toml", connect_to_pyfex=False, bypass_homing= True)
        #time.sleep(10)
        #spec_is_busy = False


def force_initialize_spec_thread():
    global spec
    global spec_is_busy
    spec = ihr(config=Path(__file__).parent / "config.toml", connect_to_pyfex=False, bypass_homing= False)
    #time.sleep(10)
    spec_is_busy = False
    status_label.config(text='Spec Ready',background='green')


def force_initialize_spec():
    global spec
    global spec_is_busy
    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        spec_is_busy = True
        status_label.config(text='Spec Initializing',background='red')
        print('Initializing spectrometer')
        threading.Thread(target=force_initialize_spec_thread).start()     
        grating_select.current(0)
        if entrance_slit_front_check.get() == 0:
            entrance_slit_front_check.set(1)
        else:
            pass
        if entrance_slit_side_check.get() == 1:
            entrance_slit_side_check.set(0)
        else:
            pass
        if exit_slit_side_check.get() == 0:
            exit_slit_side_check.set(1)
        else:
            pass
        if exit_slit_front_check.get() == 1:
            exit_slit_front_check.set(0)    
        else:
            pass
        wavelength_input.set(500) 
        exit_slit_width_select.current(0)
        entrance_slit_width_select.current(0)

'''functions for wavelength buttons'''

def spec_set_wavelength():
    global spec_wavelength
    global spec_is_busy

    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        new_wavelength = float(wavelength_input.get())
        if new_wavelength <= 1800 and new_wavelength >= 0:
            
            spec_is_busy = True
            spec.set_wavelength(new_wavelength)
            spec_is_busy = False
        else:
            print('This input is invalid')

def set_wavelength_increment():
    wavelength_input['increment'] = set_delim.get()

def enter_increment():
    
    num = float(set_delim.get())
    if num <= 5 and num >= 0:
        wavelength_input['increment'] = set_delim.get()
    else:
        print('This input is invalid')

'''Functions for slit buttons'''
def front_entrance_thread():
        global spec_is_busy
        entrance_slit_width = entrance_slit_width_select.get()
        spec.set_mirror('Entrance','front')
        spec.set_slit('Entrance_Front',float(entrance_slit_width))
        spec_is_busy = False
        status_label.config(text='Spec Ready',background='green')


def front_entrance_slit_select():
    global entrance_slit_width
    global spec_is_busy
    if spec_is_busy == True:
        print('Spectrometer is busy')
        entrance_slit_front_check.set(0)
        pass
    else:
        
        status_label.config(text='Changing entrance Mirror',background='red')
        if entrance_slit_side_check.get() == 1:
            entrance_slit_side_check.set(0)
            spec_is_busy = True
            spec.set_slit('Entrance_Side',0.0)
            spec_is_busy = False
        else:
            pass
        
        spec_is_busy = True

        threading.Thread(target=side_entrance_thread).start()


def side_entrance_thread():
        global spec_is_busy
        entrance_slit_width = entrance_slit_width_select.get()
        spec.set_mirror('Entrance','side')
        spec.set_slit('Entrance_Side',float(entrance_slit_width))
        spec_is_busy = False
        status_label.config(text='Spec Ready',background='green')

def side_entrance_slit_select():
    global entrance_slit_width
    global spec_is_busy
    
    if spec_is_busy == True:
        print('Spectrometer is busy')
        entrance_slit_side_check.set(0)
        pass
    
    else:
        status_label.config(text='Changing entrance Mirror',background='red')
        if entrance_slit_front_check.get() == 1:
            entrance_slit_front_check.set(0)
            spec_is_busy = True
            spec.set_slit('Entrance_Front',0.0)
            spec_is_busy = False
        else:
            pass
        spec_is_busy = True
        threading.Thread(target=side_entrance_thread).start()






def set_entrance_slit_width(e):
    global entrance_slit_width
    global spec_is_busy
    entrance_slit_width = entrance_slit_width_select.get()
    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        if entrance_slit_front_check.get() == 1:
            spec.set_slit('Entrance_Front',float(entrance_slit_width))
        elif entrance_slit_side_check.get() == 1:
            spec.set_slit('Entrance_Side',float(entrance_slit_width))
        else:
            print('Select an entrance slit')



def front_exit_thread():
        global spec_is_busy
        exit_slit_width = exit_slit_width_select.get()
        spec.set_mirror('Exit','front')
        spec.set_slit('Exit_Front',float(exit_slit_width))
        spec_is_busy = False
        status_label.config(text='Spec Ready',background='green')

def front_exit_slit_select():
    global exit_slit_width
    global spec_is_busy
    if spec_is_busy == True:
        print('Spectrometer is busy')
        exit_slit_front_check.set(0)
        pass
    else:
        status_label.config(text='Changing exit Mirror',background='red')
        if exit_slit_side_check.get() == 1:
            exit_slit_side_check.set(0)
            spec_is_busy = True
            spec.set_slit('Exit_Side',0.0)
            spec_is_busy = False
        else:
            pass
        
        threading.Thread(target=front_exit_thread).start()


def side_exit_thread():
        global spec_is_busy
        exit_slit_width = exit_slit_width_select.get()
        spec.set_mirror('Exit','side')
        spec.set_slit('Exit_Side',float(exit_slit_width))
        spec_is_busy = False
        status_label.config(text='Spec Ready',background='green')


def side_exit_slit_select():
    global exit_slit_width
    global spec_is_busy
    if spec_is_busy == True:
        print('Spectrometer is busy')
        exit_slit_side_check.set(0)

        pass
    
    else:
        status_label.config(text='Changing exit Mirror',background='red')
        if exit_slit_front_check.get() == 1:
            exit_slit_front_check.set(0)
            spec_is_busy = True
            spec.set_slit('Exit_Front',0.0)
            spec_is_busy = False
        else:
            pass
        spec_is_busy = True
        threading.Thread(target=side_exit_thread).start()



def exit_slit_front_adjust_thread():
    global spec_is_busy
    global exit_slit_width
    spec.set_slit('Exit_Front',float(exit_slit_width))
    spec_is_busy = False

def exit_slit_side_adjust_thread():
    global spec_is_busy
    global exit_slit_width
    spec.set_slit('Exit_Side',float(exit_slit_width))
    spec_is_busy = False

def set_exit_slit_width(e):
    global exit_slit_width
    global spec_is_busy
    exit_slit_width = exit_slit_width_select.get()
    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        spec_is_busy = True
        if exit_slit_front_check.get() == 1:
            threading.Thread(target=exit_slit_front_adjust_thread).start()
        elif exit_slit_side_check.get() == 1:
            threading.Thread(target=exit_slit_side_adjust_thread).start()
        else:
            print('Select an exit slit')

'''Grating Selection'''


def grating_thread():
    global spec_is_busy
    grating = grating_select.get()
    spec.set_turret(grating)
    spec_is_busy == False
    status_label.config(text='Spec Ready',background='green')


def set_grating(e):
    global grating
    if spec_is_busy == True:
        print('Spectrometer is busy')
        pass
    else:
        spec_is_busy == True
        status_label.config(text='Changing grating',background='red')
        threading.Thread(target=grating_thread).start()

        #grating = grating_select.get()
        #spec.set_turret(grating)
        #spec_is_busy == False


'''Gui features'''


'''initialize button'''
initialize_button = tb.Button(pane,text='Initialize',command=initialize_spec)
initialize_button.grid(pady=5,row=0,column=3)

'''Force initialize button'''
initialize_button = tb.Button(pane,text='Force Initialize',command=force_initialize_spec)
initialize_button.grid(pady=5,row=0,column=4)

'''wavelength control'''
#test_label = tb.Label(pane, text=str(spec_wavelength))
#test_label.grid(pady=5,row=0,column=0)

wavelength_input = tb.Spinbox(pane, bootstyle="success",from_=0.00,to=1800.00, format="%.2f",
                  command=spec_set_wavelength)
wavelength_input.grid(row=1,column=0,pady=5)
wavelength_input.set(spec_wavelength)


set_delim = tb.Spinbox(pane, from_=0,to=5, increment=0.01,command=set_wavelength_increment)
set_delim.grid(row=2,column=0,pady=5)
set_delim.set(0.10)

enter_wavelength_button = tb.Button(pane, text='Enter',command=spec_set_wavelength)
enter_wavelength_button.grid(row=1,column=1,pady=5)

enter_increment_button = tb.Button(pane, text='Enter',command=enter_increment)
enter_increment_button.grid(row=2,column=1,pady=5)


'''Entrance slit buttons'''
slit_options = [0.00,0.01,0.025,0.05,0.075,0.1,0.2,0.25,0.5,1,2,3,4,5,6,7]

entrance_slit_width_label = tb.Label(pane,text='Entrace slit width (mm)')
entrance_slit_width_label.grid(pady=5,row=5,column=0)
entrance_slit_width_select = tb.Combobox(pane,values=slit_options)
entrance_slit_width_select.grid(row=5,column=1,pady=5)
entrance_slit_width_select.bind("<<ComboboxSelected>>", set_entrance_slit_width)

#test_button = tb.Button(pane,text='test',command=set_entrance_slit_width)
#test_button.grid(pady=5,row=5,column=5)


entrace_slit_label = tb.Label(pane,text='Entrance slit')
entrace_slit_label.grid(pady=5,row=4,column=0)
entrance_slit_front_check = tk.IntVar()
entrace_slit_button_front = tb.Checkbutton(pane, text='Front', style='Toolbutton',command=front_entrance_slit_select,variable=entrance_slit_front_check)
entrace_slit_button_front.grid(pady=5,row=4,column=1)
entrance_slit_side_check = tk.IntVar()
entrace_slit_button_side = tb.Checkbutton(pane, text='Side', style='Toolbutton',command=side_entrance_slit_select,variable=entrance_slit_side_check)
entrace_slit_button_side.grid(pady=5,row=4,column=2)






'''Exit slit buttons'''

exit_slit_label = tb.Label(pane,text='Exit slit')
exit_slit_label.grid(pady=5,row=6,column=0)
exit_slit_front_check = tk.IntVar()
exit_slit_button_front = tb.Checkbutton(pane, text='Front', style='Toolbutton',command=front_exit_slit_select,variable=exit_slit_front_check)
exit_slit_button_front.grid(pady=5,row=6,column=1)
exit_slit_side_check = tk.IntVar()
exit_slit_button_side = tb.Checkbutton(pane, text='Side', style='Toolbutton',command=side_exit_slit_select,variable=exit_slit_side_check)
exit_slit_button_side.grid(pady=5,row=6,column=2)


exit_slit_width_label = tb.Label(pane,text='Exit slit width (mm)')
exit_slit_width_label.grid(pady=5,row=7,column=0)
exit_slit_options = [0.00,0.01,0.025,0.05,0.075,0.1,0.2,0.25,0.5,1,2,3,4,5,6,7]
exit_slit_width_select = tb.Combobox(pane,values=slit_options)
exit_slit_width_select.grid(row=7,column=1,pady=5)
exit_slit_width_select.bind("<<ComboboxSelected>>", set_exit_slit_width)

'''Set Grating'''


grating_label = tb.Label(pane,text='Select Grating')
grating_label.grid(pady=5,row=3,column=3)
grating_options = ['VIS','NIR','MIR']
grating_select = tb.Combobox(pane,values=grating_options)
grating_select.grid(pady=5,row=3,column=4)
grating_select.bind("<<ComboboxSelected>>", set_grating)



status_fix_label = tb.Label(pane,text='Spec_Status:')
status_fix_label.grid(pady=5,row=9,column=0)
status_label = tb.Label(pane,text='Spec not initialized')
status_label.grid(pady=5,row=9,column=1)


def run_app():
    master.mainloop()

if __name__ == "__main__":
    run_app()







#Button to initialize spectrometer
#initialise_spec = tb.Button(pane, text='Initialise', command = initialise()).grid(row=1,column=0, padx=5, pady=5)
#initialise_spec_button = tb.Button(pane, text='Initialise')

#grating = 

#exit_mirror

#ntry_mirror


#adjustable box to set spectrometer wavelength, when want 


#default_wavelength = spec.wavelength











#entry_slit_size

#exit_slit_size


#master.mainloop()