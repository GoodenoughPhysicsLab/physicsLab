import os
import format_coding_style as fcs
import unittest

ROOT = os.path.dirname(__file__)

import sys
sys.path.append(os.path.join(ROOT, "test"))

from test_physicsLab import BasicTest
from test_pl_web import WebTest

if __name__ == "__main__":
    fcs.main()
    unittest.main()