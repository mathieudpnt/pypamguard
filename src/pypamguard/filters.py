from dataclasses import dataclass
import datetime
import enum
from abc import ABC, abstractmethod

class FilterStopSkipException(Exception):
    pass

class FILTER_POSITION(enum.Enum):
    SKIP = 0 # ignore this object but keep reading
    KEEP = 1 # include this object
    STOP = 2 # ignore this, and all following objects

@dataclass
class FilterBinaryFile(ABC):

    @abstractmethod
    def check(self, value: any) -> FILTER_POSITION:
        raise NotImplementedError

class FilterUIDList(FilterBinaryFile):
    uid_list: list[int]

    def __init__(self, uid_list: list[int]):
        self.uid_list = uid_list
    
    def check(self, uid):
        if uid in self.uid_list:
            return FILTER_POSITION.KEEP
        return FILTER_POSITION.SKIP

class FilterUIDRange(FilterBinaryFile):

    def __init__(self, start_uid: int, end_uid: int, ignore_none: bool = False):
        self.__start_uid = start_uid
        self.__end_uid = end_uid
        self.__ignore_none = ignore_none
    
    def check(self, uid):
        if uid is None and not self.__ignore_none:
            return FILTER_POSITION.KEEP
        if uid < self.__start_uid or uid > self.__end_uid:
            return FILTER_POSITION.SKIP
        return FILTER_POSITION.KEEP

class FilterDate(FilterBinaryFile):

    def __init__(self, start_date: datetime.datetime, end_date: datetime.datetime, ignore_timezone: bool = False, ignore_none: bool = False):
        """
        Process a datetime object and return KEEP either when the date
        is between the start and end date or when the date is None. Return
        SKIP when the date is before the start date and STOP when the date
        is after the end date.
        """

        # Check that dates are given in UTC, raise exception if not
        if not ignore_timezone and (start_date.tzinfo is not datetime.timezone.utc or end_date.tzinfo is not datetime.timezone.utc):
            self.__err()
        self.__ignore_timezone = ignore_timezone
        self.__start_date = start_date
        self.__end_date = end_date
        self.__ignore_none = ignore_none

    def __err(self):
        raise ValueError("Ensure your dates are explicitly given in UTC.")

    def check(self, value: datetime.datetime):        
        if not value and not self.__ignore_none:
            return FILTER_POSITION.KEEP
        if not self.__ignore_timezone and value.tzinfo is not datetime.timezone.utc:
            self.__err()
        if value < self.__start_date:
            return FILTER_POSITION.SKIP
        if value > self.__end_date:
            return FILTER_POSITION.STOP
        return FILTER_POSITION.KEEP


INSTALLED_FILTERS = {
    'uidlist': FilterUIDList,
    'uidrange': FilterUIDList,
    'dateramge': FilterDate
}


class Filters:

    def __init__(self, filters: dict[str, FilterBinaryFile] = {}):
        for key, value in filters.items():
            self.__validate(key, value)

        self.__filters: dict[str, FilterBinaryFile] = filters
        self.position: FILTER_POSITION = None
    
    def __validate(self, key, value):
        if key in INSTALLED_FILTERS and not isinstance(value, INSTALLED_FILTERS[key]):
            raise ValueError(f"Filter {key} must be of type {INSTALLED_FILTERS[key]}")
        if key not in INSTALLED_FILTERS and not isinstance(value, FilterBinaryFile):
            raise ValueError(f"Custom filter {key} must be of type FilterBinaryFile")

    def filter(self, key, value):
        if key in self.__filters:
            self.position = self.__filters[key].check(value)
        else:
            self.position = FILTER_POSITION.KEEP
        if not self.position == FILTER_POSITION.KEEP:
            raise FilterStopSkipException()
