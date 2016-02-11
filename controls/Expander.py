from Window import Window
from illumina.EventEnum import EventEnum
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from TextLine import TextLine
import illumina
import wndMgr

class ExpanderState(object):
	COLLAPSED = 0
	EXPANDED = 1

class Expander(Window):
	BASE_PATH = "%s/controls/common/expander/" % illumina.BASE_PATH

	IMAGES = {
		'LEFT' : {
			ExpanderState.COLLAPSED : "left_01_normal.tga",
			ExpanderState.EXPANDED : "left_02_hover.tga"
		},
		'CENTER' : {
			ExpanderState.COLLAPSED : "center_01_normal.tga",
			ExpanderState.EXPANDED : "center_02_hover.tga"
		},
		'RIGHT' : {
			ExpanderState.COLLAPSED : "right_01_normal.tga",
			ExpanderState.EXPANDED : "right_02_hover.tga"
		}
	}

	MIN_WIDTH = 30
	HEIGHT = 30

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__state = ExpanderState.COLLAPSED
		self.__arrowRotation = 0.0
		
		self.__CreateUI()
		self.__SetEventListeners()

		self.SetWidth(0)
		self.SetState(ExpanderState.COLLAPSED)

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : {
				ExpanderState.EXPANDED : ImageBox(),
				ExpanderState.COLLAPSED : ImageBox()
			},
			'CENTER' : {
				ExpanderState.EXPANDED : ExpandedImageBox(),
				ExpanderState.COLLAPSED : ExpandedImageBox()
			},
			'RIGHT' : {
				ExpanderState.EXPANDED : ImageBox(),
				ExpanderState.COLLAPSED : ImageBox()
			}
		}

		self.__txtText = None

		for position, imageDictByState in self.__dictImages.iteritems():
			for state, image in imageDictByState.iteritems():
				image.SetParent(self)
				image.AddFlag("not_pick")
				image.LoadImage("%s/%s" % (Expander.BASE_PATH, Expander.IMAGES[position][state]))
				image.Hide()

		self.__imgArrowBackground = ImageBox()
		self.__imgArrowBackground.SetParent(self)
		self.__imgArrowBackground.AddFlag("not_pick")
		self.__imgArrowBackground.SetPosition(0, 0)
		self.__imgArrowBackground.LoadImage("%s/arrow_bg.tga" % Expander.BASE_PATH)
		self.__imgArrowBackground.Show()

		self.__imgArrow = ExpandedImageBox()
		self.__imgArrow.SetParent(self.__imgArrowBackground)
		self.__imgArrow.AddFlag("not_pick")
		self.__imgArrow.SetPosition(0, 0)
		self.__imgArrow.LoadImage("%s/arrow.tga" % Expander.BASE_PATH)
		self.__imgArrow.SetHorizontalAlign(wndMgr.HORIZONTAL_ALIGN_CENTER)
		self.__imgArrow.SetVerticalAlign(wndMgr.VERTICAL_ALIGN_CENTER)
		self.__imgArrow.Show()

	
	def __SetEventListeners(self):
		self.AddEventListener(Expander.Events.ON_MOUSE_OVER_IN, lambda : self.__RefreshButton(ExpanderState.EXPANDED))
		self.AddEventListener(Expander.Events.ON_MOUSE_OVER_OUT, lambda : self.__RefreshButton(ExpanderState.COLLAPSED))
		self.AddEventListener(Expander.Events.ON_MOUSE_LEFT_BUTTON_UP, lambda : self.SetState(ExpanderState.EXPANDED if self.GetState() == ExpanderState.COLLAPSED else ExpanderState.COLLAPSED))

	def __RefreshButton(self, expandingState):
		for position, imageDictByState in self.__dictImages.iteritems():
			for state, image in imageDictByState.iteritems():
				if state != expandingState:
					image.Hide()
				else:
					image.Show()

		if self.GetState() == ExpanderState.COLLAPSED:
			self.__imgArrow.SetRotation(self.__arrowRotation)
		else:
			self.__imgArrow.SetRotation(180.0 + self.__arrowRotation)
	
	def GetState(self):
		return self.__state

	def SetState(self, state):
		self.__state = state
		self.__RefreshButton(self.__state)

	def SetWidth(self, width):
		width = max(Expander.MIN_WIDTH, width)

		self.SetSize(width, Expander.HEIGHT)

		for image in self.__dictImages['CENTER'].itervalues():
			image.SetPosition(5, 0)
			image.SetScale(float(width - 10), 1.0)

		for image in self.__dictImages['RIGHT'].itervalues():
			image.SetPosition(width - 5, 0)

		self.UpdateText()

	def SetArrowRotation(self, rotation):
		self.__arrowRotation = rotation
		self.__imgArrow.SetRotation(rotation)
	
	## Text
	def SetText(self, text):
		if not self.__txtText:
			self.__txtText = TextLine()
			self.__txtText.SetParent(self)
			self.__txtText.AddFlag("not_pick")
			self.__txtText.SetVerticalAlignCenter()
			self.__txtText.SetPackedFontColor(0xFFE6D0A2)
			self.__txtText.Show()

			self.UpdateText()

		self.__txtText.SetText(text)

	def GetText(self):
		if not self.__txtText:
			return ""
		
		return self.__txtText.GetText()

	def UpdateText(self):
		if not self.__txtText:
			return

		self.__txtText.SetPosition(35, self.GetHeight() / 2 - 2)

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_EXPAND = EventEnum()
		ON_COLLAPSE = EventEnum()

