from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from Button import SimpleButton, SimpleDragButton
from illumina.EventEnum import EventEnum
import illumina

class RangeSlider(Window):
	BASE_PATH = "%s/controls/common/range/" % illumina.BASE_PATH

	HEIGHT = 17
	MIN_WIDTH = 17

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__maxValue = 1
		self.__curValues = []
		self.__rangeSliderWidth = 0
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
		self.__imgRange.AddFlag("not_pick")
		self.__imgRange.LoadImage("%s/bg_range.tga" % self.BASE_PATH)
		self.__imgRange.Show()

		self.__liRangeSlider = [SimpleDragButton() for obj in xrange(2)]
		for rangeSlider in self.__liRangeSlider:
			rangeSlider.SetParent(self)
			rangeSlider.AddFlag("movable")
			rangeSlider.AddFlag("restrict_y")
			rangeSlider.SetPosition(0, 0)
			rangeSlider.SetUpVisual("%s/btn_01_normal.tga" % RangeSlider.BASE_PATH)
			rangeSlider.SetOverVisual("%s/btn_02_hover.tga" % RangeSlider.BASE_PATH)
			rangeSlider.SetDownVisual("%s/btn_01_normal.tga" % RangeSlider.BASE_PATH)
			rangeSlider.Show()
			self.__curValues.append(0)
			self.__rangeSliderWidth = rangeSlider.GetWidth()
			
		self.__liRangeSlider[0].AddEventListener(SimpleDragButton.Events.ON_MOVE, lambda : self.__OnMove(self.__liRangeSlider[0], 0))
		self.__liRangeSlider[1].AddEventListener(SimpleDragButton.Events.ON_MOVE, lambda : self.__OnMove(self.__liRangeSlider[1], 1))

		self.__dictImages['LEFT'].SetPosition(0, 6)
		self.__dictImages['CENTER'].SetPosition(3, 6)

	def __GetStep(self):
		return float(self.GetWidth() - self.__rangeSliderWidth) / float(self.__maxValue)

	def __OnMove(self, rangeSlider, rangeSliderIndex):
		self.__doMove = not self.__doMove
		if not self.__doMove:
			return

		step = self.__GetStep()

		curValue = int(round(rangeSlider.GetLocalX() / step))
		
		rangeSlider.SetPosition(curValue * step, 0)

		self.__curValues[rangeSliderIndex] = curValue

		self.UpdateRange()

		import dbg
		dbg.TraceError("%d (%d, %d)" % (self.GetValue(), self.GetValue(0), self.GetValue(1)))

	def GetValue(self, index = -1):
		if index < 0 or index >= len(self.__curValues):
			return max(self.__curValues) - min(self.__curValues)
		else:
			return self.__curValues[index]

	def SetValue(self, index, value):
		if index < 0 or index >= len(self.__curValues) or index >= len(self.__liRangeSlider):
			return
		
		self.__curValues[index] = value
		self.__liRangeSlider[index].SetPosition(self.__GetStep() * value, 0)
		self.UpdateRange()

	def UpdateRange(self):
		startX = min(self.__liRangeSlider[0].GetLocalX(), self.__liRangeSlider[1].GetLocalX())
		endX = max(self.__liRangeSlider[0].GetLocalX(), self.__liRangeSlider[1].GetLocalX())

		self.__imgRange.SetPosition(startX + self.__liRangeSlider[0].GetWidth() / 2, self.GetHeight() / 2 - 1)
		self.__imgRange.SetScale(float(endX - startX), 1.0)
		self.__imgRange.SetTop()

	def SetWidth(self, width):
		width = max(RangeSlider.MIN_WIDTH, width)

		Window.SetSize(self, width, RangeSlider.HEIGHT)

		self.__dictImages['CENTER'].SetScale(float(width - (self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth())), 1.0)
		self.__dictImages['RIGHT'].SetPosition(width - self.__dictImages['RIGHT'].GetWidth(), 6)

		self.__liRangeSlider[0].SetPosition(0, 0)
		self.__liRangeSlider[1].SetPosition(width - self.__liRangeSlider[1].GetWidth(), 0)
		for rangeSlider in self.__liRangeSlider:
			rangeSlider.SetRestrictMovementArea(0, 0, self.GetWidth(), 0)

		self.UpdateRange()

	def SetMaxValue(self, maxValue):
		self.__maxValue = maxValue#min(max(1, maxValue), self.GetWidth() - self.__btnSlider.GetWidth())
		#self.__OnMove()

	##################################################
	## EVENTS

	class Events(Window.Events):
		pass

