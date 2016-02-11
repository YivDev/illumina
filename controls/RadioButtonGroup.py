from Button import SimpleRadioButton
from Window import Window
from illumina.EventEnum import EventEnum
import dbg

class RadioButtonGroup(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.liButtons = []
		self.__selectedIndex = 0

	def __del__(self):
		Window.__del__(self)

		del self.liButtons

	def AppendButton(self, button):
		if button in self.liButtons:
			return

		index = len(self.liButtons)
		button.AddEventListener(SimpleRadioButton.Events.ON_CALL, lambda : self.Select(index))

		self.liButtons.append(button)

	def RemoveButton(self, button):
		if not button in self.liButtons:
			return
		
		self.liButtons.remove(button)

	def Select(self, index):
		if index < 0 or index >= len(self.liButtons):
			return
		
		self.__selectedIndex = index

		for button in self.liButtons:
			button.SetUp()

		self.liButtons[index].SetDown()

		self.__OnSelect(index)

	##################################################
	## EVENTS

	class Events(Window.Events):
		ON_SELECT = EventEnum()

	def __OnSelect(self, index):
		self.CallEventListener(RadioButtonGroup.Events.ON_SELECT, index)

