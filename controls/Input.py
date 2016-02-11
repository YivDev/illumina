from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from TextLine import TextLine
from EditLine import EditLine
import illumina
import wndMgr

class _BaseInput(Window):
	BASE_PATH = "%s/controls/common/input/" % illumina.BASE_PATH

	FILE_NAME_PREFIX = ""

	MIN_WIDTH = 0
	HEIGHT = 0

	TEXT_PADDING = (3, 3)
	TEXT_COLOR = 0xffffffff

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__CreateUI()

		self.AddEventListener(Window.Events.ON_SET_FOCUS, self.__OnSetFocus)

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : ImageBox(),
			'CENTER' : ExpandedImageBox(),
			'RIGHT' : ImageBox()
		}

		for position, image in self.__dictImages.iteritems():
			image.SetParent(self)
			image.AddFlag("not_pick")
			image.LoadImage("%s/%s_%s.tga" % (self.BASE_PATH, self.FILE_NAME_PREFIX, position.lower()))
			image.Show()

		self.__dictImages['CENTER'].SetPosition(self.__dictImages['LEFT'].GetWidth(), 0)

		self.__txtInput = None
		self.__textAlign = _BaseInput.TextAlign.LEFT

	def SetWidth(self, width):
		width = max(self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth(), width)

		Window.SetSize(self, width, self.HEIGHT)

		self.__dictImages['CENTER'].SetScale((width - (self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth())) / self.__dictImages['CENTER'].GetWidth(), 1.0)
		self.__dictImages['RIGHT'].SetPosition(width - self.__dictImages['RIGHT'].GetWidth(), 0)

		if self.__txtInput:
			self.__txtInput.SetSize(self.GetWidth() - self.TEXT_PADDING[0], self.GetHeight() - self.TEXT_PADDING[1])
			self.ArrangeText()

	def __OnSetFocus(self):
		if not self.__txtInput:
			return
		
		self.__txtInput.SetFocus()

	## TEXT
	def SetTextInstance(self, allowEdit = True):
		if self.__txtInput:
			self.DeleteTextInstance()

		if allowEdit:
			self.__txtInput = EditLine()
		else:
			self.__txtInput = TextLine()
		self.__txtInput.SetParent(self)
		self.__txtInput.SetSize(self.GetWidth() - self.TEXT_PADDING[0] * 2, self.GetHeight() - self.TEXT_PADDING[1] * 2)
		self.__txtInput.SetPackedFontColor(self.TEXT_COLOR)
		self.__txtInput.Show()

		self.ArrangeText()

	def DeleteTextInstance(self):
		if not self.__txtInput:
			return
		
		self.__txtInput.Hide()
		del self.__txtInput

	def GetTextInstance(self):
		return self.__txtInput
	
	class TextAlign:
		LEFT = 0
		CENTER = 1
		RIGHT = 2

	def SetTextAlign(self, align):
		self.__textAlign = align

		self.ArrangeText()

	def ArrangeText(self):
		if not self.__txtInput:
			return

		if self.__textAlign == _BaseInput.TextAlign.LEFT:
			self.__txtInput.SetPosition(self.TEXT_PADDING[0], self.TEXT_PADDING[1])
			self.__txtInput.SetHorizontalAlignLeft()
		elif self.__textAlign == _BaseInput.TextAlign.CENTER:
			self.__txtInput.SetPosition(self.GetWidth() / 2, self.TEXT_PADDING[1])
			self.__txtInput.SetHorizontalAlignCenter()
		elif self.__textAlign == _BaseInput.TextAlign.RIGHT:
			self.__txtInput.SetPosition(self.GetWidth() - self.TEXT_PADDING[0], self.TEXT_PADDING[1])
			self.__txtInput.SetHorizontalAlignRight()

class BoardInput(_BaseInput):
	FILE_NAME_PREFIX = "board"

	MIN_WIDTH = 12
	HEIGHT = 27

	TEXT_PADDING = (6, 6)
	TEXT_COLOR = 0xFFA07970

class ThinBoardInput(_BaseInput):
	FILE_NAME_PREFIX = "thinboard"

	MIN_WIDTH = 10
	HEIGHT = 25

	TEXT_PADDING = (6, 6)
	TEXT_COLOR = 0xFF9B8D8B

class YangInput(_BaseInput):
	FILE_NAME_PREFIX = "yang"

	MIN_WIDTH = 12
	HEIGHT = 27

	TEXT_PADDING = (6, 6)
	TEXT_COLOR = 0xFFF1EC99

