# ############## #
# custom project #
# ############## #
from .base import INSTALLED_APPS

INSTALLED_APPS.append('widget_tweaks')

INSTALLED_APPS.append('blog')
INSTALLED_APPS.append('accounts')
AUTH_USER_MODEL = 'accounts.User'


