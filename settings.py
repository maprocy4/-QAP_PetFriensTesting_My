#!/usr/bin/python

import os
from dotenv import load_dotenv

load_dotenv()
valid_email = os.getenv("valid_email")
valid_passwd = os.getenv("valid_passwd")
