import logging
import os
from datetime import date, datetime, timedelta

cwd = os.getcwd()
datenow = datetime.now().strftime('%Y%m%d')

logging.basicConfig(filename= cwd + '/logs/api_face_' + datenow +'.log',
                    # format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    # datefmt='%d/%m/%Y %I:%M:%S',
                    level=logging.DEBUG
                    )

# create logger
logger = logging.getLogger('API_FARE')
logger.setLevel(logging.DEBUG)

# # sử dụng
# logger.debug('This message should go to the log file')
# logger.info('So should this')
# logger.warning('And this, too')
# logger.error()
# logger.critical()
# # ghép chuỗi
# logger.warning('%s before you %s', 'Look', 'leap!')



