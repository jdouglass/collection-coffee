import logging
from config.constants import LOG_FILENAME

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,  # The lowest level by default is WARNING if not specified
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()
