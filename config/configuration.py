from typing import Dict, Tuple

from utils.timer_status import TimerStatus


WINDOW_SIZE: Tuple[int, int] = (500, 200)

ICON_PATH: str = r"D:\Codes\Codes\202020 Rule\assets\icon.ico"
SOUND_PATH: str = r"D:\Codes\Codes\202020 Rule\assets\notification.wav"

MINIMIZE_INSTEAD_OF_CLOSING: bool = False

DURATIONS: Dict[TimerStatus, int] = {
    TimerStatus.WORKING: 10,
    TimerStatus.BREAK: 20
}

SHOULD_SHOW_WINDOW_ON_TIMER_END: bool = True

SHOULD_START_ON_STARTUP: bool = True
