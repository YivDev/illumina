from TextLine import TextLine
from Window import Window
from Bar import Bar

import app
import wndMgr
import ime
import snd

class EditLine(TextLine):
	dictCandidateClassesByCodePage = {}

	@staticmethod
	def AddCandidateClass(codePage, candidateClass):
		EditLine.dictCandidateClassesByCodePage[codePage] = candidateClass

	@staticmethod
	def GetCandidateClass(codePage):
		return EditLine.dictCandidateClassesByCodePage.get(codePage, _EmptyCandidateWindow)

	def __init__(self, layer = "UI"):
		TextLine.__init__(self, layer)

		self.__currentCandidateWindowClass = None
		self.__currentCandidateWindow = None

		self.__imeMax = 0
		self.__imeUserMax = 0
		self.__imeUse = True

		self.__isNumberMode = False

		self.__wndReading = _ReadingWindow()
		self.__wndReading.Hide()

		self.AddEventListener(EditLine.Events.ON_SET_FOCUS, self._OnSetFocus)
		self.AddEventListener(EditLine.Events.ON_KILL_FOCUS, self._OnKillFocus)
		self.AddEventListener(EditLine.Events.ON_IME_CHANGE_CODE_PAGE, self._OnIMEChangeCodePage)
		self.AddEventListener(EditLine.Events.ON_IME_OPEN_CANDIDATE_LIST, self._OnIMEOpenCandidateList)
		self.AddEventListener(EditLine.Events.ON_IME_CLOSE_CANDIDATE_LIST, lambda : self.__currentCandidateWindow.Hide())
		self.AddEventListener(EditLine.Events.ON_IME_OPEN_READING_WND, self._OnIMEOpenReadingWindow())
		self.AddEventListener(EditLine.Events.ON_IME_CLOSE_READING_WND, lambda : self.__wndReading.Hide())
		self.AddEventListener(EditLine.Events.ON_IME_UPDATE, self._OnIMEUpdate)
		self.AddEventListener(EditLine.Events.ON_IME_RETURN, lambda : snd.PlaySound("sound/ui/click.wav"))
		self.AddEventListener(EditLine.Events.ON_KEY_DOWN, self._OnKeyDown)
		self.AddEventListener(EditLine.Events.ON_IME_KEY_DOWN, self._OnIMEKeyDown)
		self.AddEventListener(EditLine.Events.ON_MOUSE_LEFT_BUTTON_DOWN, self._OnMouseLeftButtonDown)

		self.SetCodePage(app.GetDefaultCodePage())

	def __del__(self):
		TextLine.__del__(self)

	def SetCodePage(self, codePage):
		self.__SetCandidateClass(EditLine.GetCandidateClass(codePage))

	def __SetCandidateClass(self, candidateWindowClass):
		if self.__currentCandidateWindowClass == candidateWindowClass:
			return

		self.__currentCandidateWindowClass = candidateWindowClass
		self.__currentCandidateWindow = self.__currentCandidateWindowClass()
		self.__currentCandidateWindow.Load()
		self.__currentCandidateWindow.Hide()

	def SetMax(self, max):
		self.__imeMax = max

		wndMgr.SetMax(self.GetWindowHandle(), self.__imeMax)
		ime.SetMax(self.__imeMax)

		self.SetUserMax(self.__imeMax)

	def GetMax(self):
		return self.__imeMax

	def SetUserMax(self, userMax):
		self.__imeUserMax = userMax

		ime.SetUserMax(self.__imeUserMax)

	def GetUserMax(self):
		return self.__imeUserMax

	def SetNumberMode(self, isNumberMode):
		self.__isNumberMode

	def IsNumberMode(self):
		return self.__isNumberMode
	
	def SetUseIME(self, useIME):
		self.__imeUse = useIME

	def IsUseIME(self):
		return self.__imeUse
	
	def SetText(self, text):
		wndMgr.SetText(self.GetWindowHandle(), text)

		if self.IsFocus():
			ime.SetText(text)

	def Enable(self):
		wndMgr.ShowCursor(self.GetWindowHandle())

	def Disable(self):
		wndMgr.HideCursor(self.GetWindowHandle())

	def MoveCursorToEnd(self):
		ime.MoveEnd()

	def _OnSetFocus(self):
		ime.SetText(self.GetText())
		ime.SetMax(self.GetMax())
		ime.SetUserMax(self.GetUserMax())
		ime.SetCursorPosition(-1)
		if self.IsNumberMode():
			ime.SetNumberMode()
		else:
			ime.SetStringMode()
		ime.EnableCaptureInput()
		if self.IsUseIME():
			ime.EnableIME()
		else:
			ime.DisableIME()
		wndMgr.ShowCursor(self.GetWindowHandle())

	def _OnKillFocus(self):
		self.SetText(ime.GetText(False))
		self.CallEventListener(EditLine.Events.ON_IME_CLOSE_CANDIDATE_LIST)
		self.CallEventListener(EditLine.Events.ON_IME_CLOSE_READING_WND)
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.GetWindowHandle())

	def _OnIMEChangeCodePage(self):
		self.SetCodePage(ime.GetCodePage())

	def _OnIMEOpenCandidateList(self):
		self.__currentCandidateWindow.Show()
		self.__currentCandidateWindow.Clear()
		self.__currentCandidateWindow.Refresh()
		self.__currentCandidateWindow.SetCandidatePosition(self.GetGlobalX(), self.GetGlobalY(), len(self.GetText()))

	def _OnIMEOpenReadingWindow(self):
		reading = ime.GetReading()

		self.__wndReading.SetReadingPosition(self.GetGlobalX() + (len(self.GetText()) - 2) * 6 - 24 - len(reading) * 6, self.GetGlobalY())
		self.__wndReading.SetText(reading)
		if ime.GetReadingError() == 0:
			self.__wndReading.SetTextColor(0xffffffff)
		else:
			self.__wndReading.SetTextColor(0xffff0000)
		self.__wndReading.SetSize(len(reading) * 6 + 4, 19)
		self.__wndReading.Show()

	def _OnIMEUpdate(self):
		snd.PlaySound("sound/ui/type.wav")
		self.SetText(ime.GetText())

	def _OnKeyDown(self, key):
		if key == app.DIK_V and app.IsPressed(app.DIK_LCONTROL):
			ime.PasteTextFromClipBoard()

	def _OnIMEKeyDown(self, key):
		if key == app.VK_LEFT:
			ime.MoveLeft()
		elif key == app.VK_RIGHT:
			ime.MoveRight()
		elif key == app.VK_HOME:
			ime.MoveHome()
		elif key == app.VK_END:
			ime.MoveEnd()
		elif key == app.VK_DELETE:
			ime.Delete()
			self.SetText(ime.GetText(False))

	def _OnMouseLeftButtonDown(self):
		if not self.IsIn():
			return

		self.SetFocus()
		ime.SetCursorPosition(wndMgr.GetCursorPosition(self.GetWindowHandle()))

class _EmptyCandidateWindow(Window):
	def __init__(self):
		Window.__init__(self)

	def __del__(self):
		Window.__init__(self)

	def Load(self):
		pass

	def SetCandidatePosition(self, x, y, textCount):
		pass

	def Clear(self):
		pass

	def Append(self, text):
		pass

	def Refresh(self):
		pass

	def Select(self):
		pass

class _ReadingWindow(Bar):
	def __init__(self):
		Bar.__init__(self, "TOP_MOST")
		
		self.__txtText = TextLine()
		self.__txtText.SetParent(self)
		self.__txtText.SetPosition(4, 3)
		self.__txtText.Show()

		self.SetSize(80, 19)
		self.Show()

	def __del__(self):
		Bar.__del__(self)

	def SetText(self, text):
		self.__txtText.SetText(text)

	def SetReadingPosition(self, x, y):
		self.SetPosition(x + 2, y - self.GetHeight() - 2)

	def SetTextColor(self, color):
		self.__txtText.SetPackedFontColor(color)

