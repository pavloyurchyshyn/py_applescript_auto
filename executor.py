import os
import re
from subprocess import Popen, PIPE
from constants import AppleScrConst

ENCOD = 'utf-8'
DELIMITER = ', '
KVDELIMITER = ':'


class ScriptResult:
    def __init__(self, return_code, output: bytes, error: bytes, script=None):
        self.return_code = return_code
        self.output = output.decode(ENCOD)
        self.error = error.decode(ENCOD)
        self.script = script

    def json(self) -> dict:
        if not str(self.output):
            raise Exception(f'No output to parse: {self.output}')

        return self.convert_to_json(self.output)

    @staticmethod
    def convert_to_json(resp: str) -> dict:
        """
        Simple parser.
        """
        if resp.startswith('{'):
            resp = resp[1:-1]
        if resp.endswith('}'):
            resp = resp[:-1]
        parsed_json = {}

        for b in re.findall(r'[^ =,\s]{2}[\w\s\d]+:{[\d, ]*}', resp):
            k, v = b.split(KVDELIMITER)

            if k in (AppleScrConst.ObjProp.Size, AppleScrConst.ObjProp.Position):
                v = tuple(map(int, v[1:-1].split(DELIMITER)))

            parsed_json[k] = v
            resp = resp.replace(b + DELIMITER, '')

        for key_value in resp.split(DELIMITER):
            key, value = key_value.split(KVDELIMITER)
            if value == AppleScrConst.MissValue:
                value = None
            elif value == AppleScrConst.AppleScrTrue:
                value = True
            elif value == AppleScrConst.AppleScrFalse:
                value = False

            parsed_json[key] = value

        return parsed_json


def execute(script: str):
    script = open(script).read() if os.path.exists(script) else script
    exe = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = exe.communicate(input=str(script).encode(ENCOD))

    return ScriptResult(exe.returncode, out, err, script)


if __name__ == '__main__':
    pass
