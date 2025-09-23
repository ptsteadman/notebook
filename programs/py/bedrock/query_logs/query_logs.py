import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
"""
maybe streaming
parse logs
error handling

start with single file

cli with arguments for --service, --level, --start, --end

console out log lines

level -> [ids]
service -> [ids]

having logs sorted by time in parsing enables binary sort of logs
"""

@dataclass(slots=True)
class LogLine:
    ts : datetime
    level: str
    service: str
    message: str
    raw: str

    def __str__(self):
        return self.raw

class LogQuerier:
    def __init__(self, path):
        self.path = path

    def parse_logs(self, f):
        while (l := f.readline()):
            date_, level, service, message = l.split(' ', 3)
            yield LogLine(datetime.fromisoformat(date_), level, service, message, l)

    def query(self, level=None, service=None, start=None, end=None):
        p = Path(self.path)
        for file in p.iterdir():
            with file.open() as f:
                for l in self.parse_logs(f):
                    if level and l.level != level:
                        continue
                    if service and l.service != service:
                        continue
                    if start and l.ts < start:
                        continue
                    if end and l.ts > end:
                        continue
                    yield l


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to log file directory.")
    parser.add_argument("--service", type=str, default=None, help="Filter by service name.")
    parser.add_argument("--level", type=str, default=None, help="Filter by log level.")
    parser.add_argument("--start", type=str, default=None, help="Filter by log time (start limit).")
    parser.add_argument("--end", type=str, default=None, help="Filter by log time (end limit).")
    args = parser.parse_args()

    q = LogQuerier(args.path)
    it = q.query(
        level=args.level,
        service=args.service,
        start=datetime.fromisoformat(args.start) if args.start else None,
        end=datetime.fromisoformat(args.end) if args.end else None
    )
    for l in it:
        print(l, end="")

if __name__ == "__main__":
    main()
