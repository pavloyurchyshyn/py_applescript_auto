import os
from subprocess import Popen, PIPE

ENCOD = 'utf-8'


class ScriptResult:
    def __init__(self, return_code, output: bytes, error: bytes, script=None):
        self.return_code = return_code
        self.output = output.decode(ENCOD)
        self.error = error.decode(ENCOD)
        self.script = script


def execute(script: str):
    script = open(script).read() if os.path.exists(script) else script
    exe = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = exe.communicate(input=str(script).encode(ENCOD))

    return ScriptResult(exe.returncode, out, err, script)
