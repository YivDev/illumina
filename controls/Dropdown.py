from Window import Window
from Button import SimpleButton, _BaseButton, _ButtonState
from Board import _BoardBase

import illumina
import wndMgr

class _DropdownBoard(_BoardBase):
	BASE_PATH = "%s/controls/common/dropdown/" % illumina.BASE_PATH

	FILE_NAME_POSTFIX = "menu_"

	DIMENSIONS = {
		'CORNER' : {
			'WIDTH' : 5,
			'HEIGHT' : 5
		},
		'BAR_VERTICAL' : {
			'WIDTH' : 5,
			'HEIGHT' : 5
		},
		'BAR_HORIZONTAL' : {
			'WIDTH' : 5,
			'HEIGHT' : 5
		},
		'FILL' : {
			'WIDTH' : 5,
			'HEIGHT' : 5
		}
	}

	MIN_WIDTH = 5 * 2
	MIN_HEIGHT = 5 * 2

class Dropdown(Window):
	BASE_PATH = "%s/controls/common/dropdown/" % illumina.BASE_PATH

	COLLAPSED_HEIGHT = 27

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__isExpanded = True

		self.__elements = {}

		self.__CreateUI()

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__drpBoard = _DropdownBoard()
		self.__drpBoard.SetParent(self)
		self.__drpBoard.AddFlag("not_pick")
		self.__drpBoard.Show()

		self.__btnExpand = SimpleButton()
		self.__btnExpand.SetParent(self)
		self.__btnExpand.SetHorizontalAlign(wndMgr.HORIZONTAL_ALIGN_RIGHT)
		self.__btnExpand.SetUpVisual("%s/btn_01_normal.tga" % Dropdown.BASE_PATH)
		self.__btnExpand.SetOverVisual("%s/btn_02_hover.tga" % Dropdown.BASE_PATH)
		self.__btnExpand.SetDownVisual("%s/btn_03_active.tga" % Dropdown.BASE_PATH)
		self.__btnExpand.SetPosition(5, 5)
		self.__btnExpand.AddEventListener(SimpleButton.Events.ON_CALL, self.ToggleExpand)
		self.__btnExpand.Show()

	def __RefreshUI(self):
		if not self.IsExpanded():
			for btn in self.__elements.itervalues():
				btn.Hide()

			self.SetSize(self.GetWidth())
		else:
			i = 1
			for btn in self.__elements.itervalues():
				btn.SetPosition(2, 27 * i)
				btn.Show()

			self.SetSize(self.GetWidth(), 27 * (i + 2))
	
	def SetSize(self, width, height = _DropdownBoard.MIN_HEIGHT):
		width = max(_DropdownBoard.MIN_WIDTH, width)
		height = max(Dropdown.COLLAPSED_HEIGHT, height)

		self.__drpBoard.SetSize(width, height)

	def IsExpanded(self):
		return self.__isExpanded

	def SetExpanded(self, expanded):
		self.__isExpanded = expanded
		self.__RefreshUI()

	def ToggleExpand(self):
		self.SetExpanded(not self.IsExpanded())
	
	def AddElement(self, key, text):
		if self.__elements.has_key(key):
			return False

		btn = _DropdownElementButton()
		btn.SetParent(self)
		btn.SetWidth(self.GetWidth() - 4)
		btn.SetText(text)

		self.__elements[key] = btn

		self.__RefreshUI()

		return True

	def RemoveElement(self, key):
		if not self.__elements.has_key(key):
			return False

		del self.__elements[key]

		self.__RefreshUI()

		return True

class _DropdownElementButton(_BaseButton):
	IMAGES = {
		'LEFT' : {
			_ButtonState.NORMAL : "%s/menu_btn_left_01_normal.tga" % Dropdown.BASE_PATH,
			_ButtonState.HOVER : "%s/menu_btn_left_02_hover.tga" % Dropdown.BASE_PATH,
			_ButtonState.ACTIVE : "%s/menu_btn_left_03_active.tga" % Dropdown.BASE_PATH,
			_ButtonState.DISABLED : "%s/menu_btn_left_03_active.tga" % Dropdown.BASE_PATH
		},
		'CENTER' : {
			_ButtonState.NORMAL : "%s/menu_btn_center_01_normal.tga" % Dropdown.BASE_PATH,
			_ButtonState.HOVER : "%s/menu_btn_center_02_hover.tga" % Dropdown.BASE_PATH,
			_ButtonState.ACTIVE : "%s/menu_btn_center_03_active.tga" % Dropdown.BASE_PATH,
			_ButtonState.DISABLED : "%s/menu_btn_center_03_active.tga" % Dropdown.BASE_PATH
		},
		'RIGHT' : {
			_ButtonState.NORMAL : "%s/menu_btn_right_01_normal.tga" % Dropdown.BASE_PATH,
			_ButtonState.HOVER : "%s/menu_btn_right_02_hover.tga" % Dropdown.BASE_PATH,
			_ButtonState.ACTIVE : "%s/menu_btn_right_03_active.tga" % Dropdown.BASE_PATH,
			_ButtonState.DISABLED : "%s/menu_btn_right_03_active.tga" % Dropdown.BASE_PATH
		}
	}

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 1.0
	}

	WIDTH = {
		'LEFT' : 5,
		'CENTER' : 5,
		'RIGHT' : 5
	}
	HEIGHT = 25

	WIDTH_TYPE = _BaseButton.WidthType.STRETCH

	TEXT_COLOR = {
		_ButtonState.NORMAL : 0xFF938987,
		_ButtonState.HOVER : 0xFFD8CBC2,
		_ButtonState.ACTIVE : 0xFF827562,
		_ButtonState.DISABLED : 0xFF827562
	}

