# Serial Communication GUI

This project provides a graphical user interface (GUI) for managing serial communication with microcontroller units (MCUs) using Python and Tkinter.

## Features

- User-friendly interface for configuring serial communication parameters
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

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- pyserial (for serial communication)

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:
   pip install pyserial

## Usage

Run the `Master.py` file to start the application:
  python Master.py

## Classes

### RootGUI

Initializes the main application window.

### ComGUI

Manages the communication settings and interface. It includes:
- Dropdown menus for selecting communication parameters
- Connect/Disconnect button
- Refresh button for updating available COM ports

Project Link: [https://github.com/tamertfn/gui-for-serials]
