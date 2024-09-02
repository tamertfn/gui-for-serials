# Serial Communication GUI

This project provides a graphical user interface (GUI) for managing serial communication with microcontroller units (MCUs) using Python and Tkinter.

## Features

- User-friendly interface for configuring serial communication parameters
- Real-time data visualization with dynamic charts
- Supports selection of:
  - COM ports
  - Baud rates
  - Byte sizes
  - Parity
  - Stop bits
  - Timeout
- Real-time validation of input parameters
- Connection management (connect/disconnect)
- Refresh functionality for COM ports
- Data streaming control (start/stop)
- Dynamic chart creation and removal
- Data saving functionality

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- pyserial (for serial communication)
- matplotlib (for data visualization)

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install pyserial matplotlib
   ```

## Usage

Run the `Master.py` file to start the application:
  ```bash
  python Master.py
  ```

## Classes

### RootGUI

Initializes the main application window.

### ComGUI

Manages the communication settings and interface. It includes:
- Dropdown menus for selecting communication parameters
- Connect/Disconnect button
- Refresh button for updating available COM ports

### DispGUI

Handles the display management interface, including:
- Start/Stop stream buttons
- New Chart/Kill Chart buttons
- Save Data button

### SerialCtrl

Manages serial communication, including:
- Port configuration
- Data reading and parsing
- JSON data saving

### DisplayCtrl

Controls data visualization, including:
- Chart creation and updating
- Real-time data streaming

## Data Handling

- Received data is parsed and stored in a JSON format
- Data is continuously updated and can be visualized in real-time
- The application supports two data streams: T1 and T2

Project Link: [https://github.com/tamertfn/gui-for-serials]
