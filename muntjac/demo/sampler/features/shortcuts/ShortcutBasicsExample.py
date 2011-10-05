
from muntjac.ui import VerticalLayout, TextField, button, Button
from muntjac.ui.abstract_field import FocusShortcut
from muntjac.event.shortcut_action import KeyCode, ModifierKey


class ShortcutBasicsExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)

        # Firstname input with an input prompt for demo clarity
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        self.addComponent(firstname)

        # Add global shortcut that focuses the field
        firstname.addShortcutListener(FocusShortcut(firstname, KeyCode.F,
                ModifierKey.ALT, ModifierKey.SHIFT))

        # Lastname input with an input prompt for demo clarity
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        self.addComponent(lastname)

        # Add global shortcut that focuses the field
        lastname.addShortcutListener(FocusShortcut(lastname, KeyCode.L,
                ModifierKey.ALT, ModifierKey.SHIFT))

        # Button with a simple click-listener
        class EnterListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c.getWindow().showNotification('Enter button clicked')

        enter = Button('Enter', EnterListener(self))
        self.addComponent(enter)
        enter.setStyleName('primary')  # make it look like it's default

        # Add global shortcut using the built-in helper
        enter.setClickShortcut(KeyCode.ENTER)
        # which is easier to find, but otherwise equal to:
        # enter.addShortcutListener(new ClickShortcut(search,KeyCode.ENTER))
