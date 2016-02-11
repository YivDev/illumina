from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from Button import SimpleButton, SimpleDragButton
from illumina.EventEnum import EventEnum
import illumina

class Slider(Window):
	BASE_PATH = "%s/controls/common/slider/" % illumina.BASE_PATH

	HEIGHT = 17
	MIN_WIDTH = 17

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__maxValue = 1
		self.__curValue = 0
		self.__doMove = False

		self.__CreateUI()

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
			image.LoadImage("%s/bg_%s.tga" % (self.BASE_PATH, position.lower()))
			image.Show()
		
		self.__imgRange = ExpandedImageBox()
		self.__imgRange.SetParent(self)
		self.__imgRange.SetPosition(4, self.GetHeight() / 2 - 1)
		self.__imgRange.LoadImage("%s/bg_range.tga" % Slider.BASE_PATH)
		self.__imgRange.Hide()

		self.__btnSlider = SimpleDragButton()
		self.__btnSlider.SetParent(self)
		self.__btnSlider.AddFlag("movable")
		self.__btnSlider.AddFlag("restrict_y")
		self.__btnSlider.SetPosition(0, 0)
		self.__btnSlider.SetUpVisual("%s/btn_01_normal.tga" % Slider.BASE_PATH)
		self.__btnSlider.SetOverVisual("%s/btn_02_hover.tga" % Slider.BASE_PATH)
		self.__btnSlider.SetDownVisual("%s/btn_01_normal.tga" % Slider.BASE_PATH)
		self.__btnSlider.Show()

		self.__dictImages['LEFT'].SetPosition(0, 6)
		self.__dictImages['CENTER'].SetPosition(3, 6)

		self.__btnSlider.AddEventListener(SimpleDragButton.Events.ON_MOVE, self.__OnMove)

	def __OnMove(self):
		self.__doMove = not self.__doMove
		if not self.__doMove:
			return

		oldValue = self.__curValue

		slideWidth = self.GetWidth() - self.__btnSlider.GetWidth()
		step = float(slideWidth) / float(self.__maxValue)

		self.__curValue = int(round(self.__btnSlider.GetLocalX() / step))
		
		self.__btnSlider.SetPosition(self.__curValue * step, 0)
		self.UpdateRangeEffect()
			
		if oldValue != self.__curValue:
			self.CallEventListener(Slider.Events.ON_SLIDE, self.__curValue)

	def SetWidth(self, width):
		width = max(Slider.MIN_WIDTH, width)

		Window.SetSize(self, width, Slider.HEIGHT)

		self.__dictImages['CENTER'].SetScale(float(width - (self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth())), 1.0)
		self.__dictImages['RIGHT'].SetPosition(width - self.__dictImages['RIGHT'].GetWidth(), 6)

		self.__btnSlider.SetRestrictMovementArea(0, 0, self.GetWidth(), 0)
		self.__imgRange.SetPosition(2, self.GetHeight() / 2 - 1)

	def SetMaxValue(self, maxValue):
		self.__maxValue = min(max(1, maxValue), self.GetWidth() - self.__btnSlider.GetWidth())
		self.__OnMove()

	## Range Effect
	def GetRangeEffect(self):
		return self.__imgRange

	def UpdateRangeEffect(self):
		self.__imgRange.SetScale(float(self.__btnSlider.GetLocalX() + self.__btnSlider.GetWidth() / 2 - self.__imgRange.GetLocalX()), 1.0)

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_SLIDE = EventEnum()

	def __OnSlide(self, value):
		self.CallEventListener(Slider.Events.ON_SLIDE, value)

