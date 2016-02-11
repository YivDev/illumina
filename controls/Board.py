from Window import Window
from ImageBox import ImageBox
from ExpandedImageBox import ExpandedImageBox
from TitleBar import TitleBar
import illumina
import wndMgr

import dbg

class _BoardBase(Window):
	BASE_PATH = ""

	FILE_NAME_POSTFIX = ""

	DIMENSIONS = {
		'CORNER' : {
			'WIDTH' : 0,
			'HEIGHT' : 0
		},
		'BAR_VERTICAL' : {
			'WIDTH' : 0,
			'HEIGHT' : 0
		},
		'BAR_HORIZONTAL' : {
			'WIDTH' : 0,
			'HEIGHT' : 0
		},
		'FILL' : {
			'WIDTH' : 0,
			'HEIGHT' : 0
		}
	}

	MIN_WIDTH = 0
	MIN_HEIGHT = 0

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self._CreateUI()

		self.SetSize(self.MIN_WIDTH, self.MIN_HEIGHT)

	def __del__(self):
		Window.__del__(self)

	def _CreateUI(self):
		self._dictImages = {
			'CORNER' : {
				'LEFTTOP' : ImageBox(),
				'RIGHTTOP' : ImageBox(),
				'LEFTBOTTOM' : ImageBox(),
				'RIGHTBOTTOM' : ImageBox()
			},
			'BAR' : {
				'LEFT' : ExpandedImageBox(),
				'TOP' : ExpandedImageBox(),
				'RIGHT' : ExpandedImageBox(),
				'BOTTOM' : ExpandedImageBox()
			},
			'FILL' : ExpandedImageBox()
		}

		for imageDictKey in (['CORNER', 'BAR']):
			for position, image in self._dictImages[imageDictKey].iteritems():
				image.SetParent(self)
				image.AddFlag("not_pick")
				image.LoadImage("%s/%s%s_%s.tga" % (self.BASE_PATH, self.FILE_NAME_POSTFIX, imageDictKey.lower(), position.lower()))
				image.Show()
				
		self._dictImages['FILL'].SetParent(self)
		self._dictImages['FILL'].AddFlag("not_pick")
		self._dictImages['FILL'].LoadImage("%s/%sfill.tga" % (self.BASE_PATH, self.FILE_NAME_POSTFIX))
		self._dictImages['FILL'].Show()

	def SetSize(self, width, height):
		width = max(self.DIMENSIONS['CORNER']['WIDTH'] * 2, width)
		height = max(self.DIMENSIONS['CORNER']['HEIGHT'] * 2, height)

		Window.SetSize(self, width, height)

		self._dictImages['CORNER']['LEFTTOP'].SetPosition(0, 0)
		self._dictImages['CORNER']['RIGHTTOP'].SetPosition(width - self.DIMENSIONS['CORNER']['WIDTH'], 0)
		self._dictImages['CORNER']['LEFTBOTTOM'].SetPosition(0, height - self.DIMENSIONS['CORNER']['HEIGHT'])
		self._dictImages['CORNER']['RIGHTBOTTOM'].SetPosition(width - self.DIMENSIONS['CORNER']['WIDTH'], height - self.DIMENSIONS['CORNER']['HEIGHT'])
		
		widthForRendering = width - (self.DIMENSIONS['CORNER']['WIDTH'] * 2)
		heightForRendering = height - (self.DIMENSIONS['CORNER']['HEIGHT'] * 2)

		verticalRenderingRect = -1.0 + float(widthForRendering) / float(self.DIMENSIONS['BAR_VERTICAL']['WIDTH'])
		horizontalRenderingRect = -1.0 + float(heightForRendering) / float(self.DIMENSIONS['BAR_HORIZONTAL']['HEIGHT'])

		self._dictImages['BAR']['LEFT'].SetPosition(0, self.DIMENSIONS['CORNER']['HEIGHT'])
		self._dictImages['BAR']['LEFT'].SetRenderingRect(0.0, 0.0, 0.0, horizontalRenderingRect)
		self._dictImages['BAR']['LEFT'].SetSize(self.DIMENSIONS['BAR_HORIZONTAL']['WIDTH'], heightForRendering)

		self._dictImages['BAR']['TOP'].SetPosition(self.DIMENSIONS['CORNER']['WIDTH'], 0)
		self._dictImages['BAR']['TOP'].SetRenderingRect(0.0, 0.0, verticalRenderingRect, 0.0)
		self._dictImages['BAR']['TOP'].SetSize(widthForRendering, self.DIMENSIONS['BAR_VERTICAL']['HEIGHT'])

		self._dictImages['BAR']['RIGHT'].SetPosition(width - self.DIMENSIONS['BAR_HORIZONTAL']['WIDTH'], self.DIMENSIONS['CORNER']['HEIGHT'])
		self._dictImages['BAR']['RIGHT'].SetRenderingRect(0.0, 0.0, 0.0, horizontalRenderingRect)
		self._dictImages['BAR']['RIGHT'].SetSize(self.DIMENSIONS['BAR_HORIZONTAL']['WIDTH'], heightForRendering)

		self._dictImages['BAR']['BOTTOM'].SetPosition(self.DIMENSIONS['CORNER']['WIDTH'], height - self.DIMENSIONS['BAR_VERTICAL']['HEIGHT'])
		self._dictImages['BAR']['BOTTOM'].SetRenderingRect(0.0, 0.0, verticalRenderingRect, 0.0)
		self._dictImages['BAR']['BOTTOM'].SetSize(widthForRendering, self.DIMENSIONS['BAR_VERTICAL']['HEIGHT'])
		
		self._dictImages['FILL'].SetPosition(self.DIMENSIONS['CORNER']['WIDTH'], self.DIMENSIONS['CORNER']['HEIGHT'])
		self._dictImages['FILL'].SetRenderingRect(0.0, 0.0, -1.0 + float(widthForRendering) / float(self.DIMENSIONS['FILL']['WIDTH']), -1.0 + float(heightForRendering) / float(self.DIMENSIONS['FILL']['HEIGHT']))
		self._dictImages['FILL'].SetSize(widthForRendering, heightForRendering)

class Board(_BoardBase):
	class _Shadow(_BoardBase):
		BASE_PATH = "%s/controls/common/board/" % illumina.BASE_PATH

		FILE_NAME_POSTFIX = "shadow_"

		DIMENSIONS = {
			'CORNER' : {
				'WIDTH' : 73,
				'HEIGHT' : 73
			},
			'BAR_VERTICAL' : {
				'WIDTH' : 1,
				'HEIGHT' : 73
			},
			'BAR_HORIZONTAL' : {
				'WIDTH' : 73,
				'HEIGHT' : 1
			},
			'FILL' : {
				'WIDTH' : 1,
				'HEIGHT' : 1
			}
		}

		MIN_WIDTH = 55 * 2
		MIN_HEIGHT = 55 * 2

		def SetOpacity(self, opacity):
			for imageDictKey in (['CORNER', 'BAR']):
				for position, image in self._dictImages[imageDictKey].iteritems():
					image.SetDiffuseColor(1.0, 1.0, 1.0, opacity)
				
			self._dictImages['FILL'].SetDiffuseColor(1.0, 1.0, 1.0, opacity)

	BASE_PATH = "%s/controls/common/board/" % illumina.BASE_PATH

	DIMENSIONS = {
		'CORNER' : {
			'WIDTH' : 55,
			'HEIGHT' : 55
		},
		'BAR_VERTICAL' : {
			'WIDTH' : 128,
			'HEIGHT' : 55
		},
		'BAR_HORIZONTAL' : {
			'WIDTH' : 55,
			'HEIGHT' : 128
		},
		'FILL' : {
			'WIDTH' : 128,
			'HEIGHT' : 128
		}
	}

	MIN_WIDTH = 55 * 2
	MIN_HEIGHT = 55 * 2

	def __init__(self, shadowSize = -1, layer = "UI"):
		self.__hasShadow = shadowSize != -1
		self.__shadowSize = shadowSize

		_BoardBase.__init__(self, layer)

	def __del__(self):
		_BoardBase.__del__(self)

	def _CreateUI(self):
		if self.__hasShadow:
			self.__CreateShadow()
		else:
			self.__wndShadow = None

		self.__imgDecoration = ImageBox()
		self.__imgDecoration.SetParent(self)
		self.__imgDecoration.LoadImage("%s/decoration_leftbottom.tga" % self.BASE_PATH)
		self.__imgDecoration.SetVerticalAlign(wndMgr.VERTICAL_ALIGN_BOTTOM)
		self.__imgDecoration.Show()

		_BoardBase._CreateUI(self)

		self.__wndTitleBar = None

	def SetSize(self, width, height):
		_BoardBase.SetSize(self, width, height)

		self.__imgDecoration.SetPosition(-5, 52)

		self.UpdateTitleBar()

		if self.__hasShadow:
			self.UpdateShadow()

	## TitleBar
	def AddTitleBar(self):
		self.__wndTitleBar = TitleBar()
		self.__wndTitleBar.SetParent(self)
		self.__wndTitleBar.SetPosition(9, 11)
		self.__wndTitleBar.Show()

		self.UpdateTitleBar()

	def GetTitleBar(self):
		return self.__wndTitleBar
	
	def UpdateTitleBar(self):
		if not self.__wndTitleBar:
			return

		self.__wndTitleBar.SetWidth(self.GetWidth() - 18)

	## Shadow
	def __CreateShadow(self):
		self.__wndShadow = Board._Shadow()
		self.__wndShadow.SetParent(self)
		self.__wndShadow.SetPosition(-self.__shadowSize, -self.__shadowSize)
		self.__wndShadow.Show()

		self.__wndShadow.SetOpacity(0.0)

	def UpdateShadow(self):
		self.__wndShadow.SetSize(self.GetWidth() + self.__shadowSize * 2, self.GetHeight() + self.__shadowSize * 2)

	def GetShadow(self):
		return self.__wndShadow

class TransparentThinBoard(_BoardBase):
	BASE_PATH = "%s/controls/common/thinboard_transparent/" % illumina.BASE_PATH

	DIMENSIONS = {
		'CORNER' : {
			'WIDTH' : 21,
			'HEIGHT' : 21
		},
		'BAR_VERTICAL' : {
			'WIDTH' : 21,
			'HEIGHT' : 21
		},
		'BAR_HORIZONTAL' : {
			'WIDTH' : 21,
			'HEIGHT' : 21
		},
		'FILL' : {
			'WIDTH' : 1,
			'HEIGHT' : 1
		}
	}

	MIN_WIDTH = 21 * 2
	MIN_HEIGHT = 21 * 2

class IntransparentThinBoard(_BoardBase):
	BASE_PATH = "%s/controls/common/thinboard_intransparent/" % illumina.BASE_PATH

	DIMENSIONS = {
		'CORNER' : {
			'WIDTH' : 17,
			'HEIGHT' : 17
		},
		'BAR_VERTICAL' : {
			'WIDTH' : 1,
			'HEIGHT' : 17
		},
		'BAR_HORIZONTAL' : {
			'WIDTH' : 17,
			'HEIGHT' : 1
		},
		'FILL' : {
			'WIDTH' : 1,
			'HEIGHT' : 1
		}
	}

	MIN_WIDTH = 17 * 2
	MIN_HEIGHT = 17 * 2

