import os
import platform
import shutil
import subprocess
import sys
import tempfile

expect_fail = '--fail' in sys.argv
actual_fail = False

# run cookiecutter in a subprocess (so we can catch terminal output)
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
try:
    p = subprocess.Popen(
        [sys.executable, '-m', 'cookiecutter', '--no-input', '-o', temp_dir, '.'],
        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    actual_fail = p.returncode != 0
finally:
    shutil.rmtree(temp_dir, ignore_errors=True)

# handle possible issues & give proper return codes
if b'Python 3.6 or higher' in stdout or b'successfully created' in stdout:
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
elif b'SyntaxError' in stderr:
    print("got a syntax error in pre_gen_project.py:\n" + str(stderr))
    sys.exit(1)
else:
    print("unexpected error: " + str(stderr))
    sys.exit(1)
