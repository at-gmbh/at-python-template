import os
import platform
import shutil
import sys
import tempfile

from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

expect_fail = '--fail' in sys.argv
actual_fail = False

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
try:
    cookiecutter(root, no_input=True, output_dir=temp_dir)
except FailedHookException as e:
    actual_fail = True
finally:
    shutil.rmtree(temp_dir, ignore_errors=True)

if actual_fail == expect_fail:
    print("Python {} {} as expected".format(
        platform.python_version(),
        "failed" if expect_fail else "succeeded"))
else:
    print("Python {} should have {}, but actually {}".format(
        platform.python_version(),
        "failed" if expect_fail else "succeeded",
        "failed" if actual_fail else "succeeded"))
    sys.exit(1)
