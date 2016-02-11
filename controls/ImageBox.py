from Window import Window
import wndMgr
import dbg
class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterImageBox(self, layer))

	def LoadImage(self, imageName):
		wndMgr.LoadImage(self.GetWindowHandle(), imageName)

	def SetAlpha(self, alpha):
		self.SetDiffuseColor(1.0, 1.0, 1.0, alpha)

	def SetDiffuseColor(self, red, green, blue, alpha):
		wndMgr.SetDiffuseColor(self.GetWindowHandle(), red, green, blue, alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.GetWindowHandle())

	def GetHeight(self):
		return wndMgr.GetHeight(self.GetWindowHandle())

