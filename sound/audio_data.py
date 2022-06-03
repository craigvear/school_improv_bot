from dataclasses import dataclass
import config

"""a dataclass containing all the live audio data
from the microphone"""

@dataclass
class LiveAudioData:
    """Current live audio data"""

    mic_level: float = 0.0
    """current level of live mic"""

    speed: float = 0.5
    """calling the speed of Nebula"""

    baudrate: float = 0.1
    """calling tempo/ baudrate of Nebula"""

    freq: float = 0
    """fundamental frequency of signal from live mic"""

    midinote: tuple[str, int] = ("z", 0)
    """converted fund freq to note name and octave"""
