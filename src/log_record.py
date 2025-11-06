# Each line is: <timestamp_ms> <METHOD> <PATH> <status> <latency_ms>

from dataclasses import dataclass

'''
A dataclass in Python is a special kind of class that's meant for storing data like a lightweight struct in C

It automatically generates for you:
- an __init__ constructor
- a readable __repr__ (print-friendly string)
- comparison methods like __eq__, __lt__, etc. (if you want them)
- type checking hints (via type annotations)

'''

#Frozen true makes this data immutable
@dataclass(frozen=True)
class LogRecord:
    ts_ms: int
    endpoint: str
    status: int
    latency_ms: int

    #Now, we will change the string into an object
    '''
    Using "LogRecord" instead of LogRecord (as a variable type) because of forward reference, the python interpreter will save
    as "metadata" that the returning type must be a LogRecord. If we try to use LogRecord before the class is fully defined,
    it will return an error
    '''
    @staticmethod
    def from_line(line: str) -> "LogRecord":
        parts = line.strip().split()
        if len(parts) != 5:
            #Using the 'f' before the "<string>" to evaluate brackets expressions
            raise ValueError(f"bad line: {line!r}")
        ts_ms = int(parts[0])
        method = parts[1]
        path = parts[2]
        status = int(parts[3])
        latency = int(parts[4])
        return LogRecord(ts_ms, f"{method} {path}", status, latency)

'''
    #Example: 1730851200001 "GET /api/login" 200 42
    rec = LogRecord(1730851200001, "GET /api/login", 200, 42)

    print(rec.endpoint)
    print(rec)
'''