from tkinter import Button, Text, Tk
from typing import List, Tuple
from configuration import WINDOW_SIZE
from PIL import Image
from pystray import MenuItem, Icon
from pystray._win32 import Icon as icon
from sys import exit


class Notifier:
    def __init__(self) -> None:
        self.root = self.create_root()
        self.textbox = self.create_textbox()
        self.buttons = self.create_buttons()

        self.icon = self.create_system_tray_icon()

    def create_root(self) -> Tk:
        root: Tk = Tk()
        root.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        root.title("20/20/20 Rule Notifier")

        return root

    def create_textbox(self) -> Text:
        textbox: Text = Text(self.root)
        textbox.place(relx=0.5, rely=0.25, anchor='center',
                      relheight=0.5, relwidth=1.0)

        return textbox

    def create_buttons(self) -> List[Button]:
        buttons: List[Button] = []

        continue_button: Button = Button(
            self.root, command=lambda: print('Clicked continue'))
        buttons.append(continue_button)

        hide_button: Button = Button(
            self.root, command=lambda: self.hide_window())
        buttons.append(hide_button)

        for index, button in enumerate(buttons):
            button.place(relx=(index / len(buttons)), rely=0.75,
                         anchor='w', relwidth=(1 / len(buttons)), relheight=0.5)

        return buttons

    def create_system_tray_icon(self) -> icon:
        icon_image: Image = Image.open('./icon.jpeg')

        menu: Tuple[MenuItem, MenuItem] = (
            MenuItem("Show Window", self.show_window, default=True),
            MenuItem("Exit", self.exit_window)
        )

        tray_icon: icon = Icon("20/20/20 Rule Notifier",
                               icon_image, "20/20/20 Notifier", menu)
        tray_icon.visible = False

        return tray_icon

    def start(self) -> None:
        self.icon.run_detached()
        self.root.mainloop()

    def show_window(self) -> None:
        self.root.deiconify()
        self.icon.visible = False

    def hide_window(self) -> None:
        self.root.withdraw()
        self.icon.visible = True

    def exit_window(self) -> None:
        self.root.destroy()
        self.icon.stop()
