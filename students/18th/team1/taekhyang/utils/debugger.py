import logging
import datetime
import os

from logging.handlers import RotatingFileHandler


debugger = logging.getLogger("Debugger")
# to make directory for log files
try:
    now = str(datetime.datetime.now().date()).replace('-', '')
    if not os.path.isdir('./logs'):
        os.mkdir('./logs')
    if not os.path.isdir('./logs/log-{}'.format(now)):
        os.mkdir('./logs/log-{}'.format(now))
    
    f_hdlr = RotatingFileHandler('./logs/log-{}/Debugger.log'.format(now),
                                encoding='UTF-8',
                                maxBytes=10 * 1024 * 1024,
                                backupCount=3)
except Exception as e:
    print(e)
    f_hdlr = RotatingFileHandler('Debugger.log',
                                encoding='UTF-8',
                                maxBytes=10 * 1024 * 1024,
                                backupCount=3)

s_hdlr = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_hdlr.setFormatter(formatter)
f_hdlr.setFormatter(formatter)

debugger.addHandler(f_hdlr)
debugger.addHandler(s_hdlr)
debugger.setLevel(logging.DEBUG)