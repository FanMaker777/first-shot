import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Insert pyxel stub
from tests import pyxel_stub
sys.modules['pyxel'] = pyxel_stub
