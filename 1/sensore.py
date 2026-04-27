"""
Assignment 3 – Pyglet
3.1 Hello World   – red rectangle in a window
3.2 Keyboard Input – Q closes, arrow keys move the rectangle
3.3 Sensor Data   – DIPPID accelerometer moves the rectangle with border collision
"""

import pyglet
from pyglet.window import key
from pyglet import shapes
from DIPPID import SensorUDP

window = pyglet.window.Window(width=640, height=480, caption="Pyglet DIPPID")
batch = pyglet.graphics.Batch()

rect = shapes.Rectangle(x=300, y=200, width=50, height=50,
                         color=(255, 0, 0), batch=batch)

MOVE_SPEED = 10

PORT = 5700
sensor = SensorUDP(PORT)

SENSOR_SPEED = 300  

def update(dt):
    if not sensor.has_capability("accelerometer"):
        return

    accel = sensor.get_value("accelerometer")
    if accel is None:
        return

    ax = float(accel.get("x", 0.0))
    ay = float(accel.get("y", 0.0))

    # Move rectangle based on tilt
    rect.x += ax * SENSOR_SPEED * dt
    rect.y -= ay * SENSOR_SPEED * dt

    # Border collision – keep rectangle inside the window
    rect.x = max(0, min(rect.x, window.width  - rect.width))
    rect.y = max(0, min(rect.y, window.height - rect.height))

pyglet.clock.schedule_interval(update, 1 / 60)

# ──────────────────────────────────────────────────────────────────────────────
# Draw
# ──────────────────────────────────────────────────────────────────────────────
@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == "__main__":
    pyglet.app.run()