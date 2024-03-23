from asyncio import run
from logging import warning
from threading import Thread
from tkinter import Button, Text, Tk, END
from typing import List
from config.configuration import MINIMIZE_INSTEAD_OF_CLOSING, WINDOW_SIZE

from utils.event import Event
from utils.time_parser import TimeParser


class Window:
    def __init__(self, on_start: Event, on_exit: Event) -> None:
        self.time_parser: TimeParser = TimeParser()

        self.on_window_hide: Event = Event()
        self.on_window_hide.subscribe(self.hide_window)

        self.on_change_time: Event = Event()
        self.on_change_timer_status: Event = Event()

        on_start.subscribe(self.start)

        on_exit.subscribe(self.exit_window)
        self.on_exit = on_exit

        self.root = self.create_root()
        self.textbox = self.create_textbox()
        self.buttons = self.create_buttons()

        self.change_closing_protocol()

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

        reset_button: Button = Button(
            self.root, command=lambda: self.on_change_time.notify(60 * 20))
        buttons.append(reset_button)

        continue_button: Button = Button(
            self.root, command=lambda: self.on_change_timer_status.notify()
        )
        buttons.append(continue_button)

        hide_button: Button = Button(
            self.root, command=lambda: self.on_window_hide.notify())
        buttons.append(hide_button)

        for index, button in enumerate(buttons):
            button.place(relx=(index / len(buttons)), rely=0.75,
                         anchor='w', relwidth=(1 / len(buttons)), relheight=0.5)

        return buttons

    def change_closing_protocol(self) -> None:
        self.root.protocol(
            "WM_DELETE_WINDOW", self.on_window_hide.notify if MINIMIZE_INSTEAD_OF_CLOSING else self.on_exit.notify)

    def timer_change(self, seconds: int) -> None:
        self.textbox.delete('1.0', END)
        self.textbox.insert(END, self.time_parser.parse_seconds(seconds))

    def start(self) -> None:
        self.root.mainloop()

    def show_window(self) -> None:
        self.root.deiconify()

    def hide_window(self) -> None:
        self.root.withdraw()

    def exit_window(self) -> None:
        try:
            self.root.quit()
            self.root.destroy()
        except (RuntimeError):
            warning('Destroying TK root on different thread.')
