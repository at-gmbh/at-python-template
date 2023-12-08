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
return_code = 1
try:
    p = subprocess.Popen(
        [sys.executable, '-m', 'cookiecutter', '--no-input', '-o', f'"{temp_dir}"', '.'],
        cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return_code = p.returncode
    actual_fail = return_code != 0
finally:
    shutil.rmtree(temp_dir, ignore_errors=True)

# handle possible issues & give proper return codes
if b'Python 3.8 or higher' in stdout or b'successfully created' in stdout:
    status = {True: "failed", False: "succeded"}
    if actual_fail == expect_fail:
        print(f"Python {platform.python_version()} {status[expect_fail]} as expected")
    else:
        print(
            f"{platform.python_version()} should have {status[expect_fail]},",
            f"but actually {status[actual_fail]}",
        )
        sys.exit(return_code)
elif b'SyntaxError' in stderr:
    print(f"got a syntax error in pre_gen_project.py:\n{stderr}")
    sys.exit(return_code)
else:
    print(f"unexpected error, code {return_code}")
    print(f"stderr: {stderr}")
    print(f"stdout: {stdout}")
    sys.exit(return_code)
