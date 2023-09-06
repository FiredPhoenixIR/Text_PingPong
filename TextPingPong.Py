import curses
import time

def main(stdscr):
    # Screen Setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)  # 100ms timeout
    sh, sw = stdscr.getmaxyx()

    # Paddle Creation
    paddle_length = 5
    paddle_a = [(sh // 2 - paddle_length // 2, 0), (sh // 2 + paddle_length // 2, 0)]
    paddle_b = [(sh // 2 - paddle_length // 2, sw - 1), (sh // 2 + paddle_length // 2, sw - 1)]

    # Ball Creation
    ball = [sh // 2, sw // 2]
    ball_dir = [-1, 1]  # Initial ball direction (up and right)

    # Score Vars
    score_a = 0
    score_b = 0

    # Game loop
    while True:
        # Handle user input
        key = stdscr.getch()
        if key == ord('q'):
            break

        # Move the paddles
        if key == ord('w') and paddle_a[0][0] > 0:
            paddle_a = [(y - 1, x) for (y, x) in paddle_a]
        if key == ord('s') and paddle_a[1][0] < sh - 1:
            paddle_a = [(y + 1, x) for (y, x) in paddle_a]
        if key == ord('i') and paddle_b[0][0] > 0:
            paddle_b = [(y - 1, x) for (y, x) in paddle_b]
        if key == ord('k') and paddle_b[1][0] < sh - 1:
            paddle_b = [(y + 1, x) for (y, x) in paddle_b]

        # Update ball position
        ball[0] += ball_dir[0]
        ball[1] += ball_dir[1]

        # Check for collisions with paddles and walls
        if ball[0] == 0 or ball[0] == sh - 1:
            ball_dir[0] *= -1

        # Check for scoring
        if ball[1] == 0:
            score_b += 1
            ball = [sh // 2, sw // 2]
        elif ball[1] == sw - 1:
            score_a += 1
            ball = [sh // 2, sw // 2]

        # Check for collisions with paddles
        if paddle_a[0][0] <= ball[0] <= paddle_a[1][0] and ball[1] == 1:
            ball_dir[1] *= -1
        elif paddle_b[0][0] <= ball[0] <= paddle_b[1][0] and ball[1] == sw - 2:
            ball_dir[1] *= -1

        # Clear the screen
        stdscr.clear()

        # Draw paddles
        for y, x in paddle_a:
            stdscr.addch(y, x, '|')
        for y, x in paddle_b:
            stdscr.addch(y, x, '|')

        # Draw the ball
        stdscr.addch(ball[0], ball[1], '*')

        # Display the score
        stdscr.addstr(0, sw // 2 - 5, f"A:{score_a}  B:{score_b}")

        # Refresh the screen
        stdscr.refresh()

    # Clean up and exit
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
