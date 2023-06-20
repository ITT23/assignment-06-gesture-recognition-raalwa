'''
'''
import sys
import pyglet
import config
from recognizer import Recognizer

window = pyglet.window.Window(
    width=config.WINDOW_WIDTH,
    height=config.WINDOW_HEIGHT)


def init():
    global background, batch, points, recognizer, result_label, state, instruction_label
    instruction_label = pyglet.text.Label(text=config.INSTRUCTIONS,
                                          font_size=20,
                                          color=config.TEXT_COLOR,
                                          x=int(config.WINDOW_WIDTH/2),
                                          y=int(4*config.WINDOW_HEIGHT/5),
                                          anchor_x='center')
    result_label = pyglet.text.Label(text="",
                                     font_size=20,
                                     color=config.TEXT_COLOR,
                                     x=int(config.WINDOW_WIDTH/2),
                                     y=int(4*config.WINDOW_HEIGHT/5),
                                     anchor_x='center')
    state = config.State.START
    points = []
    recognizer = Recognizer()
    batch = pyglet.graphics.Batch()
    background = pyglet.sprite.Sprite(img=config.BACKGROUND)
    pyglet.app.run()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global points
    if buttons & pyglet.window.mouse.LEFT:
        points.append([x, y])
        line = pyglet.shapes.Line(
            x, y, x+dx, y+dy, color=config.LINE_COLOR, width=config.LINE_WIDTH, batch=batch)
        batch.draw()


@window.event
def on_mouse_release(x, y, button, modifiers):
    global state
    if button == pyglet.window.mouse.LEFT:
        result = recognizer.recognize(points)
        result_label.text = f'Result: {result}'
        state = config.State.END


@window.event
def on_mouse_press(x, y, button, modifiers):
    global state
    if button == pyglet.window.mouse.LEFT:
        state = config.State.DRAWING
        background.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_draw():
    if state == config.State.START:
        window.clear()
        background.draw()
        instruction_label.draw()
    if state == config.State.DRAWING:
        pass
    if state == config.State.END:
        window.clear()
        background.draw()
        result_label.draw()


if __name__ == '__main__':
    init()
