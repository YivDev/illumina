from Window import Window
import wndMgr

class TextLine(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.SetFontName("Tahoma:12") # TODO

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterTextLine(self, layer))

	def SetMax(self, max):
		wndMgr.SetMax(self.GetWindowHandle(), max)

	def SetLimitWidth(self, limitWidth):
		wndMgr.SetLimitWidth(self.GetWindowHandle(), limitWidth)

	def SetMultiLine(self, multiLine = True):
		wndMgr.SetMultiLine(self.GetWindowHandle(), multiLine)

	def SetHorizontalAlignArabic(self):
		wndMgr.SetHorizontalAlign(self.GetWindowHandle(), wndMgr.TEXT_HORIZONTAL_ALIGN_ARABIC)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.GetWindowHandle(), wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.GetWindowHandle(), wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.GetWindowHandle(), wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.GetWindowHandle(), wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.GetWindowHandle(), wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.GetWindowHandle(), wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, secret = True):
		wndMgr.SetSecret(self.GetWindowHandle(), secret)

	def SetOutline(self, outline = True):
		wndMgr.SetOutline(self.GetWindowHandle(), outline)

	def SetFeather(self, feather = True):
		wndMgr.SetFeather(self.GetWindowHandle(), feather)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.GetWindowHandle(), fontName)

	def SetPackedFontColor(self, hexColor):
		wndMgr.SetFontColor(self.GetWindowHandle(), hexColor)

	def SetFontColor(self, red, green, blue):
		wndMgr.SetFontColor(self.GetWindowHandle(), red, green, blue)

	def SetText(self, text):
		wndMgr.SetText(self.GetWindowHandle(), text)

	def GetText(self):
		return wndMgr.GetText(self.GetWindowHandle())

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.GetWindowHandle())
