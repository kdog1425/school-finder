import logging
import time

logger = logging.getLogger('qualm')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/qualm.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.converter = time.gmtime
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
