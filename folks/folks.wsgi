import sys
import os
root = os.path.dirname(__name__)
sys.path.insert(0, root)
from folks import app
application = app
