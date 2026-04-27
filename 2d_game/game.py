import pyglet
from pyglet import shapes
import random
import sys
import os

# Add the current directory to sys.path so we can import DIPPID if it's there
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from DIPPID import SensorUDP
except ImportError:
    print("Error: Could not import DIPPID. Make sure DIPPID.py is in the same directory.")
    sys.exit(1)

# Set up DIPPID
PORT = 5700
sensor = SensorUDP(PORT)

# Set up Pyglet window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Simple 2D Coin Collector")

# Game state
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT // 2
player_vx = 0.0
player_vy = 0.0
player_radius = 20
ACCELERATION = 1.5
FRICTION = 0.94

coin_x = random.randint(50, WINDOW_WIDTH - 50)
coin_y = random.randint(50, WINDOW_HEIGHT - 50)
coin_radius = 15

score = 0
score_label = pyglet.text.Label('Score: 0',
                          font_name='Arial',
                          font_size=24,
                          x=10, y=WINDOW_HEIGHT - 30,
                          anchor_x='left', anchor_y='center')

# Create a batch for efficient drawing if needed, but simple shapes are fine for now.
main_batch = pyglet.graphics.Batch()

def update(dt):
    global player_x, player_y, player_vx, player_vy, coin_x, coin_y, score
    
    if sensor.has_capability('accelerometer'):
        acc = sensor.get_value('accelerometer')
        
        # Add acceleration based on device tilt
        player_vx += acc['x'] * ACCELERATION
        player_vy += acc['y'] * ACCELERATION
        
        # Apply friction to simulate rolling resistance
        player_vx *= FRICTION
        player_vy *= FRICTION
        
        # Update position
        player_x += player_vx
        player_y += player_vy
        
        # Keep player on screen and add bounce effect
        if player_x < player_radius:
            player_x = player_radius
            player_vx *= -0.6
        elif player_x > WINDOW_WIDTH - player_radius:
            player_x = WINDOW_WIDTH - player_radius
            player_vx *= -0.6
            
        if player_y < player_radius:
            player_y = player_radius
            player_vy *= -0.6
        elif player_y > WINDOW_HEIGHT - player_radius:
            player_y = WINDOW_HEIGHT - player_radius
            player_vy *= -0.6
            
        dist = ((player_x - coin_x)**2 + (player_y - coin_y)**2)**0.5
        if dist < player_radius + coin_radius:
            score += 1
            score_label.text = f'Score: {score}'
            coin_x = random.randint(50, WINDOW_WIDTH - 50)
            coin_y = random.randint(50, WINDOW_HEIGHT - 50)

pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    
    # Draw coin (yellow)
    coin = shapes.Circle(coin_x, coin_y, coin_radius, color=(255, 255, 0))
    coin.draw()
    
    # Draw player (red default, green if button 1 is pressed)
    player_color = (255, 0, 0)
    if sensor.has_capability('button_1'):
        btn = sensor.get_value('button_1')
        if btn == 1:
            player_color = (0, 255, 0)
    
    player = shapes.Circle(player_x, player_y, player_radius, color=player_color)
    player.draw()
    
    score_label.draw()

if __name__ == '__main__':
    print("Starting Game. Make sure DIPPID sender is running on port", PORT)
    pyglet.app.run()
