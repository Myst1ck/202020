from config.configuration import SOUND_PATH
import pygame

from utils.event import Event


class Notifier:
    def __init__(self, on_start: Event, on_exit: Event) -> None:
        self.sound = None

        on_start.subscribe(self.start)
        on_exit.subscribe(self.exit)

    def start(self) -> None:
        pygame.init()

        self.sound = pygame.mixer.Sound(SOUND_PATH)

    def play_sound(self) -> None:
        self.sound.play()

    def exit(self) -> None:
        pygame.quit()
