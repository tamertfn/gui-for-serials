# DisplayCtrl class: Controls data visualization.
# It manages chart creation and updating, and real-time data streaming.

from tkinter import Frame, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot
import json
import threading
import time

class DisplayCtrl:
    def __init__(self):
        self.frame = None
        self.chart_frame = None
        self.chart_canvas = None
        self.ax = None
        self.running = False

    def set_frame(self, frame):
        self.frame = frame

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

            fig, self.ax = matplotlib.pyplot.subplots()
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.chart_canvas.get_tk_widget().pack(fill=BOTH, expand=True)

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
                print(f"JSON reading error: {e}")
                return {"T1": [], "T2": []}  # Default empty data

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
