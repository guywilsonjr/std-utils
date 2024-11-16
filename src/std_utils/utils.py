import subprocess
import time

def subprocess_seq(size):
    com = ['seq', str(size)]
    a = subprocess.run(com, capture_output=True, text=True)
    data = {
        'stdout': a.stdout,
        'stderr': a.stderr,
        'returncode': a.returncode
    }
    return data
print(data)
