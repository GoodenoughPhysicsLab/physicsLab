import format_coding_style as fcs
import unittest

import sys
sys.path.append("test")

from test_physicsLab import BasicTest
from test_pl_web import WebTest

if __name__ == "__main__":
    fcs.main()
    unittest.main()