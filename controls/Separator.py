from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
import illumina

class VerticalSeparator(Window):
	BASE_PATH = "%s/controls/common/separator/" % illumina.BASE_PATH

	HEIGHTS = {
		'TOP' : 6,
		'CENTER' : 1,
		'BOTTOM' : 6
	}

	WIDTH = 11

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__CreateUI()
		self.SetHeight(0)

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'TOP' : ImageBox(),
			'CENTER' : ExpandedImageBox(),
			'BOTTOM' : ImageBox()
		}

		for image in self.__dictImages.itervalues():
			image.SetParent(self)
			image.Show()
			
		self.__dictImages['TOP'].LoadImage("%s/vertical_top.tga" % VerticalSeparator.BASE_PATH)
		self.__dictImages['CENTER'].LoadImage("%s/vertical_center.tga" % VerticalSeparator.BASE_PATH)
		self.__dictImages['BOTTOM'].LoadImage("%s/vertical_bottom.tga" % VerticalSeparator.BASE_PATH)

		self.__dictImages['TOP'].SetPosition(0, 0)
		self.__dictImages['CENTER'].SetPosition(0, VerticalSeparator.HEIGHTS['TOP'])
		
	def SetHeight(self, height):
		height = max(VerticalSeparator.HEIGHTS['TOP'] + VerticalSeparator.HEIGHTS['BOTTOM'], height)

		self.SetSize(VerticalSeparator.WIDTH, height)
		
		self.__dictImages['CENTER'].SetScale(1.0, float(height - (VerticalSeparator.HEIGHTS['TOP'] + VerticalSeparator.HEIGHTS['BOTTOM'])) / float(VerticalSeparator.HEIGHTS['CENTER']))
		self.__dictImages['BOTTOM'].SetPosition(0, height - VerticalSeparator.HEIGHTS['BOTTOM'])


class HorizontalSeparator(Window):
	BASE_PATH = "%s/controls/common/separator/" % illumina.BASE_PATH

	WIDTHS = {
		'LEFT' : 6,
		'CENTER' : 1,
		'RIGHT' : 6
	}

	HEIGHT = 11

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

		for image in self.__dictImages.itervalues():
			image.SetParent(self)
			image.Show()
			
		self.__dictImages['LEFT'].LoadImage("%s/horizontal_left.tga" % HorizontalSeparator.BASE_PATH)
		self.__dictImages['CENTER'].LoadImage("%s/horizontal_center.tga" % HorizontalSeparator.BASE_PATH)
		self.__dictImages['RIGHT'].LoadImage("%s/horizontal_right.tga" % HorizontalSeparator.BASE_PATH)

		self.__dictImages['LEFT'].SetPosition(0, 0)
		self.__dictImages['CENTER'].SetPosition(HorizontalSeparator.WIDTHS['LEFT'], 0)
	
	def SetWidth(self, width):
		width = max(HorizontalSeparator.WIDTHS['LEFT'] + HorizontalSeparator.WIDTHS['RIGHT'], width)

		self.SetSize(width, HorizontalSeparator.HEIGHT)
		
		self.__dictImages['CENTER'].SetScale(float(width - (HorizontalSeparator.WIDTHS['LEFT'] + HorizontalSeparator.WIDTHS['RIGHT'])) / float(HorizontalSeparator.WIDTHS['CENTER']), 1.0)
		self.__dictImages['RIGHT'].SetPosition(width - HorizontalSeparator.WIDTHS['RIGHT'], 0)

