from logging import warning
from tkinter import Button, Text, Tk, END
from typing import List, Literal
from config.configuration import BG_COLOR, ICON_PATH, WINDOW_SIZE

from utils.event import Event
from utils.settings_reader import SettingsReader
from utils.time_parser import TimeParser


class NotifierWindow:
    def __init__(self, on_start: Event, on_exit: Event, on_end: Event, settings_reader: SettingsReader) -> None:
        self.time_parser: TimeParser = TimeParser()

        self.on_window_hide: Event = Event()
        self.on_window_hide.subscribe(self.hide_window)

        self.on_change_time: Event = Event()

        self.on_change_timer_status: Event = Event()
        self.on_change_timer_status.subscribe(self.change_state_button)

        self.on_settings_show: Event = Event()

        self.settings_reader = settings_reader

        self.on_end = on_end

        on_start.subscribe(self.start)

        on_exit.subscribe(self.exit_window)
        self.on_exit = on_exit

        self.on_reset: Event = Event()

        self.root = self.create_root()
        self.textbox = self.create_textbox()
        self.buttons = self.create_buttons()

        self.change_closing_protocol()

    def create_root(self) -> Tk:
        root: Tk = Tk()
        root.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        root.resizable(0, 0)
        root.bind('<Unmap>', lambda x: self.on_window_hide.notify())
        root.title("20/20/20 Rule Notifier")
        root.iconbitmap(ICON_PATH)

        root.config(bg=BG_COLOR)

        return root

    def create_textbox(self) -> Text:
        textbox: Text = Text(self.root, font=(
            'Arial', 48, 'bold'), highlightthickness=0, borderwidth=0, bg='#EAEAEA')
        textbox.place(relx=-0.5, rely=0.25, anchor='center',
                      relheight=0.5, relwidth=1.0)
        textbox.config(state='disabled')

        textbox.tag_configure('center', justify='center', spacing1=10)

        return textbox

    def create_buttons(self) -> List[Button]:
        buttons: List[Button] = []

        reset_button: Button = Button(
            self.root, command=lambda: self.on_reset.notify(), text="Reset")
        buttons.append(reset_button)

        continue_button: Button = Button(
            self.root, command=lambda: self.on_change_timer_status.notify(), text="Continue"
        )
        buttons.append(continue_button)

        skip_button: Button = Button(
            self.root, command=lambda: self.on_end.notify(), text="Skip"
        )
        buttons.append(skip_button)

        configuration_button: Button = Button(
            self.root, command=lambda: self.on_settings_show.notify(), text="Settings"
        )
        buttons.append(configuration_button)

        for index, button in enumerate(buttons):
            button.place(relx=(index / len(buttons)), rely=0.75,
                         anchor='w', relwidth=(1 / len(buttons)), relheight=0.5)

        return buttons

    def change_closing_protocol(self) -> None:
        self.root.protocol(
            "WM_DELETE_WINDOW", self.on_window_hide.notify if self.settings_reader.get_value('MINIMIZE_INSTEAD_OF_CLOSING') else self.on_exit.notify)

    def timer_change(self, seconds: int) -> None:
        self.textbox.config(state='normal')
        self.textbox.delete('1.0', END)
        self.textbox.insert(
            END, self.time_parser.parse_seconds(seconds), 'center')
        self.textbox.config(state='disabled')
        self.textbox.pack()

    def start(self) -> None:
        self.on_reset.notify()
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

    def change_state_button(self, value: Literal['Continue', 'Stop'] = None) -> None:
        continue_button = self.buttons[1]

        if not value:
            current_text: str = continue_button.cget('text')
            continue_button.config(
                text='Continue' if current_text != 'Continue' else 'Stop')
        else:
            continue_button.config(text=value)
