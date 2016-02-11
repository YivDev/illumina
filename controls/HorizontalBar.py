from ExpandedImageBox import ExpandedImageBox
from TextLine import TextLine
import illumina

class HorizontalBar(ExpandedImageBox):
	BASE_PATH = "%s/controls/common/horizontal_bar/" % illumina.BASE_PATH
	
	WIDTH = 208
	HEIGHT = 32

	def __init__(self, layer = "UI"):
		ExpandedImageBox.__init__(self, layer)

		self.__width = 0

		self.__CreateUI()
		self.SetWidth(HorizontalBar.WIDTH)

	def __del__(self):
		ExpandedImageBox.__del__(self)

	def __CreateUI(self):
		self.__txtTitle = None

		self.LoadImage("%s/center.tga" % HorizontalBar.BASE_PATH)
		self.Show()

	def SetWidth(self, width):
		self.__width = width

		self.SetScale(float(width) / float(HorizontalBar.WIDTH), 1.0)

		self.UpdateTitle()

	## Title
	def SetTitle(self, title):
		if not self.__txtTitle:
			self.__txtTitle = TextLine()
			self.__txtTitle.SetParent(self)
			self.__txtTitle.SetPackedFontColor(0xFFCAA76F)
			self.__txtTitle.SetHorizontalAlignCenter()
			self.__txtTitle.Show()

		self.__txtTitle.SetText(title)
		self.UpdateTitle()

	def UpdateTitle(self):
		if not self.__txtTitle:
			return
		
		self.__txtTitle.SetPosition(self.__width / 2, 5)
