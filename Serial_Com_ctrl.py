# SerialCtrl class: Manages serial communication.
# It handles port configuration, data reading and parsing, and JSON data saving.

import serial.tools.list_ports
import time
import threading
import re
import json

class SerialCtrl():
    def __init__(self):
        self.ports = list(serial.tools.list_ports.comports())
        self.ser = None
        self.is_connected = False
        self.read_thread = None
        self.data = {"T1": [], "T2": []}
    
    def serial_conf(self, Comgui):
        if not self.is_connected:
            try:
                self.ser = serial.Serial(
                    port=Comgui.clicked_com.get(),
                    baudrate=int(Comgui.clicked_bd.get()),
                    bytesize=int(Comgui.clicked_bs.get()),
                    parity=Comgui.clicked_par.get()[0],
                    stopbits=float(Comgui.clicked_sb.get()),
                    timeout=float(Comgui.entry_to.get())        
                )
                
                if self.ser.is_open:
                    print(f"Connected to {self.ser.port}")
                    self.is_connected = True
                    self.read_thread = threading.Thread(target=self.read_data, daemon=True)
                    self.read_thread.start()
            except serial.SerialException as e:
                print(f"Failed to connect: {e}")
                self.is_connected = False
        else:
            self.disconnect()

    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            if self.read_thread and self.read_thread.is_alive():
                try:
                    self.read_thread.join(timeout=1.0)
                except RuntimeError:
                    print("Error: Cannot join the current thread.")
            if self.ser:
                try:
                    self.ser.close()
                except Exception as e:
                    print(f"DISCONNECT An error occurred: {e}")
                self.ser = None
            print("Serial connection closed.")
            self.save_to_json()  # Save data to JSON file when disconnecting

    def read_data(self):
        buffer = ""
        try:
            while self.is_connected:
                try:
                    if self.ser and self.ser.in_waiting > 0:
                        received_data = self.ser.read(self.ser.in_waiting)
                        decoded_data = received_data.decode('utf-8', errors='ignore').replace('\0','')  # 'ignore' karakter hatalarını yoksayar
                        buffer += decoded_data
                        
                        # Verileri ayıkla
                        pattern = r'T1:\s*(\d+)\s*T2:\s*(\d+)'
                        matches = re.findall(pattern, buffer)
                        
                        if matches:
                            for match in matches:
                                t1_val, t2_val = match
                                try:
                                    t1_val = int(t1_val)
                                    t2_val = int(t2_val)
                                    self.data["T1"].append(t1_val)
                                    self.data["T2"].append(t2_val)
                                    parsed_data = {
                                        "T1": t1_val,
                                        "T2": t2_val
                                    }
                                    print(parsed_data)
                                    self.save_to_json()
                                except ValueError as e:
                                    print(f"Data parsing error: T1_data={t1_val}, T2_data={t2_val}. Error: {e}")
                                
                            # Buffer'ı temizle
                            last_match_end = buffer.rfind(matches[-1][-1]) + len(matches[-1][-1])
                            buffer = buffer[last_match_end:]
                        else:
                            print("No matches found in buffer.")
                    
                    time.sleep(0.1)
                    
                except serial.SerialException as e:
                    print(f"Serial connection lost. Error: {e}")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.disconnect()

    def save_to_json(self):
        try:
            with open("received_data.json", "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving JSON file: {e}")

if __name__ == "__main__":
    SerialCtrl()