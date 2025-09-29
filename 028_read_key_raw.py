import select
import sys
import termios
import select
import tty


fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

try:
    # PLAY WITH THIS
    # tty.setraw(fd)
    tty.setcbreak(fd)
    for i in range(100):
        ready, _, _ = select.select([sys.stdin], [], [], 0.1)  # Blocks efficiently
        if ready:
            key = sys.stdin.read(1)
            print(f"Key: {key}\r\n")
            if key == 'q':
                break
        else: 
            # Timeout occurred - no input
            pass

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

