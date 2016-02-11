from Window import Window

class Line(Window):
	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterLine(self, layer))
	
	def SetColor(self, color):
		wndMgr.SetColor(self.GetWindowHandle(), color)

