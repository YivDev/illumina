from Window import Window
from illumina.EventEnum import EventEnum
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from TextLine import TextLine
import wndMgr
import snd
import illumina
import dbg

class SimpleButton(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterButton(self, layer))

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.GetWindowHandle(), filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.GetWindowHandle(), filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.GetWindowHandle(), filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.GetWindowHandle(), filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.GetWindowHandle())
	
	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.GetWindowHandle())
	
	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.GetWindowHandle())

	def Flash(self):
		wndMgr.Flash(self.GetWindowHandle())

	def Enable(self):
		wndMgr.Enable(self.GetWindowHandle())

	def Disable(self):
		wndMgr.Disable(self.GetWindowHandle())

	def SetDown(self):
		wndMgr.Down(self.GetWindowHandle())

	def SetUp(self):
		wndMgr.SetUp(self.GetWindowHandle())

	def IsDown(self):
		return wndMgr.IsDown(self.GetWindowHandle())

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_CALL = EventEnum()
	#	ON_DOWN = EventEnum()

		ON_SHOW_TOOL_TIP = EventEnum()
		ON_HIDE_TOOL_TIP = EventEnum()

	def CallEvent(self):
		self.CallEventListener(SimpleButton.Events.ON_CALL)
	
	# There is no need for the event because ON_CALL is called at the same time
	#def DownEvent(self):
	#	self.CallEventListener(SimpleButton.Events.ON_DOWN)

	def ShowToolTip(self):
		self.CallEventListener(SimpleButton.Events.ON_SHOW_TOOL_TIP)

	def HideToolTip(self):
		self.CallEventListener(SimpleButton.Events.ON_HIDE_TOOL_TIP)

class SimpleRadioButton(SimpleButton):
	def __init__(self, layer = "UI"):
		SimpleButton.__init__(self, layer)

	def __del__(self):
		SimpleButton.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterRadioButton(self, layer))

	##################################################
	## EVENTS

	class Events(SimpleButton.Events):
		pass

class SimpleToggleButton(SimpleButton):
	def __init__(self, layer = "UI"):
		SimpleButton.__init__(self, layer)

		self.__isToggled = False
		
		self.AddEventListener(SimpleToggleButton.Events.ON_TOGGLE_UP, lambda : self.__SetToggled(False))
		self.AddEventListener(SimpleToggleButton.Events.ON_TOGGLE_DOWN, lambda : self.__SetToggled(True))

	def __del__(self):
		SimpleButton.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterToggleButton(self, layer))
	
	def __SetToggled(self, isToggled):
		self.__isToggled = isToggled

	def IsToggled(self):
		return self.__isToggled

	##################################################
	## EVENTS

	class Events(SimpleButton.Events):
		ON_TOGGLE_UP = EventEnum()
		ON_TOGGLE_DOWN = EventEnum()

	def OnToggleUp(self):
		self.CallEventListener(SimpleToggleButton.Events.ON_TOGGLE_UP)

	def OnToggleDown(self):
		self.CallEventListener(SimpleToggleButton.Events.ON_TOGGLE_DOWN)

class SimpleDragButton(SimpleButton):
	def __init__(self, layer = "UI"):
		SimpleButton.__init__(self, layer)

	def __del__(self):
		SimpleButton.__del__(self)

	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.RegisterDragButton(self, layer))

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.GetWindowHandle(), x, y, width, height)

	##################################################
	## EVENTS

	class Events(SimpleButton.Events):
		ON_MOVE = EventEnum()

	def OnMove(self):
		self.CallEventListener(SimpleDragButton.Events.ON_MOVE)
		
class _ButtonState(object):
	NORMAL = 0
	HOVER = 1
	ACTIVE = 2
	DISABLED = 3

class _BaseButton(Window):
	class WidthType(object):
		STRETCH = 0
		REPEAT = 1

	BASE_PATH = "%s/controls/common/button/" % illumina.BASE_PATH

	IMAGES = None

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 1.0
	}

	WIDTH = None
	HEIGHT = None

	WIDTH_TYPE = None

	TEXT_COLOR = None

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__state = _ButtonState.NORMAL

		self.__CreateUI()
		self._SetEventListeners()

		self.SetWidth(0)
		self.SetState(_ButtonState.NORMAL)

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : {
				_ButtonState.NORMAL : ImageBox(),
				_ButtonState.HOVER : ImageBox(),
				_ButtonState.ACTIVE : ImageBox(),
				_ButtonState.DISABLED : ImageBox()
			},
			'CENTER' : {
				_ButtonState.NORMAL : ExpandedImageBox(),
				_ButtonState.HOVER : ExpandedImageBox(),
				_ButtonState.ACTIVE : ExpandedImageBox(),
				_ButtonState.DISABLED : ExpandedImageBox()
			},
			'RIGHT' : {
				_ButtonState.NORMAL : ImageBox(),
				_ButtonState.HOVER : ImageBox(),
				_ButtonState.ACTIVE : ImageBox(),
				_ButtonState.DISABLED : ImageBox()
			}
		}

		self.__txtText = None

		for position, imageDictByState in self.__dictImages.iteritems():
			for state, image in imageDictByState.iteritems():
				image.SetParent(self)
				image.AddFlag("not_pick")
				image.LoadImage(self.IMAGES[position][state])
				image.Hide()
	
	def _SetEventListeners(self):
		self.AddEventListener(_BaseButton.Events.ON_MOUSE_OVER_IN, lambda state=_ButtonState.HOVER: self.SetState(state, True))
		self.AddEventListener(_BaseButton.Events.ON_MOUSE_OVER_OUT, lambda state=_ButtonState.NORMAL: self.SetState(state, True))
		self.AddEventListener(_BaseButton.Events.ON_MOUSE_LEFT_BUTTON_DOWN, lambda state=_ButtonState.ACTIVE: self.SetState(state, True))
		self.AddEventListener(_BaseButton.Events.ON_MOUSE_LEFT_BUTTON_UP, self.OnClick)
		self.AddEventListener(_BaseButton.Events.ON_CLICK, lambda state=-1: self.SetState(state, True))

	def __RefreshButton(self):
		for position, imageDictByState in self.__dictImages.iteritems():
			for state, image in imageDictByState.iteritems():
				if state != self.GetState():
					image.Hide()
				else:
					image.SetAlpha(self.OPACITY[self.GetState()])
					image.Show()

		self.UpdateTextColor()
	
	def GetState(self):
		return self.__state

	def SetState(self, state, byEvent = False):
		if byEvent and self.IsDisabled():
			return

		callEnableEvent = self.GetState() == _ButtonState.DISABLED

		self.__state = state
		if self.GetState() < _ButtonState.NORMAL or self.GetState() > _ButtonState.DISABLED:
			if self.IsIn():
				self.__state = _ButtonState.HOVER
			else:
				self.__state = _ButtonState.NORMAL

		self.__RefreshButton()

		if callEnableEvent:
			self.CallEventListener(_BaseButton.Events.ON_ENABLE)
		elif self.IsDisabled():
			self.CallEventListener(_BaseButton.Events.ON_DISABLE)

	def SetEnabled(self, enabled = True):
		if enabled and self.IsDisabled():
			self.SetState(_ButtonState.NORMAL)
		elif not enabled and not self.IsDisabled():
			self.SetState(_ButtonState.DISABLED)

	def IsDisabled(self):
		return self.GetState() == _ButtonState.DISABLED

	def SetWidth(self, width):
		width = max(self.WIDTH['LEFT'] + self.WIDTH['RIGHT'], width)

		self.SetSize(width, self.HEIGHT)

		for image in self.__dictImages['CENTER'].itervalues():
			image.SetPosition(self.WIDTH['LEFT'], 0)
			rect = float(width - (self.WIDTH['LEFT'] + self.WIDTH['RIGHT'])) / float(self.WIDTH['CENTER'])
			if self.WIDTH_TYPE == _BaseButton.WidthType.STRETCH:
				image.SetScale(rect, 1.0)
			else:
				image.SetRenderingRect(0.0, 0.0, -1.0 + rect, 0.0)

		for image in self.__dictImages['RIGHT'].itervalues():
			image.SetPosition(width - self.WIDTH['RIGHT'], 0)

		self.UpdateText()

	## Text
	def SetText(self, text):
		if not self.__txtText:
			self.__txtText = TextLine()
			self.__txtText.SetParent(self)
			self.__txtText.AddFlag("not_pick")
			self.__txtText.SetHorizontalAlignCenter()
			self.__txtText.SetVerticalAlignCenter()
			self.__txtText.Show()

			self.UpdateText()
			self.UpdateTextColor()

		self.__txtText.SetText(text)

	def GetText(self):
		if not self.__txtText:
			return ""
		
		return self.__txtText.GetText()

	def UpdateText(self):
		if not self.__txtText:
			return

		self.__txtText.SetPosition(self.GetWidth() / 2, self.GetHeight() / 2 - 2)

	def UpdateTextColor(self):
		if not self.__txtText:
			return

		self.__txtText.SetPackedFontColor(self.TEXT_COLOR[self.GetState()])

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_CLICK = EventEnum()

		ON_DISABLE = EventEnum()
		ON_ENABLE = EventEnum()

	def OnClick(self):
		if self.IsDisabled():
			return

		self.CallEventListener(_BaseButton.Events.ON_CLICK)

class _BaseToggleButton(_BaseButton):
	def __init__(self, layer = "UI"):
		_BaseButton.__init__(self, layer)

		self.__isToggled = False

	def __del__(self):
		_BaseButton.__del__(self)

	def _SetEventListeners(self):
		self.AddEventListener(_BaseToggleButton.Events.ON_MOUSE_OVER_IN, self.__OnMouseOverIn)
		self.AddEventListener(_BaseToggleButton.Events.ON_MOUSE_OVER_OUT, self.__OnMouseOverOut)
		self.AddEventListener(_BaseToggleButton.Events.ON_MOUSE_LEFT_BUTTON_DOWN, self.Toggle)
		self.AddEventListener(_BaseToggleButton.Events.ON_CLICK, self.__OnClick)

		self.AddEventListener(_BaseToggleButton.Events.ON_ENABLE, self.__RefreshUI)

	def Toggle(self):
		self.__isToggled = not self.IsToggled()

		if self.IsToggled():
			self.__OnToggleDown()
		else:
			self.__OnToggleUp()

		self.__RefreshUI()

	def __RefreshUI(self):
		if self.IsToggled():
			self.SetState(_ButtonState.ACTIVE, True)
		else:
			self.SetState(-1, True)

	def IsToggled(self):
		return self.__isToggled

	def __OnMouseOverIn(self):
		if self.IsToggled():
			return

		self.SetState(_ButtonState.HOVER, True)

	def __OnMouseOverOut(self):
		if self.IsToggled():
			return
		
		self.SetState(_ButtonState.NORMAL, True)

	def __OnClick(self):
		if self.IsToggled():
			return
		
		self.SetState(-1, True)
	
	##################################################
	## EVENTS

	class Events(_BaseButton.Events):
		ON_TOGGLE = _BaseButton.Events.ON_CLICK
		ON_TOGGLE_UP = EventEnum()
		ON_TOGGLE_DOWN = EventEnum()

	def __OnToggleUp(self):
		self.CallEventListener(_BaseToggleButton.Events.ON_TOGGLE_UP)

	def __OnToggleDown(self):
		self.CallEventListener(_BaseToggleButton.Events.ON_TOGGLE_DOWN)

class BoardButton(_BaseButton):
	IMAGES = {
		'LEFT' : {
			_ButtonState.NORMAL : "%s/board_main_left_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/board_main_left_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/board_main_left_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/board_main_left_01_normal.tga" % _BaseButton.BASE_PATH
		},
		'CENTER' : {
			_ButtonState.NORMAL : "%s/board_main_center_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/board_main_center_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/board_main_center_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/board_main_center_01_normal.tga" % _BaseButton.BASE_PATH
		},
		'RIGHT' : {
			_ButtonState.NORMAL : "%s/board_main_right_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/board_main_right_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/board_main_right_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/board_main_right_01_normal.tga" % _BaseButton.BASE_PATH
		}
	}

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 0.5
	}

	WIDTH = {
		'LEFT' : 9,
		'CENTER' : 90,
		'RIGHT' : 9
	}
	HEIGHT = 31

	WIDTH_TYPE = _BaseButton.WidthType.STRETCH

	TEXT_COLOR = {
		_ButtonState.NORMAL : 0xFFC8B89C,
		_ButtonState.HOVER : 0xFFF5CDB9,
		_ButtonState.ACTIVE : 0xFFB7766B,
		_ButtonState.DISABLED : 0xFFC8B89C
	}

	class Events(_BaseButton.Events):
		pass

class BoardToggleButton(_BaseToggleButton, BoardButton):
	pass

class ThinButton(_BaseButton):
	IMAGES = {
		'LEFT' : {
			_ButtonState.NORMAL : "%s/thinboard_main_left_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/thinboard_main_left_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/thinboard_main_left_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/thinboard_main_left_01_normal.tga" % _BaseButton.BASE_PATH
		},
		'CENTER' : {
			_ButtonState.NORMAL : "%s/thinboard_main_center_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/thinboard_main_center_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/thinboard_main_center_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/thinboard_main_center_01_normal.tga" % _BaseButton.BASE_PATH
		},
		'RIGHT' : {
			_ButtonState.NORMAL : "%s/thinboard_main_right_01_normal.tga" % _BaseButton.BASE_PATH,
			_ButtonState.HOVER : "%s/thinboard_main_right_02_hover.tga" % _BaseButton.BASE_PATH,
			_ButtonState.ACTIVE : "%s/thinboard_main_right_03_active.tga" % _BaseButton.BASE_PATH,
			_ButtonState.DISABLED : "%s/thinboard_main_right_01_normal.tga" % _BaseButton.BASE_PATH
		}
	}

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 0.5
	}

	WIDTH = {
		'LEFT' : 33,
		'CENTER' : 2,
		'RIGHT' : 33
	}
	HEIGHT = 28

	WIDTH_TYPE = _BaseButton.WidthType.REPEAT

	TEXT_COLOR = {
		_ButtonState.NORMAL : 0xFFF4E1C4,
		_ButtonState.HOVER : 0xFFFFF9F4,
		_ButtonState.ACTIVE : 0xFFCAB89F,
		_ButtonState.DISABLED : 0xFFF4E1C4
	}

	class Events(_BaseButton.Events):
		pass

class ThinToggleButton(_BaseToggleButton, ThinButton):
	pass

