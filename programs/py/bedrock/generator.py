import argparse
from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import Iterable
from uuid import uuid4


LEVELS = ("ERROR", "WARNING", "INFO", "DEBUG")

SERVICES = ("auth", "payment", "app", "backend")

MESSAGES = {
    "ERROR": ("Failed to process request", "Resource not found"),
    "WARNING": ("Cache miss for key", "Memory usage threshold exceeded"),
    "INFO": ("User logged in successfully", "Database connection established"),
    "DEBUG": ("Data validation complete", "Background task scheduled"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="logs", help="Output directory for logs.")
    parser.add_argument("--log-count", type=int, default=16, help="Number of logs to generate.")
    parser.add_argument("--line-count", type=int, default=100000, help="Number of lines per log.")
    args = parser.parse_args()

    dir = Path(args.path)
    dir.mkdir(parents=True, exist_ok=True)

    random.seed(42)

    for i in range(args.log_count):
        offset = timedelta(seconds=i)
        generate_file(
            path=dir / f"test_{i:05d}.log",
            start=datetime(2025, 2, 1, 0, 0, 0) + offset,
            end=datetime(2025, 3, 1, 0, 0, 0) + offset,
            count=args.line_count
        )


def generate_file(path: Path, start: datetime, end: datetime, count: int):
    """Generate a log file at the specified path."""
    with open(path, "w") as f:
        for timestamp in iter_timestamps(start, end, count):
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            level = random.choice(LEVELS)
            service = random.choice(SERVICES) + "-service"
            message = random.choice(MESSAGES[level]) + ": " + str(uuid4())
            if service == "app-service":
                message += f" [response_time={random.randint(1, 1000)}ms]"

            f.write(f"{timestamp} {level} {service} {message}\n")


def iter_timestamps(start: datetime, end: datetime, count: int) -> Iterable[datetime]:
    """Iterate timestamps in equal intervals between [start, end)."""
    interval = (end - start) / count
    for i in range(count):
        yield start + i * interval


if __name__ == "__main__":
    main()
