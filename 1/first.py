import pyglet
from pyglet import shapes

window = pyglet.window.Window(width=640, height=480, caption="Pyglet 3.1 Hello World")

batch = pyglet.graphics.Batch()
red_rect = shapes.Rectangle(x=220, y=140, width=200, height=200, 
                            color=(255, 0, 0), batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == "__main__":
    pyglet.app.run()