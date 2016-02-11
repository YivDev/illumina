from Window import Window
from illumina.EventEnum import EventEnum
import illumina
import wndMgr

class CheckBox(Window):
	BASE_PATH = "%s/controls/common/checkbox/" % illumina.BASE_PATH

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.SetChecked(False, True)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterButton(self, layer))

	def SetChecked(self, checked, noBroadcast = False):
		self.__isChecked = checked

		stateName = ({True : "filled", False : "empty"})[self.IsChecked()]
		wndMgr.SetUpVisual(self.GetWindowHandle(), "%s/%s_01_normal.tga" % (CheckBox.BASE_PATH, stateName))
		wndMgr.SetOverVisual(self.GetWindowHandle(), "%s/%s_02_hover.tga" % (CheckBox.BASE_PATH, stateName))
		wndMgr.SetDownVisual(self.GetWindowHandle(), "%s/%s_03_active.tga" % (CheckBox.BASE_PATH, stateName))
		wndMgr.SetDisableVisual(self.GetWindowHandle(), "%s/%s_01_normal.tga" % (CheckBox.BASE_PATH, stateName))
		
		if not noBroadcast:
			if self.IsChecked():
				self.CallEventListener(CheckBox.Events.ON_CHECK)
			else:
				self.CallEventListener(CheckBox.Events.ON_UNCHECK)

	def IsChecked(self):
		return self.__isChecked

	def Enable(self):
		wndMgr.Enable(self.GetWindowHandle())

	def Disable(self):
		wndMgr.Disable(self.GetWindowHandle())

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_CHECK = EventEnum()
		ON_UNCHECK = EventEnum()

	def CallEvent(self):
		self.SetChecked(not self.IsChecked())

