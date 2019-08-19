# Note: This file allows the other tests to import the packages to be tested, as explained at
# https://docs.python-guide.org/writing/structure/#test-suite.
# (currently unneeded, as all tests use the subprocess call ... hope this gets fixed though)

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
