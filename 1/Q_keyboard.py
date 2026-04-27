import pyglet
from pyglet.window import key
from pyglet import shapes

window = pyglet.window.Window(width=640, height=480, caption="Keyboard Input Task")
batch = pyglet.graphics.Batch()
rect = shapes.Rectangle(x=300, y=200, width=50, height=50, 
                        color=(255, 0, 0), batch=batch)

# Speed of the rectangle (pixels per movement)
MOVE_SPEED = 10

@window.event
def on_key_press(symbol, modifiers):
    # Close the window if 'Q' is pressed
    if symbol == key.Q:
        window.close()
    
    # Move the rectangle based on Arrow Keys
    elif symbol == key.UP:
        rect.y += MOVE_SPEED
    elif symbol == key.DOWN:
        rect.y -= MOVE_SPEED
    elif symbol == key.LEFT:
        rect.x -= MOVE_SPEED
    elif symbol == key.RIGHT:
        rect.x += MOVE_SPEED

@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == "__main__":
    pyglet.app.run()