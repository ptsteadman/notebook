"""Mob programming timer with async support and curses interface.

Mob programming is a collaborative software development practice where multiple
developers work together wth a single "screen". One person acts as the "driver"
(typing the code or modifying configuration) while others act as "navigators" (providing guidance and review).
This timer manages session rotation to ensure everyone stays engaged, while being flexible enough to
handle breaks and skipping sessions.

It only uses the python standard library because it's meant to be a portable script 
that I can send to collaborators. 

It's also meant to be modifiable by the team based on workflow: often times, we'll want to perform
some automation like commiting/pushing a git branch, but this typically varies greatly based on
project. Or sometimes people have different preferences/needs for notifications and reminders.

I chose async instead of threads because I wanted to better understand python's async model.

NOTE: sound, voice and banner notifications only supported on OSX!
"""
import argparse
from datetime import timedelta
import asyncio
import subprocess
import curses
from dataclasses import dataclass
from typing import Dict, Optional

def main():
    parser = argparse.ArgumentParser(
        "mob.py", 
        description="A curses-based timer for mob programming sessions. Only supports OSX at present."
    )
    parser.add_argument("-d", "--duration", default="10", type=float)
    parser.add_argument("-b", "--break", dest="break_duration", default="0", type=float, help="Break duration (default 0, no break)")
    parser.add_argument("-e", "--break-every", dest="break_every", default="1", type=int, help="Take a break every N sessions (default: 1)")
    parser.add_argument("--no-voice", dest="voice_enabled", action="store_false", help="Disable voice announcements")
    parser.add_argument("--no-notifications", dest="notifications_enabled", action="store_false", help="Disable native macOS notifications")
    parser.add_argument("-n", "--names", nargs="*", action="extend", type=str)
    
    args = parser.parse_args()

    if not args.names:
        names_input = input("Enter comma separated names (first will be first driver): ")
        args.names = [names_input] 

    args.names = [n.strip() for name in args.names for n in name.split(",") if n.strip()]

    def curses_main(stdscr):
        curses.curs_set(1)
        stdscr.nodelay(1)
        stdscr.clear()
        
        display = Display(stdscr)
        timer = MobManager(
            display=display,
            session_duration=timedelta(seconds=args.duration * 60),
            names=args.names,
            break_duration=args.break_duration,
            break_every=args.break_every,
            voice_enabled=args.voice_enabled,
            notifications_enabled=args.notifications_enabled
        )
        asyncio.run(timer.run())
    
    curses.wrapper(curses_main)



@dataclass
class SessionState:
    driver_index: int = 0
    session_count: int = 0
    driver_times: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        if self.driver_times is None:
            self.driver_times = {}


class Display:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
    def show(self, lines):
        self.stdscr.clear()
        for i, line in enumerate(lines):
            if isinstance(line, str):
                self.stdscr.addstr(i, 0, line)
            else:
                col = 0
                for text, attrs in line:
                    self.stdscr.addstr(i, col, text, attrs)
                    col += len(text)
        self.stdscr.refresh()
        
    def update_line(self, row, content, attrs=0):
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()
        
        if isinstance(content, str):
            self.stdscr.addstr(row, 0, content, attrs)
        else:
            col = 0
            for text, part_attrs in content:
                self.stdscr.addstr(row, col, text, part_attrs)
                col += len(text)
        
        self.stdscr.refresh()


class NotificationManager:
    @staticmethod
    async def play_alert_sequence():
        for _ in range(3):
            try:
                subprocess.run(["afplay", "/System/Library/Sounds/Hero.aiff"], check=True)
                await asyncio.sleep(0.1)
            except subprocess.CalledProcessError:
                pass
            
    @staticmethod
    def say(message, voice_enabled=True):
        if voice_enabled:
            try:
                subprocess.run(["say", message], check=True)
            except subprocess.CalledProcessError:
                pass
    
    @staticmethod
    def show_notification(title, message, sound=None, notifications_enabled=True):
        if not notifications_enabled:
            return
            
        try:
            # Escape quotes in the message and title
            safe_title = title.replace('"', '\\"')
            safe_message = message.replace('"', '\\"')
            
            applescript = f'display notification "{safe_message}" with title "{safe_title}"'
            if sound:
                applescript += f' sound name "{sound}"'
            
            subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            pass

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



class MobManager:
    def __init__(self, display: Display, session_duration: timedelta, names: list, break_duration: float, break_every: int, voice_enabled: bool, notifications_enabled: bool):
        self.display = display
        self.session_duration = session_duration
        self.names = names
        self.break_duration = break_duration
        self.break_every = break_every
        self.voice_enabled = voice_enabled
        self.notifications_enabled = notifications_enabled
        self.state = SessionState()
        self.is_pomodoro = len(names) == 1
        
        # Initialize driver times
        if not self.state.driver_times:
            self.state.driver_times = {name: 0.0 for name in names}
        
        # Timer state variables
        self.is_paused = False
        self.pause_time = 0
        self.end_time = 0
        
    async def run(self):
        try:
            while True:
                self._show_main_screen()
                await get_input(self.display)
                
                current_driver = self.names[self.state.driver_index]
                next_driver = self.names[(self.state.driver_index + 1) % len(self.names)]
                result = await self._countdown_timer(int(self.session_duration.total_seconds()), current_driver, next_driver)
                
                if result == "completed":
                    await self._handle_session_complete(skipped=False)
                    if self.state.session_count % self.break_every == 0 and self.break_duration > 0:
                        next_driver_name = self.names[self.state.driver_index] if not self.is_pomodoro else None
                        await self._break_timer(int(self.break_duration * 60), next_driver_name)
                    else:
                        self._show_transition_screen()
                elif result == "skipped":
                    await self._handle_session_complete(skipped=True)
                elif result == "break":
                    if self.break_duration > 0:
                        next_driver_name = self.names[self.state.driver_index] if not self.is_pomodoro else None
                        await self._break_timer(int(self.break_duration * 60), next_driver_name)
                    else:
                        self.display.show(["Break requested but no break duration set!", "Continuing session..."])
                        await asyncio.sleep(2)
                        
        except (KeyboardInterrupt, asyncio.CancelledError):
            self.display.show(["👋 Mob session ended. Thanks for coding together!"])
            await asyncio.sleep(1)
    
    def _show_main_screen(self):
        lines = []
        
        if self.is_pomodoro:
            lines.extend([
                [("🍅 Pomodoro Session", curses.A_BOLD)],
                "Solo Focus Time"
            ])
        else:
            lines.extend([
                [("🚗 Mob Programming Session", curses.A_BOLD)],
                [("Current Driver: ", 0), (self.names[self.state.driver_index], curses.A_BOLD)]
            ])
        
        lines.append([("Session Duration: ", 0), (str(self.session_duration), curses.A_BOLD)])
        
        if self.break_duration > 0:
            break_duration = timedelta(seconds=self.break_duration * 60)
            break_every_str = f"{self.break_every} session{'s' if self.break_every > 1 else ''}"
            lines.extend([
                [("Break Duration: ", 0), (str(break_duration), curses.A_BOLD)],
                [("Break Every: ", 0), (break_every_str, curses.A_BOLD)]
            ])
        else:
            lines.append([("Break Mode: ", 0), ("Disabled", curses.A_DIM)])
        
        if not self.is_pomodoro:
            lines.extend([
                "",
                "Driver rotation:"
            ])
            for i, name in enumerate(self.names):
                prefix = "→ " if i == self.state.driver_index else "  "
                if i == self.state.driver_index:
                    lines.append([(prefix, 0), (name, curses.A_BOLD)])
                else:
                    lines.append(f"{prefix}{name}")
        
        lines.extend([
            "",
            "Press any key to start the session timer..."
        ])
        
        self.display.show(lines)
    
    async def _handle_session_complete(self, skipped: bool = False):
        self.state.session_count += 1
        self.state.driver_times = {} if not self.state.driver_times else self.state.driver_times
        self.state.driver_times[self.names[self.state.driver_index]] += self.session_duration.total_seconds() / 60
        
        if not skipped:
            asyncio.create_task(NotificationManager.play_alert_sequence())
            if not self.is_pomodoro:
                next_driver_name = self.names[(self.state.driver_index + 1) % len(self.names)]
                NotificationManager.say(f"{next_driver_name} is next driver", self.voice_enabled)
                NotificationManager.show_notification(
                    "Mob Timer", 
                    f"Session complete! {next_driver_name} is next driver", 
                    notifications_enabled=self.notifications_enabled
                )
            else:
                NotificationManager.show_notification(
                    "Pomodoro Timer", 
                    "Session complete! Take a break", 
                    notifications_enabled=self.notifications_enabled
                )
        
        self.state.driver_index = (self.state.driver_index + 1) % len(self.names)
    
    def _show_transition_screen(self):
        lines = []
        if self.is_pomodoro:
            lines.extend([
                f"🍅 Session {self.state.session_count} complete!",
            ])
            if self.break_duration > 0:
                lines.append(f"Next break in {self.break_every - (self.state.session_count % self.break_every)} sessions")
        else:
            lines.extend([
                f"🔄 Session {self.state.session_count} complete!",
                f"Next driver: {self.names[self.state.driver_index]}",
            ])
            if self.break_duration > 0:
                lines.append(f"Next break in {self.break_every - (self.state.session_count % self.break_every)} sessions")
        self.display.show(lines)

    async def _countdown_timer(self, duration_seconds: int, current_driver: str, next_driver: str):
        # Reset timer state
        self.is_paused = False
        self.pause_time = 0
        message_clear_time = 0
        
        lines = [
            [("Driver: ", 0), (current_driver, curses.A_BOLD)],
            f"Next driver: {next_driver}",
            "⏰ Time remaining: --:--",
            "",
            PROMPT,
            "",
            ""
        ]
        self.display.show(lines)
        
        time_line = 2
        input_line = 4
        cursor_line = 5
        message_line = 6
        
        start_time = asyncio.get_event_loop().time()
        self.end_time = start_time + duration_seconds
        last_update = 0
        remaining = 0
        frozen_remaining = 0
        
        
        async def handle_timer_input():
            nonlocal message_clear_time
            ch = self.display.stdscr.getch()
            if ch != -1:
                if ch in (ord('s'), ord('S')):
                    if await confirm_action(self.display, "Skip session?", message_line):
                        self.display.update_line(message_line, f"Session skipped! Press any key to continue...")
                        return "skipped"
                elif ch in (ord('r'), ord('R'), ord('u'), ord('U')) and self.is_paused:
                    if await confirm_action(self.display, "Resume session?", message_line):
                        current_resume_time = asyncio.get_event_loop().time()
                        self.end_time = current_resume_time + remaining
                        self.is_paused = False
                        self.pause_time = 0
                        self.display.update_line(input_line, PROMPT)
                        self.display.update_line(message_line, "Session resumed")
                        message_clear_time = current_resume_time + 2
                elif ch in (ord('p'), ord('P')):
                    if await confirm_action(self.display, "Pause session?", message_line):
                        self.is_paused = True
                        self.pause_time = current_time
                        resume_prompt = [
                            ("Session paused: press ", 0),
                            ("r", curses.A_BOLD),
                            (" to (", 0),
                            ("r", curses.A_BOLD),
                            (")esume the session timer", 0)
                        ]
                        self.display.update_line(input_line, resume_prompt)
                        self.display.update_line(message_line, "")
                elif ch in (ord('b'), ord('B')):
                    if await confirm_action(self.display, "Take immediate break?", message_line):
                        self.display.update_line(message_line, f"Taking break! Press any key to continue...")
                        return "break"
            return None
        
        try:
            while True:
                current_time = asyncio.get_event_loop().time()
                
                # Calculate remaining time
                calculated_remaining = max(0, int(self.end_time - current_time))
                
                if self.is_paused:
                    if self.pause_time == 0:
                        frozen_remaining = calculated_remaining
                    remaining = frozen_remaining
                else:
                    remaining = calculated_remaining
                    frozen_remaining = calculated_remaining
                
                # Clear expired messages
                if message_clear_time > 0 and current_time >= message_clear_time:
                    self.display.update_line(message_line, "")
                    message_clear_time = 0
                
                # Update display
                if remaining != last_update:
                    minutes, seconds = divmod(remaining, 60)
                    status_text = "⏰ Time remaining: " if not self.is_paused else "⏸️  PAUSED - Time: "
                    time_parts = [
                        (status_text, 0),
                        (f" {minutes:02d}:{seconds:02d}", curses.A_BOLD)
                    ]
                    self.display.update_line(time_line, time_parts)
                    self.display.stdscr.move(cursor_line, 0)
                    last_update = remaining
                    
                    if remaining <= 0 and not self.is_paused:
                        self.display.update_line(message_line, f"Session complete! Press any key to continue...")
                        return "completed"
                
                result = await handle_timer_input()
                if result:
                    return result
                
                await asyncio.sleep(0.05)
                            
        except asyncio.CancelledError:
            self.display.update_line(message_line, "Session interrupted")
            raise

    async def _break_timer(self, break_seconds: int, next_driver_name: Optional[str] = None):
        lines = [
            "🍅 Break time!" if self.is_pomodoro else "🔄 Break time!",
            "Take a short break" if self.is_pomodoro else f"Next driver will be: {next_driver_name or 'Unknown'}",
            "⏰ Break time remaining: --:--",
            "",
            "Press any key to skip break..."
        ]
        self.display.show(lines)
        
        start_time = asyncio.get_event_loop().time()
        end_time = start_time + break_seconds
        last_update = -1
        
        try:
            while True:
                current_time = asyncio.get_event_loop().time()
                remaining = max(0, int(end_time - current_time))
                
                if remaining != last_update:
                    minutes, seconds = divmod(remaining, 60)
                    self.display.update_line(2, f"⏰ Break time remaining: {minutes:02d}:{seconds:02d}")
                    last_update = remaining
                    
                    if remaining <= 0:
                        self.display.update_line(5, "Break complete! Ready for next session...")
                        if self.is_pomodoro:
                            NotificationManager.show_notification(
                                "Pomodoro Timer", 
                                "Break complete! Ready for next session", 
                                notifications_enabled=self.notifications_enabled
                            )
                        else:
                            NotificationManager.show_notification(
                                "Mob Timer", 
                                f"Break complete! {next_driver_name} is ready to drive", 
                                notifications_enabled=self.notifications_enabled
                            )
                        await asyncio.sleep(2)
                        return
                
                if self.display.stdscr.getch() != -1:
                    self.display.update_line(5, "Break skipped! Ready for next session...")
                    await asyncio.sleep(1)
                    return
                
                await asyncio.sleep(0.05)
                            
        except asyncio.CancelledError:
            self.display.update_line(5, "Break interrupted")
            raise


async def get_input(display: Display):
    while True:
        if display.stdscr.getch() != -1:
            return
        await asyncio.sleep(0.01)

async def get_input_with_reminders(display: Display):
    start_time = asyncio.get_event_loop().time()
    last_reminder = start_time
    reminder_interval = 2.5 * 60
    
    while True:
        if display.stdscr.getch() != -1:
            return
            
        current_time = asyncio.get_event_loop().time()
        if current_time - last_reminder >= reminder_interval:
            NotificationManager.say(
                "Press enter to continue with the next session", 
                voice_enabled=True
            )
            last_reminder = current_time
        
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    main()
