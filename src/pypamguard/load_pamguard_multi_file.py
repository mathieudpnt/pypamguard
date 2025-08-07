import os, glob
from pypamguard.core.filters import Filters, WhitelistFilter
from .load_pamguard_binary_file import load_pamguard_binary_file
from .logger import logger, Verbosity
from pypamguard.core.readers import Report
from pypamguard.core.exceptions import CriticalException

last_root = None
last_mask = None
master_list = []
master_dict = {}
MAX_NAME_LEN = 80

def find_binary_file(root, mask, file):
    global last_mask, last_root, master_list, master_dict
    if (not last_root or not last_mask) or (last_root != root or last_mask != mask):
        master_list = glob.glob(pathname=mask, root_dir=root, recursive=True)
        master_dict = {}
        for reldir in master_list:
            path = os.path.join(root, reldir)
            fname = os.path.basename(path)
            short_name = fname[len(fname)-MAX_NAME_LEN:] if len(fname) > MAX_NAME_LEN else fname
            if short_name not in master_dict: 
                master_dict[short_name] = path
        last_root = root
        last_mask = mask
    if file in master_dict:
        return master_dict[file]
    else:
        return None

def load_pamguard_multi_file(data_dir, file_names, item_uids):
    """
    A function to load a number of PAMGuard data chunks at once from
    various binary files, filtering by UID.

    For example
    `file_names=["file1.pgdf", "file1.pgdf", "file2.pgdf", "file3.pgdf", "file3.pgdf"]`
    `item_uids=[7000001, 7000199, 10000001, 10002893, 6000001]`
    Will expect to find 3 files: "file1.pgdf", "file2.pgdf", and "file3.pgdf". In
    "file1.pgdf" will expect to find uids 7000001, 7000199. In "file2.pgdf" will expect
    to find uid 10000001. In "file3.pgdf" will expect to find uids 10002893, 6000001.
    
    If `len(file_names) != len(item_uids)`, will raise an error.
    If a particular file name is not found in the data directory, will raise a warning.
    If a particular uid is not found in an expected file, will raise a warning.
    """


    file_name_dict = {}
    report = Report()

    if len(file_names) != len(item_uids):
        report.add_error(CriticalException("file_names and item_uids must be the same length."))

    event_data = []
    logger.set_verbosity(verbosity=Verbosity.ERROR)
        
    # Each file name has one or more UIDs. Better represented by dict.
    for file_name, uid in zip(file_names, item_uids):
        if file_name not in file_name_dict:
            file_name_dict[file_name] = []
        file_name_dict[file_name].append(uid)

    for file_name in file_name_dict:
        logger.info(f"Loading {file_name}")
        filter_obj = Filters({"uidlist": WhitelistFilter(file_name_dict[file_name])})
        file_path = find_binary_file(data_dir, "**/*.pgdf", file_name)
        file_data = load_pamguard_binary_file(file_path, filters=filter_obj, report = report)
        if not file_data:
            report.add_warning(f"File {file_name} not found in {data_dir}. Skipping.")
            continue
        event_data.extend(file_data.data)

    return event_data, report