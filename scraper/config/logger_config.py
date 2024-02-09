import logging
from config.constants import LOG_FILENAME
import re
from datetime import datetime, timedelta

logger = logging.getLogger()
if not logger.handlers:
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.DEBUG,  # The lowest level by default is WARNING if not specified
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')



def clear_old_log_entries(log_file_path, days_old=3):
    """
    Clears log entries older than a specified number of days.

    Parameters:
    - log_file_path: Path to the log file to be cleaned.
    - days_old: Number of days to use as the cutoff for old entries. Defaults to 3.
    """
    cutoff_date = datetime.now() - timedelta(days=days_old)
    current_entries = []
    last_date = None  # Variable to hold the date of the last timestamped entry

    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                log_date = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                last_date = log_date  # Update last known date
            if last_date and last_date > cutoff_date:
                current_entries.append(line)
            elif not match:
                continue

    with open(log_file_path, 'w') as file:
        file.writelines(current_entries)
