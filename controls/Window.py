import dbg
from illumina.EventEnum import EventEnum
import wndMgr

class Window(object):
	_windowHandle = None
	__parent = None
	
	def __init__(self, layer = "UI"):
		self.RegisterWindow(layer)
	
	def __del__(self):
		wndMgr.Destroy(self.GetWindowHandle())
	
	def RegisterWindow(self, layer):
		self.SetWindowHandle(wndMgr.Register(self, layer))
	
	def SetWindowHandle(self, windowHandle):
		self._windowHandle = windowHandle
	
	def GetWindowHandle(self):
		return self._windowHandle
	
	def SetName(self, sName):
		wndMgr.SetName(self.GetWindowHandle(), sName)
	
	def GetName(self):
		return wndMgr.GetName(self.GetWindowHandle())

	def AddFlag(self, flag):
		wndMgr.AddFlag(self.GetWindowHandle(), flag)
	
	def SetTop(self):
		wndMgr.SetTop(self.GetWindowHandle())
	
	def Show(self):
		wndMgr.Show(self.GetWindowHandle())
	
	def Hide(self):
		wndMgr.Hide(self.GetWindowHandle())
	
	def IsShow(self):
		return wndMgr.IsShow(self.GetWindowHandle())
	
	def SetParent(self, parent):
		if not parent:
			dbg.TraceError("Window.SetParent :: Tried to set 'None' as parent for window '%s'." % self.GetName())
			return
		
		self.__parent = parent
		wndMgr.SetParent(self.GetWindowHandle(), self.__parent.GetWindowHandle())
	
	def GetParent(self):
		return self.__parent
	
	def SetPickAlways(self):
		wndMgr.SetPickAlways(self.GetWindowHandle())
	
	def IsFocus(self):
		return wndMgr.IsFocus(self.GetWindowHandle())
	
	def SetFocus(self):
		wndMgr.SetFocus(self.GetWindowHandle())
	
	def KillFocus(self):
		wndMgr.KillFocus(self.GetWindowHandle())
	
	def Lock(self):
		wndMgr.Lock(self.GetWindowHandle())
	
	def Unlock(self):
		wndMgr.Unlock(self.GetWindowHandle())
	
	def SetSize(self, width, height):
		wndMgr.SetWindowSize(self.GetWindowHandle(), width, height)
	
	def SetPosition(self, x, y):
		wndMgr.SetWindowPosition(self.GetWindowHandle(), x, y)
	
	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.GetWindowHandle())
	
	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.GetWindowHandle())
	
	def GetLocalPosition(self):
		return wndMgr.GetWindowLocalPosition(self.GetWindowHandle())
	
	def GetLocalX(self):
		(x, y) = self.GetLocalPosition()
		return x
	
	def GetLocalY(self):
		(x, y) = self.GetLocalPosition()
		return y
	
	def GetGlobalPosition(self):
		return wndMgr.GetWindowGlobalPosition(self.GetWindowHandle())
	
	def GetGlobalX(self):
		(x, y) = self.GetGlobalPosition()
		return x
	
	def GetGlobalY(self):
		(x, y) = self.GetGlobalPosition()
		return y
	
	def GetRect(self):
		return wndMgr.GetWindowRect(self.GetWindowHandle())
	
	def SetHorizontalAlign(self, horizontalAlign):
		wndMgr.SetWindowHorizontalAlign(self.GetWindowHandle(), horizontalAlign)
	
	def SetVerticalAlign(self, verticalAlign):
		wndMgr.SetWindowVerticalAlign(self.GetWindowHandle(), verticalAlign)
	
	def GetChildCount(self):
		return wndMgr.GetChildCount(self.GetWindowHandle())
	
	def IsPickedWindow(self):
		return wndMgr.IsPickedWindow(self.GetWindowHandle())
	
	def IsIn(self):
		return wndMgr.IsIn(self.GetWindowHandle())
	
	def GetMouseLocalPosition(self):
		return wndMgr.GetMouseLocalPosition(self.GetWindowHandle())
	
	def GetMousePosition(self):
		return wndMgr.GetMousePosition(self.GetWindowHandle())
	
	def IsDragging(self):
		return wndMgr.IsDragging(self.GetWindowHandle())
	
	def SetLimitBias(self, left, right, top, bottom):
		wndMgr.SetLimitBias(self.GetWindowHandle(), left, right, top, bottom)
	
	def UpdateRect(self):
		wndMgr.UpdateRect(self.GetWindowHandle())
	
	##################################################
	## EVENTS
	
	class Events(object):
		ON_MOVE_WINDOW = EventEnum()
		ON_SET_FOCUS = EventEnum()
		ON_KILL_FOCUS = EventEnum()

		ON_DROP = EventEnum()
		ON_TOP = EventEnum()
		
		ON_MOUSE_DRAG = EventEnum()
		ON_MOUSE_OVER_IN = EventEnum()
		ON_MOUSE_OVER_OUT = EventEnum()
		ON_MOUSE_LEFT_BUTTON_DOWN = EventEnum()
		ON_MOUSE_LEFT_BUTTON_UP = EventEnum()
		ON_MOUSE_LEFT_BUTTON_DOUBLE_CLICK = EventEnum()
		ON_MOUSE_RIGHT_BUTTON_DOWN = EventEnum()
		ON_MOUSE_RIGHT_BUTTON_UP = EventEnum()
		ON_MOUSE_RIGHT_BUTTON_DOUBLE_CLICK = EventEnum()
		ON_MOUSE_MIDDLE_BUTTON_DOWN = EventEnum()
		ON_MOUSE_MIDDLE_BUTTON_UP = EventEnum()
		
		ON_IME_UPDATE = EventEnum()
		ON_IME_TAB = EventEnum()
		ON_IME_RETURN = EventEnum()
		ON_IME_KEY_DOWN = EventEnum()
		ON_IME_CHANGE_CODE_PAGE = EventEnum()
		ON_IME_OPEN_CANDIDATE_LIST = EventEnum()
		ON_IME_CLOSE_CANDIDATE_LIST = EventEnum()
		ON_IME_OPEN_READING_WND = EventEnum()
		ON_IME_CLOSE_READING_WND = EventEnum()

		ON_KEY_DOWN = EventEnum()
		ON_KEY_UP = EventEnum()
		ON_PRESS_ESCAPE_KEY = EventEnum()
		ON_PRESS_EXIT_KEY = EventEnum()

		ON_UPDATE = EventEnum()
		ON_RENDER = EventEnum()

	__dictEvents = None
	
	def AddEventListener(self, eventType, eventListener):
		if not self.__dictEvents:
			self.__dictEvents = {}
		
		eventListenerList = self.__dictEvents.get(eventType, None)
		if eventListenerList:
			eventListenerList.append(eventListener)
		else:
			self.__dictEvents[eventType] = [eventListener]
	
	def RemoveEventListener(self, eventType, eventListener):
		eventListenerList = self.GetEventListeners(eventType)
		if not eventListenerList:
			return
		
		if eventListener in eventListenerList:
			eventListenerList.remove(eventListener)
	
	def GetEventListeners(self, eventType):
		if not self.__dictEvents:
			return None
		
		return self.__dictEvents.get(eventType, None)
	
	def CallEventListener(self, eventType, *args):
		eventListenerList = self.GetEventListeners(eventType)
		if not eventListenerList:
			return

		for eventListener in eventListenerList:
			eventListener(*args)
	
	def OnMouseDrag(self, x, y):
		self.CallEventListener(Window.Events.ON_MOUSE_DRAG, x, y)
	
	def OnMoveWindow(self, x, y):
		self.CallEventListener(Window.Events.ON_MOVE_WINDOW, x, y)
	
	def OnSetFocus(self):
		self.CallEventListener(Window.Events.ON_SET_FOCUS)
	
	def OnKillFocus(self):
		self.CallEventListener(Window.Events.ON_KILL_FOCUS)
	
	def OnMouseOverIn(self):
		self.CallEventListener(Window.Events.ON_MOUSE_OVER_IN)
	
	def OnMouseOverOut(self):
		self.CallEventListener(Window.Events.ON_MOUSE_OVER_OUT)
	
	def OnDrop(self):
		self.CallEventListener(Window.Events.ON_DROP)
	
	def OnTop(self):
		self.CallEventListener(Window.Events.ON_TOP)
	
	def OnIMEUpdate(self):
		self.CallEventListener(Window.Events.ON_IME_UPDATE)
	
	def OnMouseLeftButtonDown(self):
		self.CallEventListener(Window.Events.ON_MOUSE_LEFT_BUTTON_DOWN)
	
	def OnMouseLeftButtonUp(self):
		self.CallEventListener(Window.Events.ON_MOUSE_LEFT_BUTTON_UP)
	
	def OnMouseLeftButtonDoubleClick(self):
		self.CallEventListener(Window.Events.ON_MOUSE_LEFT_BUTTON_DOUBLE_CLICK)
	
	def OnMouseRightButtonDown(self):
		self.CallEventListener(Window.Events.ON_MOUSE_RIGHT_BUTTON_DOWN)
	
	def OnMouseRightButtonUp(self):
		self.CallEventListener(Window.Events.ON_MOUSE_RIGHT_BUTTON_UP)
	
	def OnMouseRightButtonDoubleClick(self):
		self.CallEventListener(Window.Events.ON_MOUSE_RIGHT_BUTTON_DOUBLE_CLICK)
	
	def OnMouseMiddleButtonDown(self):
		self.CallEventListener(Window.Events.ON_MOUSE_MIDDLE_BUTTON_DOWN)
	
	def OnMouseMiddleButtonUp(self):
		self.CallEventListener(Window.Events.ON_MOUSE_MIDDLE_BUTTON_UP)
	
	def OnIMETab(self):
		self.CallEventListener(Window.Events.ON_IME_TAB)
	
	def OnIMEReturn(self):
		self.CallEventListener(Window.Events.ON_IME_RETURN)
	
	def OnIMEKeyDown(self, key):
		self.CallEventListener(Window.Events.ON_IME_KEY_DOWN, key)
	
	def OnIMEChangeCodePage(self):
		self.CallEventListener(Window.Events.ON_IME_CHANGE_CODE_PAGE)
	
	def OnIMEOpenCandidateList(self):
		self.CallEventListener(Window.Events.ON_IME_OPEN_CANDIDATE_LIST)
	
	def OnIMECloseCandidateList(self):
		self.CallEventListener(Window.Events.ON_IME_CLOSE_CANDIDATE_LIST)
	
	def OnIMEOpenReadingWnd(self):
		self.CallEventListener(Window.Events.ON_IME_OPEN_READING_WND)
	
	def OnIMECloseReadingWnd(self):
		self.CallEventListener(Window.Events.ON_IME_CLOSE_READING_WND)
	
	def OnKeyDown(self, key):
		self.CallEventListener(Window.Events.ON_KEY_DOWN, key)
	
	def OnKeyUp(self, key):
		self.CallEventListener(Window.Events.ON_KEY_UP, key)
	
	def OnPressEscapeKey(self):
		self.CallEventListener(Window.Events.ON_PRESS_ESCAPE_KEY)
	
	def OnPressExitKey(self):
		self.CallEventListener(Window.Events.ON_PRESS_EXIT_KEY)

	def OnUpdate(self):
		self.CallEventListener(Window.Events.ON_UPDATE)

	def OnRender(self):
		self.CallEventListener(Window.Events.ON_RENDER)

