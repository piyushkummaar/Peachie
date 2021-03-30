#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/SmsService/project")
from project import application
application.secret_key = 'mysecretkey123'