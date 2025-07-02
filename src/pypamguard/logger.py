import enum
from contextlib import contextmanager
import sys
import time

class Verbosity(enum.IntEnum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4

@contextmanager
def logger_config(verbosity: Verbosity):
    old_verbosity = logger.verbosity
    logger.set_verbosity(verbosity)
    yield
    logger.set_verbosity(old_verbosity)

class Logger:

    def __init__(self):
        self.verbosity = Verbosity.INFO

    def start_progress_bar(self, limit: int, name: str = "Progress", unit: str = "bytes", scale: int = 1, rounding = 2, show_info = True):
        self.progress_name = name
        self.progress_limit = limit
        self.scaled_progress_limit = round(limit * scale, rounding)
        self.progress_increment = limit / 20
        self.progress_unit = unit
        self.progress_scale = scale
        self.start_time = time.time()
        self.units_per_second = 0
        self.rounding = rounding
        self.last_update_time = time.time()
        self.show_info = show_info
        self.perc = 0
        self.suffix = ""
        self.eta = 0
        self.log_progress(0)

    def log_progress(self, value: int, message: str = ""):
        current_time = time.time()
        current_prog = round(value * self.progress_scale, self.rounding)
        perc = int(100 * value / self.progress_limit)
        
    def start_progress_bar(self, limit: int, name: str = "Progress", unit: str = "bytes", scale: int = 1, rounding: int = 2, show_info: bool = True):
        self.progress_name = name
        self.progress_limit = limit
        self.scaled_progress_limit = round(limit * scale, rounding)
        self.progress_increment = limit / 20
        self.progress_unit = unit
        self.progress_scale = scale
        self.start_time = time.time()
        self.rounding = rounding
        self.show_info = show_info
        self.log_progress(0)

    def log_progress(self, value: int, message: str = ""):
        if value == 0:
            self.last_update_time = time.time()
            self.perc = 0
            self.units_per_second = 0
            self.eta = 0
            self.total_time = 0

        current_time = time.time()
        current_prog = round(value * self.progress_scale, self.rounding)
        perc = int(100 * value / self.progress_limit)

        if perc >= 100 or perc > self.perc:
            self.total_time = time.time() - self.start_time

            if perc >= 100:
                perc = 100
                self.suffix = f"completed in {self.total_time:.2f} s\n"
            else:
                if current_time - self.last_update_time < 0.15:
                    return
                self.last_update_time = current_time
                self.units_per_second = round(self.progress_scale * value / self.total_time, self.rounding)
                self.eta = self.total_time * (self.progress_limit - value) / value

        if perc < 100:
            self.suffix = f"eta {self.eta:.0f} s"

        self.perc = perc

        if self.show_info:
            message = f"{current_prog:.{self.rounding}f}/{self.scaled_progress_limit:.{self.rounding}f} {self.progress_unit} | {self.units_per_second:.{self.rounding}f} {self.progress_unit}/s | {self.suffix}     "

        if self.verbosity < Verbosity.DEBUG:
            sys.stdout.write(f"\r[PROGRESS] {self.progress_name} [{'=' * int(perc // 5) + ' ' * int((self.progress_limit - value)/ self.progress_increment)}] {perc}% {message}")
            sys.stdout.flush()        


    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def _log(self, level, message):
        lines = message.split('\n')
        print(f"[{level}] {lines[0]}")
        for line in lines[1:]:
            print(f"\t{line}")

    def info(self, message):
        if self.verbosity >= Verbosity.INFO:
            self._log("INFO", message)

    def debug(self, message):
        if self.verbosity >= Verbosity.DEBUG:
            self._log("DEBUG", message)

    def warning(self, message):
        if self.verbosity >= Verbosity.WARNING:
            self._log("WARNING", message)

    def error(self, message):
        self._log("ERROR", message)

logger = Logger()
