# This file contains the main GUI classes for the Serial Communication GUI application.
# It includes RootGUI, ComGUI, and DispGUI classes which manage different aspects of the user interface.

from tkinter import *
import threading

# RootGUI class: Initializes the main application window.
class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("Serial communication")
        self.root.geometry("500x500")
        self.root.config(bg="white")

# ComGUI class: Manages the communication settings and interface.
# It includes dropdown menus for selecting communication parameters,
# Connect/Disconnect button, and Refresh button for updating available COM ports.
class ComGUI():
    def __init__(self, root, serial, display_ctrl):
        '''
        Initialize the connexion GUI and initialize the main widgets 
        '''
        # Initializing the Widgets
        self.root = root
        self.serial = serial
        self.display_ctrl = display_ctrl
        self.frame = LabelFrame(root, text="Com Manager",
                                padx=5, pady=5, bg="white")
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        self.label_bd = Label(
            self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")
        self.label_bs = Label(
            self.frame, text="Bytesize: ", bg="white", width=15, anchor="w")
        self.label_par = Label(
            self.frame, text="Parity: ", bg="white", width=15, anchor="w")
        self.label_sb = Label(
            self.frame, text="Stopbits: ", bg="white", width=15, anchor="w")
        self.label_to = Label(
            self.frame, text="Timeout(s): ", bg="white", width=15, anchor="w")

        # Setup the Drop option menu
        self.baudOptionMenu()
        self.ComOptionMenu()
        self.bsOptionMenu()
        self.parOptionMenu()
        self.sbOptionMenu()
        self.toOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_refresh = Button(self.frame, text="Refresh",
                                  width=10,  command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect",
                                  width=10, state="disabled", command=self.toggle_connection)

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()

        self.option_menus = []  # List to store all option menus

        self.dispgui = None

    def publish(self):
        '''
         Method to display all the Widget of the main frame
        '''
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.label_bd.grid(column=1, row=3)
        self.label_bs.grid(column=1, row=4)
        self.label_par.grid(column=1, row=5)
        self.label_sb.grid(column=1, row=6)
        self.label_to.grid(column=1, row=7)

        self.drop_com.grid(column=2, row=2, padx=self.padx)
        self.drop_baud.grid(column=2, row=3, padx=self.padx, pady=self.pady)
        self.drop_bs.grid(column=2, row=4, padx=self.padx, pady=self.pady)
        self.drop_par.grid(column=2, row=5, padx=self.padx, pady=self.pady)
        self.drop_sb.grid(column=2, row=6, padx=self.padx, pady=self.pady)
        self.entry_to.grid(column=2, row=7, padx=self.padx, pady=self.pady)

        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3)

    def ComOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms
        coms = ["-"]
        for port in self.serial.ports:
            coms.append(port.name)
        
        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *coms, command=self.connect_ctrl)
        self.drop_com.config(width=10)

    def baudOptionMenu(self):
        '''
         Method to list all the baud rates in a drop menu
        '''
        self.clicked_bd = StringVar()
        bds = ["-",
               "300",
               "600",
               "1200",
               "2400",
               "4800",
               "9600",
               "14400",
               "19200",
               "28800",
               "38400",
               "56000",
               "57600",
               "115200"]
        self.clicked_bd.set(bds[0])
        self.drop_baud = OptionMenu(
            self.frame, self.clicked_bd, *bds, command=self.connect_ctrl)
        self.drop_baud.config(width=10)
    
    def bsOptionMenu(self):
        '''
         Method to list all the bytesize in a drop menu
        '''
        self.clicked_bs = StringVar()
        bss = ["-",
               "5",
               "6",
               "7",
               "8",
               "9",]
        self.clicked_bs.set(bss[0])
        self.drop_bs = OptionMenu(
            self.frame, self.clicked_bs, *bss, command=self.connect_ctrl)
        self.drop_bs.config(width=10)
        
    def parOptionMenu(self):
        '''
         Method to list all the parity in a drop menu
        '''
        self.clicked_par = StringVar()
        pars = ["-",
               "None",
               "Even",
               "Odd",
               "Mark",
               "Space",]
        self.clicked_par.set(pars[0])
        self.drop_par = OptionMenu(
            self.frame, self.clicked_par, *pars, command=self.connect_ctrl)
        self.drop_par.config(width=10)
        
    def sbOptionMenu(self):
        '''
         Method to list all the stopbits in a drop menu
        '''
        self.clicked_sb = StringVar()
        sbs = ["-",
               "1",
               "1.5",
               "2",]
        self.clicked_sb.set(sbs[0])
        self.drop_sb = OptionMenu(
            self.frame, self.clicked_sb, *sbs, command=self.connect_ctrl)
        self.drop_sb.config(width=10)
        
    def toOptionMenu(self):
        '''
         Method to entry timeout in a entry
        '''
        self.entry_var = StringVar()
        self.entry_var.trace_add("write", self.connect_ctrl)
        
        self.entry_to = Entry(self.frame, width=15,
                              background="Light Gray", textvariable=self.entry_var)
        self.entry_to.insert(0, "")

    def connect_ctrl(self, widget, *args):
        '''
        Method to keep the connect button disabled if all the
        conditions are not cleared
        '''
        # Check if any dropdown is not selected or if the timeout entry is invalid
        dropdowns_not_selected = [
            self.clicked_bd.get() == '-',
            self.clicked_com.get() == '-',
            self.clicked_bs.get() == '-',
            self.clicked_par.get() == '-',
            self.clicked_sb.get() == '-'
        ]
        
        timeout_invalid = self.is_valid(self.entry_to.get())
        
        if any(dropdowns_not_selected) or timeout_invalid:
            self.btn_connect["state"] = "disabled"
        else:
            self.btn_connect["state"] = "active"
    
    def is_valid(self, value):
        try:
            value = float(value)
            return False
        except ValueError:
            return True

    def com_refresh(self):
        print("Refresh")
        self.unfreeze_options()

    def toggle_connection(self):
        if not self.serial.is_connected:
            # Thread for serial configuration
            serial_thread = threading.Thread(target=self.connect_and_initialize, daemon=True)
            serial_thread.start()
            print(f"Serial Thread: {serial_thread.name}")
        else:
            self.disconnect_and_cleanup()

    def connect_and_initialize(self):
        self.serial.serial_conf(self)
        if self.serial.is_connected:
            self.root.after(0, self.update_ui_after_connect)

    def update_ui_after_connect(self):
        self.btn_connect['text'] = "Disconnect"
        self.freeze_options()
        # Thread for DispGUI initialization
        disp_thread = threading.Thread(target=self.initialize_DispGUI, daemon=True)
        disp_thread.start()
        print(f"DispGUI Thread: {disp_thread.name}")

    def disconnect_and_cleanup(self):
        self.serial.disconnect()
        self.root.after(0, self.update_ui_after_disconnect)

    def update_ui_after_disconnect(self):
        self.btn_connect['text'] = "Connect"
        self.unfreeze_options()
        if self.dispgui:
            self.dispgui.DispGUIClose()
            self.dispgui = None

    def freeze_options(self):
        for menu in [self.drop_com, self.drop_baud, self.drop_bs, self.drop_par, self.drop_sb]:
            menu.config(state="disabled")
        self.entry_to.config(state="disabled")

    def unfreeze_options(self):
        for menu in [self.drop_com, self.drop_baud, self.drop_bs, self.drop_par, self.drop_sb]:
            menu.config(state="normal")
        self.entry_to.config(state="normal")
    
    def initialize_DispGUI(self):
        if self.dispgui is None:
            self.dispgui = DispGUI(self.root, self.serial, self.display_ctrl)
            self.root.after(0, self.dispgui.publish)

# DispGUI class: Handles the display management interface.
# It includes Start/Stop stream buttons, New Chart/Kill Chart buttons, and Save Data button.
class DispGUI():
    def __init__(self, root, serial, display_ctrl):
        '''
        Initialize main Widgets for communication GUI
        '''
        self.root = root
        self.serial = serial
        self.display_ctrl = display_ctrl
        self.chart_frame = None
        self.chart_canvas = None

        # Build ConnGui Static Elements
        self.frame = LabelFrame(root, text="Display Manager",
                                padx=5, pady=5, bg="white", width=60)
        
        # Pass the frame to DisplayCtrl
        self.display_ctrl.set_frame(self.frame)

        # Initialize widgets
        self.btn_start_stream = Button(self.frame, text="Start Stream", command=self.display_ctrl.start_stream)
        self.btn_stop_stream = Button(self.frame, text="Stop Stream", command=self.display_ctrl.stop_stream)
        self.btn_new_chart = Button(self.frame, text="New Chart", command=self.display_ctrl.new_chart)
        self.btn_kill_chart = Button(self.frame, text="Kill Chart", command=self.display_ctrl.kill_chart)
        self.btn_save_data = Button(self.frame, text="Save Data", command=self.display_ctrl.save_data)
        
        # Publish widgets
        self.publish()

    def publish(self):
        '''
        Method to display all the widgets
        '''
        self.root.geometry("800x800")
        self.frame.grid(row=8, column=0, rowspan=3, columnspan=5, padx=5, pady=5)

        # Layout for buttons
        self.btn_start_stream.grid(column=0, row=8, padx=5, pady=5)
        self.btn_stop_stream.grid(column=1, row=8, padx=5, pady=5)
        self.btn_new_chart.grid(column=2, row=8, padx=5, pady=5)
        self.btn_kill_chart.grid(column=3, row=8, padx=5, pady=5)
        self.btn_save_data.grid(column=4, row=8, padx=5, pady=5)

    def DispGUIClose(self):
        '''
        Method to close the connection GUI and destroy the widgets
        '''
        # Must destroy all the elements so they are not kept in memory
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("500x500")

if __name__ == "__main__":
    RootGUI()
    ComGUI()    
    DispGUI()