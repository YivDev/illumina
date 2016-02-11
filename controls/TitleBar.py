from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from Button import SimpleButton
from TextLine import TextLine
import illumina
import wndMgr

class TitleBar(Window):
	BASE_PATH = "%s/controls/common/titlebar/" % illumina.BASE_PATH
	
	HEIGHT = 28
	MIN_WIDTH = 70

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__CreateUI()

		self.SetWidth(0)

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : ImageBox(),
			'CENTER' : ExpandedImageBox(),
			'RIGHT' : ImageBox()
		}

		self.__imgCloseButtonDecoration = None
		self.__btnClose = None
		self.__txtTitle = None

		for image in self.__dictImages.itervalues():
			image.SetParent(self)
			image.AddFlag("not_pick")
			image.Show()

		self.__dictImages['LEFT'].LoadImage("%s/left.tga" % TitleBar.BASE_PATH)
		self.__dictImages['CENTER'].LoadImage("%s/center.tga" % TitleBar.BASE_PATH)
		self.__dictImages['RIGHT'].LoadImage("%s/right.tga" % TitleBar.BASE_PATH)

	def UpdateGeneralUIPosition(self):
		self.__dictImages['LEFT'].SetPosition(0, TitleBar.HEIGHT - self.__dictImages['LEFT'].GetHeight())
		self.__dictImages['CENTER'].SetPosition(self.__dictImages['LEFT'].GetWidth(), TitleBar.HEIGHT - self.__dictImages['CENTER'].GetHeight())
		self.__dictImages['RIGHT'].SetPosition(self.GetWidth() - self.__dictImages['RIGHT'].GetWidth(), TitleBar.HEIGHT - self.__dictImages['RIGHT'].GetHeight())

		self.__dictImages['CENTER'].SetScale(float(self.GetWidth() - (self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth())) / float(self.__dictImages['CENTER'].GetWidth()), 1.0)

	def SetWidth(self, width):
		width = max(TitleBar.MIN_WIDTH, width)

		self.SetSize(width, TitleBar.HEIGHT)

		self.UpdateGeneralUIPosition()
		self.UpdateTitlePosition()
		self.UpdateCloseButtonAndDecorationPosition()

	## TITLE
	def SetTitle(self, title):
		if not self.__txtTitle:
			self.__txtTitle = TextLine()
			self.__txtTitle.SetParent(self)
			self.__txtTitle.SetPackedFontColor(0xFFE6D0A2)
			self.__txtTitle.SetHorizontalAlignCenter()
			self.__txtTitle.SetVerticalAlignBottom()
			self.__txtTitle.Show()

		self.__txtTitle.SetText(title)
		self.UpdateTitlePosition()

	def UpdateTitlePosition(self):
		if not self.__txtTitle:
			return

		self.__txtTitle.SetPosition(self.GetWidth() / 2, 17)

	## CLOSE BUTTON
	def AddCloseButton(self):
		self.__imgCloseButtonDecoration = ImageBox()
		self.__imgCloseButtonDecoration.SetParent(self)
		self.__imgCloseButtonDecoration.AddFlag("not_pick")
		self.__imgCloseButtonDecoration.LoadImage("%s/decoration_right.tga" % TitleBar.BASE_PATH)
		self.__imgCloseButtonDecoration.SetHorizontalAlign(wndMgr.HORIZONTAL_ALIGN_RIGHT)
		self.__imgCloseButtonDecoration.Show()

		self.__btnClose = SimpleButton()
		self.__btnClose.SetParent(self)
		self.__btnClose.SetUpVisual("%s/controls/common/button/board_close_01_normal.tga" % illumina.BASE_PATH)
		self.__btnClose.SetOverVisual("%s/controls/common/button/board_close_02_hover.tga" % illumina.BASE_PATH)
		self.__btnClose.SetDownVisual("%s/controls/common/button/board_close_03_active.tga" % illumina.BASE_PATH)
		self.__btnClose.SetHorizontalAlign(wndMgr.HORIZONTAL_ALIGN_RIGHT)
		self.__btnClose.Show()

		self.UpdateGeneralUIPosition()
		self.UpdateTitlePosition()
		self.UpdateCloseButtonAndDecorationPosition()

	def GetCloseButton(self):
		return self.__btnClose

	def HasCloseButton(self):
		return (self.__imgCloseButtonDecoration and self.__btnClose)
	
	def UpdateCloseButtonAndDecorationPosition(self):
		if not self.HasCloseButton():
			return

		self.__imgCloseButtonDecoration.SetPosition(self.__imgCloseButtonDecoration.GetWidth() - 13, -18)
		self.__btnClose.SetPosition(self.__btnClose.GetWidth() - 1, 0)


