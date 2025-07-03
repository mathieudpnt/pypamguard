import enum
from contextlib import contextmanager
import sys
import time
import resource
import psutil

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


class ProgressBar:

    def __init__(self, name: str, limit: int, scale: int = 1, unit: str = "units", rounding: int = 0):
        """
        Create a progress bar that prints to the terminal. The progress bar can be configured
        by passing in parameters to the constructor or `start()` method. The value of the
        bar can then be updated by calling the `update()` method. Once completed, either pass
        in a value to `update()` equal to or greater than `limit`, or call `complete()`.

        :param name: The name of the progress bar.
        :param limit: The maximum value of the progress bar.
        :param scale: A scaling factor for printing `limit` (for example, if `limit` is in bytes
                        but you want to print in MB, set `scale` to 1/1024 ** 2).
        :param unit: The unit of `limit` after applying `scale`.
        :param rounding: How many decimal points to round values printed in the progress bar to.
        """
        self.limit = limit
        self.scale = scale
        self.unit = unit
        self.name = name
        self.rounding = rounding
        self.start()
        self.process = psutil.Process()


    def __print(self, message):
        sys.stdout.write(f"\r[PROGRESS] {self.name} [{'=' * int(self.perc // 5) + ' ' * int((100 - self.perc) // 5)}] {self.perc}% {message}")
        sys.stdout.flush()        
        
    def start(self):
        self.start_time = time.time()
        self.last_updated_time = self.start_time
        self.update(0)
    
    def __message(self, suffix):
        return f"{(self.value*self.scale):.{self.rounding}f}/{(self.limit*self.scale):.{self.rounding}f} {self.unit} | {self.units_per_second:.{self.rounding}f} {self.unit}/s | mem {self.mem_usage_kb:.0f} KB | {suffix}"

    def update(self, value):        
        if time.time() - self.last_updated_time <= 0.1 and not value == self.limit: return
        self.last_updated_time = time.time()
        self.value = value
        self.perc = round(100 * self.value / self.limit, 2)
        self.total_time = self.last_updated_time - self.start_time
        self.units_per_second = round(self.scale * value / self.total_time, self.rounding)
        mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.mem_usage_kb = self.process.memory_info().rss / (1024)

        eta = round((self.limit - self.value) * self.scale / self.units_per_second, 0) if self.units_per_second > 0 else -1
        self.__print(self.__message(f"eta {eta:.0f} s    " if eta > 0 else "eta"))

    def complete(self):
        self.update(self.limit)
        self.__print(self.__message(f"completed in {self.total_time:.2f} s\n"))

class Logger:

    def __init__(self):
        self.verbosity = Verbosity.INFO

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
