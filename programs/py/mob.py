"""
TODO:
- [] implement looping
- [] implement interrupt/cancellation/skip
- [] show countdown

"""
import argparse
import sys
from datetime import timedelta
import asyncio
import subprocess


parser = argparse.ArgumentParser("mob.py", "specify input time and people")
parser.add_argument("-d", "--duration", default="10", type=float)
parser.add_argument("-n", "--names", nargs="+", action="extend", type=str)
args = parser.parse_args()


async def mob(session_duration: timedelta):
    driver_index = 0
    while True:
        print(f"Driver: {args.names[driver_index]}")
        print(f"Code for {session_duration}...")
        await asyncio.sleep(session_duration.seconds)
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

async def get_input():
    await asyncio.to_thread(sys.stdin.readline) 

asyncio.run(mob(timedelta(seconds=args.duration * 60)))