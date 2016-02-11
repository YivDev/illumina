from Window import Window
import wndMgr

class Bar(Window):
	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterBar(self, layer))
	
	def SetColor(self, color):
		wndMgr.SetColor(self.GetWindowHandle(), color)

