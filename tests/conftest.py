import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
# adventures are private; the tests use a fictional fixture
os.environ["ADVENTURES_DIR"] = os.path.join(ROOT, "tests", "fixtures", "adventures")
