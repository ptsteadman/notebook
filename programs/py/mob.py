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


async def countdown(duration_seconds: int):
    try:
        for remaining in range(duration_seconds, 0, -1):
            minutes = remaining // 60
            seconds = remaining % 60
            print(f"\r⏰ Time remaining: {minutes:02d}:{seconds:02d}", end="", flush=True)
            await asyncio.sleep(1)
        print(f"\r⏰ Time remaining: 00:00", flush=True)
    except asyncio.CancelledError:
        print(f"\r⏰ Session interrupted", flush=True)
        raise

async def mob(session_duration: timedelta):
    driver_index = 0
    try:
        while True:
            print(f"Driver: {args.names[driver_index]}")
            print(f"Code for {session_duration}...")
            
            await countdown(session_duration.seconds)
            
            next_driver = (driver_index + 1) % len(args.names)
            try:
                subprocess.run(
                    ["say", f"Session complete, {args.names[next_driver]} is driver now!"], check=True
                )
            except (subprocess.CalledProcessError) as e:
                print("Session complete, time to switch drivers.")
            print(f"Done! Press enter to continue")
            await get_input()
            driver_index = next_driver
    except (KeyboardInterrupt, asyncio.CancelledError):
        print(f"\n\n👋 Mob session ended. Thanks for coding together!")
        return

async def get_input():
    await asyncio.to_thread(sys.stdin.readline) 

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
