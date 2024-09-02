# This is the main entry point of the Serial Communication GUI application.
# It initializes the main components (SerialCtrl, RootGUI, DisplayCtrl, ComGUI)
# and starts the main event loop.

from GUI_Master import RootGUI, ComGUI
from Serial_Com_ctrl import SerialCtrl
from Display_ctrl import DisplayCtrl

SerialControl = SerialCtrl()
RootMaster = RootGUI()
DisplayControl = DisplayCtrl()

ComMaster = ComGUI(RootMaster.root, SerialControl, DisplayControl)

RootMaster.root.mainloop()