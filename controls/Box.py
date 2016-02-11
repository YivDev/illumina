from Window import Window

class Box(Window):
	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterBox(self, layer))
	
	def SetColor(self, color):
		wndMgr.SetColor(self.GetWindowHandle(), color)

