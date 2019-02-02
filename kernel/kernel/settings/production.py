from .base import *
from .secure import *

DEBUG = False
ALLOWED_HOST = config('ALLOWED_HOST', cast=lambda v:[s.strip() for s in v.split(',')])