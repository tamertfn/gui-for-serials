import serial.tools.list_ports
import time
import threading

class SerialCtrl():
    def __init__(self):
        self.ports = list(serial.tools.list_ports.comports())
        self.ser = None
        self.is_connected = False
        self.read_thread = None
    
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
            if self.read_thread:
                self.read_thread.join(timeout=1.0)
            if self.ser:
                try:
                    self.ser.close()
                except Exception as e:
                    print(f"DISCONNECT An error occurred: {e}")
                self.ser = None
            print("Serial connection closed.")

    def read_data(self):
        try:
            with open("received_data.txt", "a") as file:
                while self.is_connected:
                    try:
                        if self.ser and self.ser.in_waiting > 0:
                            received_data = self.ser.read(self.ser.in_waiting)
                            decoded_data = received_data.decode('utf-8').replace('\n','').replace('\0','')
                            print(decoded_data, end="")
                            
                            file.write(decoded_data)
                            file.flush()
                            
                            self.ser.write(received_data)
                    except serial.SerialException:
                        print("Serial connection lost.")
                        break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.disconnect()

if __name__ == "__main__":
    SerialCtrl()