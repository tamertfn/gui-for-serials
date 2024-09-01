import serial.tools.list_ports
import time

class SerialCtrl():
    def __init__(self):
        self.ports = list(serial.tools.list_ports.comports())
    
    def serial_conf(self, Comgui):
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
    
        try:
            with open("received_data.txt", "a") as file:  # Dosyayı aç veya oluştur (ekleme modunda)
                while True:
                    if self.ser.in_waiting > 0:
                        received_data = self.ser.read(self.ser.in_waiting)
                        decoded_data = received_data.decode('utf-8').replace('\n','').replace('\0','')
                        print(decoded_data,end="")
                        
                        # Dosyaya yaz
                        file.write(decoded_data)
                        file.flush()
                        
                        # Echo the received data back
                        self.ser.write(received_data)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Ensure the serial port is closed properly
            self.ser.close()
            print("Serial connection closed.")
            
if __name__ == "__main__":
    SerialCtrl()