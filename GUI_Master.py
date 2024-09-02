import tkinter as tk
from tkinter import *
from tkinter import Button, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import threading
import time
import matplotlib.pyplot as plt

class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("Serial communication")
        self.root.geometry("500x500")
        self.root.config(bg="white")

# Class to setup and create the communication manager with MCU
class ComGUI():
    def __init__(self, root, serial):
        '''
        Initialize the connexion GUI and initialize the main widgets 
        '''
        # Initializing the Widgets
        self.root = root
        self.serial = serial
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
        self.clicked_com.set(coms[-1])
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
        self.clicked_bd.set(bds[-1])
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
        self.clicked_bs.set(bss[-2])
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
        self.clicked_par.set(pars[1])
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
        self.clicked_sb.set(sbs[1])
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
            thread = threading.Thread(target=self.serial.serial_conf, args=(self,), daemon=True)
            thread.start()
            print(f"THREAD NUMARA: {thread.name}")
            self.btn_connect['text'] = "Disconnect"
            thread2 = threading.Thread(target=self.initialize_DispGUI, args=(self.root,self.serial, ), daemon=True)
            thread2.start()
            self.freeze_options()  # Freeze options when connected
        else:
            self.serial.disconnect()
            self.btn_connect['text'] = "Connect"
            self.unfreeze_options()  # Unfreeze options when disconnected

    def freeze_options(self):
        for menu in [self.drop_com, self.drop_baud, self.drop_bs, self.drop_par, self.drop_sb]:
            menu.config(state="disabled")
        self.entry_to.config(state="disabled")

    def unfreeze_options(self):
        for menu in [self.drop_com, self.drop_baud, self.drop_bs, self.drop_par, self.drop_sb]:
            menu.config(state="normal")
        self.entry_to.config(state="normal")
    
    def initialize_DispGUI(self, root, serial):
        Dispgui = DispGUI(root, serial)

class DispGUI():
    def __init__(self, root, serial):
        '''
        Initialize main Widgets for communication GUI
        '''
        self.root = root
        self.serial = serial
        self.chart_frame = None
        self.chart_canvas = None
        self.ax = None
        self.running = False

        # Build ConnGui Static Elements
        self.frame = tk.LabelFrame(root, text="Display Manager",
                                padx=5, pady=5, bg="white", width=60)
        self.DispGUIOpen()

    def DispGUIOpen(self):
        '''
        Method to display all the widgets 
        '''
        self.root.geometry("800x800")
        self.frame.grid(row=8, column=0, rowspan=3, columnspan=5, padx=5, pady=5)

        # Buttons for chart control
        self.btn_start_stream = Button(self.frame, text="Start Stream", command=self.start_stream)
        self.btn_start_stream.grid(column=0, row=8, padx=5, pady=5)

        self.btn_stop_stream = Button(self.frame, text="Stop Stream", command=self.stop_stream)
        self.btn_stop_stream.grid(column=1, row=8, padx=5, pady=5)

        self.btn_new_chart = Button(self.frame, text="New Chart", command=self.new_chart)
        self.btn_new_chart.grid(column=2, row=8, padx=5, pady=5)

        self.btn_kill_chart = Button(self.frame, text="Kill Chart", command=self.kill_chart)
        self.btn_kill_chart.grid(column=3, row=8, padx=5, pady=5)

        self.btn_save_data = Button(self.frame, text="Save Data", command=self.save_data)
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

    def start_stream(self):
        if self.chart_canvas is not None:
            self.running = True
            self.update_chart()

    def stop_stream(self):
        self.running = False

    def new_chart(self):
        if self.chart_frame is None:
            self.chart_frame = Frame(self.frame)
            self.chart_frame.grid(row=10, column=0, columnspan=5)

            fig, self.ax = plt.subplots()
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.ax.set_title('Real-Time Data')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Value')

            self.chart_canvas.draw()

    def update_chart(self):
        def read_json_data():
            try:
                with open("received_data.json", "r") as file:
                    data = json.load(file)
                    return data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"JSON okuma hatası: {e}")
                return {"T1": [], "T2": []}  # Varsayılan boş veri

        def animate():
            while self.running:
                data = read_json_data()

                if data:
                    T1_data = data.get("T1", [])[-50:]  # Get the last 50 data points
                    T2_data = data.get("T2", [])[-50:]
                    time_data = list(range(len(T1_data)))  # Time data is index-based

                    self.ax.clear()
                    self.ax.plot(time_data, T1_data, label="T1", marker='o')
                    self.ax.plot(time_data, T2_data, label="T2", marker='o')
                    self.ax.set_title('Real-Time Data')
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('Value')
                    self.ax.legend()

                    self.chart_canvas.draw()

                time.sleep(1)  # Update interval in seconds

        threading.Thread(target=animate, daemon=True).start()


    def kill_chart(self):
        if self.chart_frame is not None:
            self.chart_frame.destroy()
            self.chart_frame = None
            self.chart_canvas = None

    def save_data(self):
        # Implement the save data functionality
        pass

if __name__ == "__main__":
    RootGUI()
    ComGUI()
    DispGUI()