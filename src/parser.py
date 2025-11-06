from typing import Iterable, Iterator
from .log_record import LogRecord
import sys


#Iterable: Any object you can loop over using a for loop
#Iterator Gives items one by one (result of iter(list) or a generator function)
def parse_lines(lines: Iterable[str]) -> Iterator[LogRecord]:
    for ln in lines:
        if not ln or not ln.strip():
            continue
        
        #Use yield instead of return, "yield" is like a return but lazy, it wont generate until you actually call it
        yield LogRecord.from_line(ln)


def parse_file(path: str, strict: bool = True) -> Iterator[LogRecord]:
    """Open a text file and yield LogRecord objects for each line.
    strict=True -> raise on malformed; strict=False -> skip bad lines and log count.
    """
    skipped = 0
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            if not ln.strip():
                continue
            try:
                yield LogRecord.from_line(ln)
            except ValueError:
                if strict:
                    raise
                skipped += 1
    if not strict and skipped:
        print(f"[info] {path}: skipped malformed lines: {skipped}", file=sys.stderr)