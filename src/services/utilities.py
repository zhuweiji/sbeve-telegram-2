import logging
from pathlib import Path
logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

import os

TOKEN = os.environ['SBEVE_BOT_TOKEN']
WEBHOOK_URL = os.environ['WEBHOOK_URL']


PROJECT_DIR = Path(__file__).parent.parent
SECRETS_DIR = PROJECT_DIR / 'secrets'
