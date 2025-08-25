"""
Use asyncio to manage async tasks.

TODO:
- [] implement looping
- [] implement interrupt/cancellation/skip
- [] show countdown
- [] solo pomodoro mode

"""
import argparse
from datetime import timedelta
import asyncio
import subprocess
import curses
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SessionState:
    driver_index: int = 0
    session_count: int = 0
    driver_times: Dict[str, float] = None
    
    def __post_init__(self):
        if self.driver_times is None:
            self.driver_times = {name: 0.0 for name in args.names}


class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def show(self, lines):
        """Display multiple lines at once"""
        self.stdscr.clear()
        for i, line in enumerate(lines):
            self.stdscr.addstr(i, 0, line)
        self.stdscr.refresh()
        
    def update_line(self, row, text, attrs=0):
        """Update a specific line without full refresh"""
        # Proper curses pattern: move -> addstr -> clrtoeol -> refresh
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()  # Clear from end of text to end of line
        self.stdscr.addstr(row, 0, text, attrs)
        self.stdscr.refresh()
        
    def update_line_with_parts(self, row, parts):
        """Update a line with multiple parts that can have different attributes"""
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()
        col = 0
        for text, attrs in parts:
            self.stdscr.addstr(row, col, text, attrs)
            col += len(text)
        self.stdscr.refresh()


class NotificationManager:
    @staticmethod
    def play_sound():
        try:
            subprocess.run(["afplay", "/System/Library/Sounds/Hero.aiff"], check=True)
        except subprocess.CalledProcessError:
            pass
            
    @staticmethod
    def say(message):
        if args.voice_enabled:
            try:
                subprocess.run(["say", message], check=True)
            except subprocess.CalledProcessError:
                pass


parser = argparse.ArgumentParser("mob.py", "specify input time and people")
parser.add_argument("-d", "--duration", default="10", type=float)
parser.add_argument("-b", "--break", dest="break_duration", default="0", type=float, help="Break duration (default 0, no break)")
parser.add_argument("--break-every", dest="break_every", default="1", type=int, help="Take a break every N sessions (default: 1)")
parser.add_argument("--no-voice", dest="voice_enabled", action="store_false", help="Disable voice announcements")
parser.add_argument("-n", "--names", nargs="*", action="extend", type=str)
def setup_args():
    global args
    args = parser.parse_args()

    if not args.names:
        names_input = input("Enter comma separated names (first will be first driver): ")
        args.names = [names_input] 

    args.names = [n.strip() for name in args.names for n in name.split(",") if n.strip()]

PROMPT = "(n to skip)> "



async def countdown_timer(display: Display, duration_seconds: int, current_driver: str, next_driver: str):
    """Generic countdown timer with skip functionality"""
    input_buffer = ""
    
    # Initial display with bold formatting
    display.stdscr.clear()
    display.stdscr.addstr(0, 0, "Driver: ")
    display.stdscr.addstr(0, 8, current_driver, curses.A_BOLD)
    display.stdscr.addstr(2, 0, "⏰ Time remaining:")
    display.stdscr.addstr(4, 0, PROMPT)
    display.stdscr.refresh()
    
    # Calculate line positions based on the layout
    time_line = 2  # Time is always on line 2
    input_line = 4  # Input prompt is on line 4
    message_line = 6  # Message goes after the layout
    
    # Time-based countdown
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + duration_seconds
    last_update = 0
    
    try:
        while True:
            current_time = asyncio.get_event_loop().time()
            remaining = max(0, int(end_time - current_time))
            
            # Update display only when the second changes
            if remaining != last_update:
                minutes, seconds = divmod(remaining, 60)
                # Update time with bold formatting
                time_parts = [
                    ("⏰ Time remaining: ", 0),
                    (f"{minutes:02d}:{seconds:02d}", curses.A_BOLD)
                ]
                display.update_line_with_parts(time_line, time_parts)
                # Position cursor back to input line after time update
                display.stdscr.move(input_line, len(PROMPT) + len(input_buffer))
                last_update = remaining
                
                # Check if time is up
                if remaining <= 0:
                    display.update_line(message_line, f"Session complete! Press enter to start timer for {next_driver}")
                    return "completed"
            
            # Handle input (fast response time)
            ch = display.stdscr.getch()
            if ch != -1:
                if ch in (ord('\n'), ord('\r')):
                    if input_buffer.strip().lower() == 'n':
                        display.update_line(message_line, f"Session skipped! Press enter to start timer for {next_driver}")
                        return "skipped"
                    else:
                        display.update_line(message_line, "Unknown command: " + input_buffer)
                    input_buffer = ""
                    display.update_line(input_line, PROMPT)
                elif ch in (127, curses.KEY_BACKSPACE):
                    if input_buffer:
                        input_buffer = input_buffer[:-1]
                elif 32 <= ch <= 126:
                    input_buffer += chr(ch)
                
                # Update input line and position cursor correctly
                display.update_line(input_line, PROMPT + input_buffer)
                display.stdscr.move(input_line, len(PROMPT) + len(input_buffer))
            
            # Fast input polling, but not tied to countdown
            await asyncio.sleep(0.05)
                        
    except asyncio.CancelledError:
        display.update_line(message_line, "Session interrupted")
        raise

def show_main_screen(display: Display, state: SessionState, session_duration: timedelta, is_pomodoro: bool):
    """Show the main session screen with bold formatting"""
    display.stdscr.clear()
    row = 0
    
    if is_pomodoro:
        display.stdscr.addstr(row, 0, "🍅 Pomodoro Session", curses.A_BOLD)
        row += 1
        display.stdscr.addstr(row, 0, "Solo Focus Time")
        row += 1
    else:
        display.stdscr.addstr(row, 0, "🚗 Mob Programming Session", curses.A_BOLD)
        row += 1
        display.stdscr.addstr(row, 0, "Current Driver: ")
        display.stdscr.addstr(row, 16, args.names[state.driver_index], curses.A_BOLD)
        row += 1
        
    display.stdscr.addstr(row, 0, f"Session Duration: ")
    display.stdscr.addstr(row, 18, str(session_duration), curses.A_BOLD)
    row += 1
    
    if not is_pomodoro:
        row += 1  # Empty line
        display.stdscr.addstr(row, 0, "Driving times:")
        row += 1
        for name, time in state.driver_times.items():
            prefix = "→ " if name == args.names[state.driver_index] else "  "
            display.stdscr.addstr(row, 0, prefix)
            if name == args.names[state.driver_index]:
                display.stdscr.addstr(row, 2, f"{name}: {time:.1f}m", curses.A_BOLD)
            else:
                display.stdscr.addstr(row, 2, f"{name}: {time:.1f}m")
            row += 1
    
    row += 1  # Empty line
    display.stdscr.addstr(row, 0, "Press any key to start the session timer...")
    display.stdscr.refresh()


async def handle_session_complete(state: SessionState, is_pomodoro: bool):
    """Handle end of session notifications and break logic"""
    state.session_count += 1
    state.driver_times[args.names[state.driver_index]] += args.duration
    
    # Notifications
    NotificationManager.play_sound()
    if not is_pomodoro:
        next_driver_name = args.names[(state.driver_index + 1) % len(args.names)]
        NotificationManager.say(f"{next_driver_name} is next driver")
    
    state.driver_index = (state.driver_index + 1) % len(args.names)


async def mob_session(display: Display, session_duration: timedelta):
    """Main mob programming session loop"""
    state = SessionState()
    is_pomodoro = len(args.names) == 1
    
    try:
        while True:
            # Show main screen
            show_main_screen(display, state, session_duration, is_pomodoro)
            
            # Wait for start
            await get_input(display)
            
            # Run session timer
            current_driver = args.names[state.driver_index]
            next_driver = args.names[(state.driver_index + 1) % len(args.names)]
            result = await countdown_timer(display, session_duration.seconds, current_driver, next_driver)
            
            if result in ("completed", "skipped"):
                await handle_session_complete(state, is_pomodoro)
                
                # Break logic
                if state.session_count % args.break_every == 0 and args.break_duration > 0:
                    next_driver_name = args.names[state.driver_index] if not is_pomodoro else None
                    await break_timer(display, args.break_duration * 60, is_pomodoro, next_driver_name)
                else:
                    await show_transition_screen(display, state, is_pomodoro)
                    
    except (KeyboardInterrupt, asyncio.CancelledError):
        display.show(["👋 Mob session ended. Thanks for coding together!"])
        await asyncio.sleep(2)

async def show_transition_screen(display: Display, state: SessionState, is_pomodoro: bool):
    """Show transition screen between sessions when no break is scheduled"""
    lines = []
    if is_pomodoro:
        lines.extend([
            f"🍅 Session {state.session_count} complete!",
        ])
        if args.break_duration > 0:
            lines.append(f"Next break in {args.break_every - (state.session_count % args.break_every)} sessions")
    else:
        lines.extend([
            f"🔄 Session {state.session_count} complete!",
            f"Next driver: {args.names[state.driver_index]}",
        ])
        if args.break_duration > 0:
            lines.append(f"Next break in {args.break_every - (state.session_count % args.break_every)} sessions")
    lines.extend(["", "Press any key to continue..."])
    display.show(lines)
    await get_input(display)


async def get_input(display: Display):
    """Wait for any keypress"""
    while True:
        if display.stdscr.getch() != -1:
            return
        await asyncio.sleep(0.01)

async def get_input_with_reminders(display: Display):
    """Wait for input with periodic voice reminders"""
    start_time = asyncio.get_event_loop().time()
    last_reminder = start_time
    reminder_interval = 2.5 * 60
    
    while True:
        if display.stdscr.getch() != -1:
            return
            
        current_time = asyncio.get_event_loop().time()
        if current_time - last_reminder >= reminder_interval:
            NotificationManager.say("Press enter to continue with the next session")
            last_reminder = current_time
        
        await asyncio.sleep(0.1)

async def break_timer(display: Display, break_seconds: int, is_pomodoro: bool, next_driver_name: str = None):
    """Break timer with skip functionality"""
    lines = [
        "🍅 Break time!" if is_pomodoro else "🔄 Break time!",
        "Take a short break" if is_pomodoro else f"Next driver will be: {next_driver_name}",
        "⏰ Break time remaining: --:--",
        "",
        "Press any key to skip break..."
    ]
    display.show(lines)
    
    # Time-based break countdown
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + break_seconds
    last_update = -1
    
    try:
        while True:
            current_time = asyncio.get_event_loop().time()
            remaining = max(0, int(end_time - current_time))
            
            # Update display only when the second changes
            if remaining != last_update:
                minutes, seconds = divmod(remaining, 60)
                display.update_line(2, f"⏰ Break time remaining: {minutes:02d}:{seconds:02d}")
                last_update = remaining
                
                # Check if break is complete
                if remaining <= 0:
                    display.update_line(5, "Break complete! Ready for next session...")
                    await asyncio.sleep(2)
                    return
            
            # Check for skip input (fast response)
            if display.stdscr.getch() != -1:
                display.update_line(5, "Break skipped! Ready for next session...")
                await asyncio.sleep(1)
                return
            
            # Fast input polling
            await asyncio.sleep(0.05)
                        
    except asyncio.CancelledError:
        display.update_line(5, "Break interrupted")
        raise

def curses_main(stdscr):
    """Main curses wrapper function"""
    curses.curs_set(1)
    stdscr.nodelay(1)
    stdscr.clear()
    
    display = Display(stdscr)
    asyncio.run(mob_session(display, timedelta(seconds=args.duration * 60)))

if __name__ == "__main__":
    setup_args()
    try:
        curses.wrapper(curses_main)
    except KeyboardInterrupt:
        pass
