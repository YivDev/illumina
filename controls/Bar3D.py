from Window import Window

class Bar3D(Window):
	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterBar3D(self, layer))
	
	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.GetWindowHandle(), left, right, center)

