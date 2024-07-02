import curses
import random
import time
import math

# Initialize the screen
stdscr = curses.initscr()
curses.cbreak()  # Don't wait for enter key
stdscr.nodelay(1)  # Non-blocking getch()

#Initialize colors
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Saved baby
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Unsaved baby

# Define game characters
building = '|'
baby = 'B'
trampoline = '===='

# Building and ground dimensions
building_height = 20
building_width = 10
ground_width = 50

# Initial position and velocity for baby and position of trampoline
baby_pos = [building_height - 1, building_width // 2]
baby_velocity = [0, 0]
trampoline_pos = [building_height, ground_width // 2 - 1]

# Baby launch angle range (in degrees)
angle_range = [15, 30]

# Baby launch speed
launch_speed = 2

# Gravity
g = 0.2

# Game duration and score
start_time = time.time()
score = 0
killed = 0

def launch_baby():
    angle = random.randint(*angle_range)
    angle = math.radians(angle)  # convert to radians
    return [-launch_speed * math.sin(angle), launch_speed * math.cos(angle)]

baby_velocity = launch_baby()

try:
    # Set up the screen
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(1)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            trampoline_pos[1] = max(0, trampoline_pos[1] - 1)
        elif key == curses.KEY_RIGHT:
            trampoline_pos[1] = min(ground_width - len(trampoline), trampoline_pos[1] + 1)

        # Baby falls and moves
        baby_velocity[0] += g
        baby_pos[0] += baby_velocity[0]
        baby_pos[1] += baby_velocity[1]

        # Check if baby hits the trampoline
        if int(baby_pos[0]) == trampoline_pos[0] and int(baby_pos[1]) in range(trampoline_pos[1], trampoline_pos[1] + len(trampoline)):
            score += 1
            baby_pos = [building_height - 1, building_width // 2]
            baby_velocity = launch_baby()
            trampoline_color = curses.color_pair(1)  # Green for saved
        else:
            trampoline_color = curses.color_pair(0)  # Default color

        # Check if baby hits the ground or goes off screen
        if int(baby_pos[0]) > trampoline_pos[0] or int(baby_pos[1]) < 0 or int(baby_pos[1]) > ground_width:
            baby_pos = [building_height - 1, building_width // 2]
            baby_velocity = launch_baby()
            trampoline_color = curses.color_pair(2)  # Red for not saved

        # Redraw screen on EVERY iteration of the loop
        stdscr.clear()
        # Draw building, ground, baby, and trampoline as before
        for i in range(building_height):
            stdscr.addstr(i, building_width // 2, building)

        # Draw the ground
        for i in range(ground_width):
            stdscr.addstr(building_height, i, '-')

        # Draw the baby
        stdscr.addstr(int(baby_pos[0]), int(baby_pos[1]), baby)
        stdscr.addstr(trampoline_pos[0], trampoline_pos[1], trampoline, trampoline_color)

        # Display the score (same as before)
        stdscr.addstr(0, 0, f"Saved Babies: {score}")

        stdscr.refresh()
        time.sleep(0.1)  # Adjust the sleep time for smoother animation


        # Game ends after 1 minute
        if time.time() - start_time >= 60:
            break

finally:
    # Clean up the terminal
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

print(f'Game over. You saved {score} babies and killed {killed} babies.')

