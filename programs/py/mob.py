"""
Use asyncio to manage async tasks.

TODO:
- [] implement looping
- [] implement interrupt/cancellation/skip
- [] show countdown
- [] solo pomodoro mode

"""
import argparse
import sys
from datetime import timedelta
import asyncio
import subprocess
import signal


parser = argparse.ArgumentParser("mob.py", "specify input time and people")
parser.add_argument("-d", "--duration", default="10", type=float)
parser.add_argument("-n", "--names", nargs="*", action="extend", type=str)
args = parser.parse_args()

if not args.names:
    names_input = input("Enter comma separated names (first will be first driver): ")
    args.names = [name.strip() for name in names_input.split(",") if name.strip()]


import threading
import queue

# Global queue for input
input_queue = queue.Queue()
input_thread = None

def input_listener():
    """Background thread to listen for input"""
    while True:
        try:
            line = sys.stdin.readline()
            if line:
                input_queue.put(line.strip().lower())
        except:
            break

async def countdown(duration_seconds: int, next_driver):
    global input_thread
    
    # Start input listener thread if not already running
    if input_thread is None or not input_thread.is_alive():
        input_thread = threading.Thread(target=input_listener, daemon=True)
        input_thread.start()
    
    # Clear any pending input from the queue
    while True:
        try:
            input_queue.get_nowait()
        except queue.Empty:
            break
    
    try:
        for remaining in range(duration_seconds, 0, -1):
            minutes = remaining // 60
            seconds = remaining % 60
            print(f"\r⏰ Time remaining: {minutes:02d}:{seconds:02d} (type 'n' + enter to skip)", end="", flush=True)
            
            # Check for input without blocking
            try:
                user_input = input_queue.get_nowait()
                if user_input == 'n':
                    print(f"\r⏰ Session skipped! Press enter to start timer for {args.names[next_driver]}                                              ")
                    return
            except queue.Empty:
                pass
            
            await asyncio.sleep(1)
                    
        print(f"\r⏰ Time remaining: 00:00                                              ")
    except asyncio.CancelledError:
        print(f"\r⏰ Session interrupted                                              ")
        raise

async def mob(session_duration: timedelta):
    driver_index = 0
    try:
        while True:
            print(f"Driver: {args.names[driver_index]}")
            print(f"Code for {session_duration}...")
            next_driver = (driver_index + 1) % len(args.names)
            
            await countdown(session_duration.seconds, next_driver)
            
            try:
                subprocess.run(
                    ["say", f"Session complete, {args.names[next_driver]} is driver now!"], check=True
                )
            except (subprocess.CalledProcessError) as e:
                print("Session complete, time to switch drivers.")
            await get_input()
            driver_index = next_driver
    except (KeyboardInterrupt, asyncio.CancelledError):
        print(f"\n\n👋 Mob session ended. Thanks for coding together!")
        return

async def get_input():
    global input_thread
    
    # Start input listener thread if not already running
    if input_thread is None or not input_thread.is_alive():
        input_thread = threading.Thread(target=input_listener, daemon=True)
        input_thread.start()
    
    # Wait for any input from the queue
    while True:
        try:
            input_queue.get_nowait()
            return  # Got input, continue
        except queue.Empty:
            await asyncio.sleep(0.1)  # Wait a bit and check again 

async def main():
    try:
        await mob(timedelta(seconds=args.duration * 60))
    except KeyboardInterrupt:
        print(f"\n\n👋 Mob session ended. Thanks for coding together!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
