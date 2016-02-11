from ImageBox import ImageBox
import wndMgr

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)

	def __del__(self):
		ImageBox.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterExpandedImageBox(self, layer))

	def SetScale(self, x, y):
		wndMgr.SetScale(self.GetWindowHandle(), x, y)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.GetWindowHandle(), x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.GetWindowHandle(), rotation)

	def SetRenderingMode(self, renderingMode):
		wndMgr.SetRenderingMode(self.GetWindowHandle(), renderingMode)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.GetWindowHandle(), left, top, right, bottom)
