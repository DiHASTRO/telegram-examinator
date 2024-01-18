# Just an example
# Most likely you will need to change only API_TOKEN

from pathlib import Path
import sys

API_TOKEN = '1234567890:AaBbCcDdEeSm222DwDqwDzxzZS2-AB7C2d'
DATABASE_FILE = 'database.db'

PROJECT_ROOT = Path(__file__).parent.parent

DATABASE_PATH = PROJECT_ROOT / DATABASE_FILE
STATICS_PATH = PROJECT_ROOT / 'static'
IMAGES_PATH = STATICS_PATH / 'images'

