'''
This module stores default values for the application
'''
import pyglet
from enum import Enum
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# Image by ChrisFiedler from Pixabay
BACKGROUND = pyglet.resource.image('assets/background.jpg')
TEXT_COLOR = (255, 255, 255, 255)
INSTRUCTION_COLOR = (255, 255, 255, 128)
LINE_COLOR = (0, 0, 0, 255)
LINE_WIDTH = 5
LABELS = ['v', 'x', 'arrow', 'check', 'circle']
NUM_POINTS = 64
INSTRUCTIONS = 'Draw a gesture on the canvas to begin'


class State(Enum):
    START = 1,
    DRAWING = 2,
    END = 3
