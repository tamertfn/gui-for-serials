from GUI_Master import RootGUI, ComGUI
from Serial_Com_ctrl import SerialCtrl

SerialControl = SerialCtrl()
RootMaster = RootGUI()

ComMaster = ComGUI(RootMaster.root, SerialControl)

RootMaster.root.mainloop()