import curses
import time

def main(stdscr):
    # Configure curses for non-blocking input
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.clear()
    
    stdscr.addstr(0, 0, "Press keys (q to quit, arrow keys work too)")
    stdscr.refresh()
    
    counter = 0
    row = 2
    
    while True:
        # Non-blocking key read - returns -1 if no key pressed
        key = stdscr.getch()
        
        if key != -1:  # Key was pressed
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                stdscr.addstr(row, 0, f"UP arrow pressed! (count: {counter})")
            elif key == curses.KEY_DOWN:
                stdscr.addstr(row, 0, f"DOWN arrow pressed! (count: {counter})")
            elif key == curses.KEY_LEFT:
                stdscr.addstr(row, 0, f"LEFT arrow pressed! (count: {counter})")
            elif key == curses.KEY_RIGHT:
                stdscr.addstr(row, 0, f"RIGHT arrow pressed! (count: {counter})")
            else:
                stdscr.addstr(row, 0, f"Key pressed: {chr(key) if 32 <= key <= 126 else key} (count: {counter})")
            
            row += 1
            if row > 20:
                row = 2
                stdscr.clear()
                stdscr.addstr(0, 0, "Press keys (q to quit, arrow keys work too)")
            
            stdscr.refresh()
        
        # Do other work here without blocking
        counter += 1
        stdscr.addstr(1, 0, f"Loop iterations: {counter} ")
        stdscr.refresh()
        
        time.sleep(0.05)  # Small sleep to reduce CPU usage

# Run the curses application
curses.wrapper(main)