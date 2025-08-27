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
    driver_times: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        if self.driver_times is None:
            self.driver_times = {name: 0.0 for name in args.names}


class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def show(self, lines):
        """Display multiple lines at once
        
        Args:
            lines: List of lines, where each line can be:
                   - A string for plain text
                   - A list of (text, attrs) tuples for formatted text
        """
        self.stdscr.clear()
        for i, line in enumerate(lines):
            if isinstance(line, str):
                # Simple string case
                self.stdscr.addstr(i, 0, line)
            else:
                # List of (text, attrs) tuples case
                col = 0
                for text, attrs in line:
                    self.stdscr.addstr(i, col, text, attrs)
                    col += len(text)
        self.stdscr.refresh()
        
    def update_line(self, row, content, attrs=0):
        """Update a specific line without full refresh
        
        Args:
            row: Line number to update
            content: Either a string or list of (text, attrs) tuples
            attrs: Attributes for simple string (ignored if content is a list)
        """
        # Proper curses pattern: move -> addstr -> clrtoeol -> refresh
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()  # Clear from end of text to end of line
        
        if isinstance(content, str):
            # Simple string case
            self.stdscr.addstr(row, 0, content, attrs)
        else:
            # List of (text, attrs) tuples case
            col = 0
            for text, part_attrs in content:
                self.stdscr.addstr(row, col, text, part_attrs)
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
    
    @staticmethod
    def show_notification(title, message, sound=None):
        """Show native macOS notification using AppleScript"""
        if not args.notifications_enabled:
            return
            
        try:
            applescript = f'display notification "{message}" with title "{title}"'
            if sound:
                applescript += f' sound name "{sound}"'
            
            subprocess.run(["osascript", "-e", applescript], check=True)
        except subprocess.CalledProcessError:
            pass


parser = argparse.ArgumentParser("mob.py", "specify input time and people")
parser.add_argument("-d", "--duration", default="10", type=float)
parser.add_argument("-b", "--break", dest="break_duration", default="0", type=float, help="Break duration (default 0, no break)")
parser.add_argument("--break-every", dest="break_every", default="1", type=int, help="Take a break every N sessions (default: 1)")
parser.add_argument("--no-voice", dest="voice_enabled", action="store_false", help="Disable voice announcements")
parser.add_argument("--notifications", dest="notifications_enabled", action="store_true", help="Enable native macOS notifications")
parser.add_argument("-n", "--names", nargs="*", action="extend", type=str)
def setup_args():
    global args
    args = parser.parse_args()

    if not args.names:
        names_input = input("Enter comma separated names (first will be first driver): ")
        args.names = [names_input] 

    args.names = [n.strip() for name in args.names for n in name.split(",") if n.strip()]

PROMPT = [
    ("Press ", 0),
    ("s", curses.A_BOLD),
    (" to (", 0),
    ("s", curses.A_BOLD),
    (")kip this session, ", 0),
    ("p", curses.A_BOLD),
    (" to (", 0),
    ("p", curses.A_BOLD),
    (")ause it, or ", 0),
    ("b", curses.A_BOLD),
    (" for a (", 0),
    ("b", curses.A_BOLD),
    (")reak:", 0)
]


async def confirm_action(display: Display, prompt: str, message_line: int) -> bool:
    """Show confirmation dialog and return True if confirmed, False if cancelled"""
    display.update_line(message_line, f"{prompt} (y/n): ")
    
    while True:
        ch = display.stdscr.getch()
        if ch != -1:
            if ch in (ord('y'), ord('Y')):
                return True
            elif ch in (ord('n'), ord('N')):
                display.update_line(message_line, "")
                return False
        await asyncio.sleep(0.05)


async def countdown_timer(display: Display, duration_seconds: int, current_driver: str, next_driver: str):
    """Generic countdown timer with skip, pause, and break functionality"""
    is_paused = False
    pause_time = 0
    message_clear_time = 0  # Time when to clear temporary messages
    
    # Initial display using lines array pattern
    lines = [
        [("Driver: ", 0), (current_driver, curses.A_BOLD)],
        f"Next driver: {next_driver}",
        "⏰ Time remaining: --:--",
        "",
        PROMPT,
        "",  # Cursor position line
        ""   # Message line
    ]
    display.show(lines)
    
    # Calculate line positions based on the layout
    time_line = 2  # Time is always on line 2
    input_line = 4  # Input prompt is on line 4
    cursor_line = 5  # Cursor position below prompt
    message_line = 6  # Message goes after cursor
    
    # Time-based countdown
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + duration_seconds
    last_update = 0
    
    try:
        while True:
            current_time = asyncio.get_event_loop().time()
            
            # Handle pause logic
            if is_paused:
                # When paused, freeze the remaining time
                if pause_time == 0:
                    # Just entered pause - calculate and freeze remaining time
                    remaining = max(0, int(end_time - current_time))
                # else: keep the same remaining time (frozen)
            else:
                # When not paused, calculate normally
                remaining = max(0, int(end_time - current_time))
            
            # Clear temporary messages after delay
            if message_clear_time > 0 and current_time >= message_clear_time:
                display.update_line(message_line, "")
                message_clear_time = 0
            
            # Update display only when the second changes
            if remaining != last_update:
                minutes, seconds = divmod(remaining, 60)
                # Update time with bold formatting and pause indicator
                status_text = "⏰ Time remaining: " if not is_paused else "⏸️  PAUSED - Time: "
                time_parts = [
                    (status_text, 0),
                    (f" {minutes:02d}:{seconds:02d}", curses.A_BOLD)
                ]
                display.update_line(time_line, time_parts)
                # Position cursor on the cursor line
                display.stdscr.move(cursor_line, 0)
                last_update = remaining
                
                # Check if time is up (only when not paused)
                if remaining <= 0 and not is_paused:
                    display.update_line(message_line, f"Session complete! Press any key to continue...")
                    return "completed"
            
            # Handle input (fast response time)
            ch = display.stdscr.getch()
            if ch != -1:
                if ch in (ord('s'), ord('S')):
                    if await confirm_action(display, "Skip session?", message_line):
                        display.update_line(message_line, f"Session skipped! Press any key to continue...")
                        return "skipped"
                elif ch in (ord('r'), ord('R'), ord('u'), ord('U')) and is_paused:
                    # Resume session when paused (r, u keys)
                    if await confirm_action(display, "Resume session?", message_line):
                        # Calculate new end time based on remaining time
                        current_resume_time = asyncio.get_event_loop().time()
                        end_time = current_resume_time + remaining
                        is_paused = False
                        pause_time = 0
                        # Restore original prompt
                        display.update_line(input_line, PROMPT)
                        display.update_line(message_line, "Session resumed")
                        message_clear_time = current_resume_time + 2  # Clear after 2 seconds
                elif ch in (ord('p'), ord('P')):
                    if is_paused:
                        # Also handle 'p' when paused to resume
                        if await confirm_action(display, "Resume session?", message_line):
                            # Calculate new end time based on remaining time
                            current_resume_time = asyncio.get_event_loop().time()
                            end_time = current_resume_time + remaining
                            is_paused = False
                            pause_time = 0
                            # Restore original prompt
                            display.update_line(input_line, PROMPT)
                            display.update_line(message_line, "Session resumed")
                            message_clear_time = current_resume_time + 2  # Clear after 2 seconds
                    else:
                        if await confirm_action(display, "Pause session?", message_line):
                            is_paused = True
                            pause_time = current_time
                            # Update prompt to show resume options with bold 'r'
                            resume_prompt = [
                                ("Session paused: press ", 0),
                                ("r", curses.A_BOLD),
                                (" to (", 0),
                                ("r", curses.A_BOLD),
                                (")esume the session timer", 0)
                            ]
                            display.update_line(input_line, resume_prompt)
                            display.update_line(message_line, "")
                elif ch in (ord('b'), ord('B')):
                    if await confirm_action(display, "Take immediate break?", message_line):
                        display.update_line(message_line, f"Taking break! Press any key to continue...")
                        return "break"
            
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
    
    # Break configuration display
    if args.break_duration > 0:
        display.stdscr.addstr(row, 0, f"Break Duration: ")
        break_duration = timedelta(seconds=args.break_duration * 60)
        display.stdscr.addstr(row, 16, str(break_duration), curses.A_BOLD)
        row += 1
        display.stdscr.addstr(row, 0, f"Break Every: ")
        break_every_str = f"{args.break_every} session{'s' if args.break_every > 1 else ''}"
        display.stdscr.addstr(row, 14, break_every_str, curses.A_BOLD)
        row += 1
    else:
        display.stdscr.addstr(row, 0, "Break Mode: ")
        display.stdscr.addstr(row, 12, "Disabled", curses.A_DIM)
        row += 1
    
    if not is_pomodoro:
        row += 1  # Empty line
        display.stdscr.addstr(row, 0, "Driver rotation:")
        row += 1
        for i, name in enumerate(args.names):
            prefix = "→ " if i == state.driver_index else "  "
            display.stdscr.addstr(row, 0, prefix)
            if i == state.driver_index:
                display.stdscr.addstr(row, 2, name, curses.A_BOLD)
            else:
                display.stdscr.addstr(row, 2, name)
            row += 1
    
    row += 1  # Empty line
    display.stdscr.addstr(row, 0, "Press any key to start the session timer...")
    display.stdscr.refresh()


async def handle_session_complete(state: SessionState, is_pomodoro: bool, skipped: bool = False):
    """Handle end of session notifications and break logic"""
    state.session_count += 1
    state.driver_times = {} if not state.driver_times else state.driver_times
    state.driver_times[args.names[state.driver_index]] += args.duration
    
    # Notifications (only if session wasn't skipped)
    if not skipped:
        NotificationManager.play_sound()
        if not is_pomodoro:
            next_driver_name = args.names[(state.driver_index + 1) % len(args.names)]
            NotificationManager.say(f"{next_driver_name} is next driver")
            NotificationManager.show_notification("Mob Timer", f"Session complete! {next_driver_name} is next driver")
        else:
            NotificationManager.show_notification("Pomodoro Timer", "Session complete! Take a break")
    
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
            
            if result == "completed":
                await handle_session_complete(state, is_pomodoro, skipped=False)
                
                # Break logic
                if state.session_count % args.break_every == 0 and args.break_duration > 0:
                    next_driver_name = args.names[state.driver_index] if not is_pomodoro else None
                    await break_timer(display, args.break_duration * 60, is_pomodoro, next_driver_name)
                else:
                    show_transition_screen(display, state, is_pomodoro)
            elif result == "skipped":
                await handle_session_complete(state, is_pomodoro, skipped=True)
                # Skip transition screen for skipped sessions - go directly to main screen
            elif result == "break":
                # Immediate break requested - don't advance driver or count session
                if args.break_duration > 0:
                    next_driver_name = args.names[state.driver_index] if not is_pomodoro else None
                    await break_timer(display, args.break_duration * 60, is_pomodoro, next_driver_name)
                else:
                    display.show(["Break requested but no break duration set!", "Continuing session..."])
                    await asyncio.sleep(2)
                    
    except (KeyboardInterrupt, asyncio.CancelledError):
        display.show(["👋 Mob session ended. Thanks for coding together!"])
        await asyncio.sleep(2)

def show_transition_screen(display: Display, state: SessionState, is_pomodoro: bool):
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
    display.show(lines)


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
                    if is_pomodoro:
                        NotificationManager.show_notification("Pomodoro Timer", "Break complete! Ready for next session")
                    else:
                        NotificationManager.show_notification("Mob Timer", f"Break complete! {next_driver_name} is ready to drive")
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
