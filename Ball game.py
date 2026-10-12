import pygame
import random
import sys
import math

# Initialize Pygame and the Joystick subsystem
pygame.init()
pygame.joystick.init()

# Check for connected Xbox controller
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Successfully connected controller: {joystick.get_name()}")
else:
    print("WARNING: No Xbox controller detected! Please plug it in and restart.")

# Window Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DIY Pilot ADAPT Assessment - Xbox Controller Input")
clock = pygame.time.Clock()

# Colors (RGB)
BACKGROUND = (20, 24, 33)
GRID_LINE = (50, 60, 75)
CENTER_GREEN = (46, 204, 113)
BALL_COLOR = (231, 76, 60)
TEXT_WHITE = (236, 240, 241)

# Game Variables
center_x, center_y = WIDTH // 2, HEIGHT // 2
ball_x, ball_y = float(center_x), float(center_y)
ball_radius = 15
target_radius = 40  

# Ball Physics
controller_sensitivity = 0.6  # Adjust this to change how fast the ball moves
friction = 0.96              # Simulates inertia and aerodynamic momentum
vel_x = 0.0
vel_y = 0.0
DEADZONE = 0.15              # Ignores minor stick drift when centering the stick

# Turbulence / Wind Variables
wind_force = 0.18            # Slightly higher drift to compensate for better analog accuracy
wind_angle = random.uniform(0, 2 * math.pi)
wind_change_timer = 0

# Scoring Metrics
time_in_center = 0.0  
total_time = 0.0      

# Game Loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  
    total_time += dt

    # Handle Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read Analog Inputs from Left Stick
    input_x = 0.0
    input_y = 0.0
    
    if joystick:
        # Axis 0 is Left Stick Horizontal, Axis 1 is Left Stick Vertical
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        
        # Apply deadzone filtering to avoid automatic drifting
        if abs(axis_x) > DEADZONE:
            input_x = axis_x
        if abs(axis_y) > DEADZONE:
            input_y = axis_y

    # Apply continuous acceleration based on how far you push the stick
    vel_x += input_x * controller_sensitivity
    vel_y += input_y * controller_sensitivity

    # Simulate Aerodynamic Turbulence (Changes direction every 1.5 seconds)
    wind_change_timer += dt
    if wind_change_timer > 1.5:
        wind_angle = random.uniform(0, 2 * math.pi)
        wind_change_timer = 0

    # Apply continuous drift forces
    vel_x += math.cos(wind_angle) * wind_force
    vel_y += math.sin(wind_angle) * wind_force

    # Apply friction and update position
    vel_x *= friction
    vel_y *= friction
    ball_x += vel_x
    ball_y += vel_y

    # Screen boundary constraints
    ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))
    ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))

    # Calculate Distance from Target Center
    distance_from_center = math.sqrt((ball_x - center_x)**2 + (ball_y - center_y)**2)
    
    if distance_from_center <= target_radius:
        time_in_center += dt

    # Drawing Graphics
    screen.fill(BACKGROUND)

    # Draw Crosshair System
    pygame.draw.line(screen, GRID_LINE, (0, center_y), (WIDTH, center_y), 1)
    pygame.draw.line(screen, GRID_LINE, (center_x, 0), (center_x, HEIGHT), 1)
    
    # Draw Inner Target Ring (Green Safe Zone)
    pygame.draw.circle(screen, CENTER_GREEN, (center_x, center_y), target_radius, 2)
    pygame.draw.circle(screen, GRID_LINE, (center_x, center_y), target_radius * 2, 1)

    # Draw User-Controlled Ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), ball_radius)

    # Display Telemetry UI Text
    font = pygame.font.SysFont("Courier", 20, bold=True)
    accuracy = (time_in_center / total_time) * 100 if total_time > 0 else 0.0
    
    text_score = font.render(f"Time in Target Zone: {time_in_center:.2f}s", True, TEXT_WHITE)
    text_accuracy = font.render(f"Tracking Accuracy : {accuracy:.1f}%", True, CENTER_GREEN if accuracy > 75 else BALL_COLOR)
    text_deviation = font.render(f"Center Deviation  : {int(distance_from_center)}px", True, TEXT_WHITE)
    
    screen.blit(text_score, (20, 20))
    screen.blit(text_accuracy, (20, 50))
    screen.blit(text_deviation, (20, 80))

    pygame.display.flip()

pygame.quit()
sys.exit()
