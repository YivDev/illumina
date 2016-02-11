from Window import Window
import wndMgr
from illumina.EventEnum import EventEnum

class AnimatedImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterAniImageBox(self, layer))

	def AppendImage(self, imageName):
		wndMgr.AppendImage(self.GetWindowHandle(), imageName)

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.GetWindowHandle(), delay)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.GetWindowHandle(), left, top, right, bottom)

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_END_FRAME = EventEnum()

	def OnEndFrame(self):
		self.CallEventListener(AnimatedImageBox.Events.ON_END_FRAME)
