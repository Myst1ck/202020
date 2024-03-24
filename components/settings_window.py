import logging
import math
import tkinter
from typing import Any, Dict, Literal, Tuple, TypeAlias

from config.configuration import BG_COLOR, ICON_PATH, SETTINGS_WINDOW_SIZE
from utils.event import Event
from utils.settings_reader import SettingsReader

CheckboxInput: TypeAlias = Tuple[tkinter.Label,
                                 tkinter.BooleanVar, tkinter.Checkbutton]
IntegerInput: TypeAlias = Tuple[tkinter.Label, tkinter.IntVar, tkinter.Spinbox]


class SettingsWindow:
    def __init__(self, on_exit: Event, settings_reader: SettingsReader) -> None:
        on_exit.subscribe(self.exit)

        self.root: tkinter.Tk = None

        self.checkbox_inputs: Dict[str, Any] = None
        self.integer_inputs: Dict[str, Any] = None
        self.save_button: tkinter.Button = None

        self.settings_reader = settings_reader

        self.on_settings_change: Event = Event()

    def create_root(self) -> tkinter.Tk:
        root = tkinter.Toplevel()
        root.geometry(f"{SETTINGS_WINDOW_SIZE[0]}x{SETTINGS_WINDOW_SIZE[1]}")
        root.resizable(0, 0)
        root.bind('<Unmap>', lambda _: self.exit())
        root.title('20/20/20 Rule Notifier Settings')
        root.iconbitmap(ICON_PATH)

        root.config(bg=BG_COLOR)

        return root

    def start(self) -> None:
        if self.root is None:
            self.root = self.create_root()
            self.setup_widgets()

        self.root.mainloop()

    def setup_widgets(self) -> None:
        self.checkbox_inputs = self.create_checkbox_inputs()
        self.integer_inputs = self.create_string_inputs()

        self.save_button = self.create_save_button()

    def create_checkbox_inputs(self) -> Dict[str, Any]:
        def create_checkbox_input(text: str, key: str, self: SettingsWindow, value: bool = None) -> Dict[str, CheckboxInput]:
            label = tkinter.Label(self.root, text=text)
            label.pack()

            var = tkinter.BooleanVar(value=self.settings_reader.get_value(
                key) if value is None else value)

            checkbox = tkinter.Checkbutton(self.root, variable=var)
            checkbox.pack()

            return {key: (label, var, checkbox)}

        result: Dict[str, Any] = create_checkbox_input(
            'Minimize window instead of closing.', 'MINIMIZE_INSTEAD_OF_CLOSING', self)
        result.update(create_checkbox_input('Show window on timer end.',
                      'SHOULD_SHOW_WINDOW_ON_TIMER_END', self))
        result.update(create_checkbox_input(
            'Start the timer on startup.', 'SHOULD_START_ON_STARTUP', self))

        return result

    def create_string_inputs(self) -> Dict[str, Any]:
        def create_string_input(text: str, key: str, self: SettingsWindow, value: str = None) -> Dict[str, IntegerInput]:
            label = tkinter.Label(self.root, text=text)
            label.pack()

            var = tkinter.IntVar(
                value=str(self.settings_reader.get_value(key)) if value is None else value)

            entry = tkinter.Spinbox(self.root, textvariable=var, from_=0, to=math.inf)
            entry.pack()

            return {key: (label, var, entry)}

        def create_durations(self: SettingsWindow) -> Dict[str, Dict[str, IntegerInput]]:
            duration_label = tkinter.Label(self.root, text='Durations (in seconds):')
            duration_label.pack()

            durations: Dict[Literal['WORKING', 'BREAK'],
                            int] = self.settings_reader.get_value('DURATIONS')

            result: Dict[str, Any] = create_string_input(
                'Working time.', 'WORKING', self, durations['WORKING'])
            result.update(create_string_input('Eye break time.', 'BREAK', self, durations['BREAK']))

            return {'DURATIONS': result}

        return create_durations(self)

    def create_save_button(self) -> tkinter.Button:
        save_button = tkinter.Button(self.root, text='Save settings.', command=self.settings_save)
        save_button.pack()

        return save_button

    def exit(self) -> None:
        try:
            self.root.quit()
            self.root.destroy()
        except RuntimeError:
            logging.warning('Destroying TK root on different thread.')
        except Exception as e:
            logging.warning(e)

    def settings_save(self) -> None:
        def put_settings(settings: Dict[str, Any], item: Any, key: str) -> None:
            if isinstance(item, tuple) and len(item) >= 1 and isinstance(item[1], tkinter.Variable):
                settings[key] = item[1].get()
            elif isinstance(item, dict):
                settings[key] = {}

                for new_key, value in item.items():
                    put_settings(settings[key], value, new_key)
            else:
                logging.warning(f'Checkbox of type {type(checkbox)}.')

        settings: Dict[str, Any] = {}

        for key, checkbox in self.checkbox_inputs.items():
            put_settings(settings, checkbox, key)

        for key, integer in self.integer_inputs.items():
            put_settings(settings, integer, key)

        if settings != self.settings_reader.get_settings():
            self.settings_reader.write_settings(settings)
            self.on_settings_change.notify()
