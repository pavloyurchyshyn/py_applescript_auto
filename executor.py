import os
import re
from subprocess import Popen, PIPE
from const import AppleScrConst as ASC, ObjProp

ENCOD = 'utf-8'
DELIMITER = ', '
KVDELIMITER = ':'


class ScriptResult:
    def __init__(self, return_code, output: bytes, error: bytes, script=None):
        self.return_code = return_code
        self.output = output.decode(ENCOD)
        self.error = error.decode(ENCOD)
        self.script = script

    def boolean(self):
        if self.output == ASC.AppleScrTrue:
            return True
        elif self.output == ASC.AppleScrFalse:
            return False
        else:
            raise TypeError(f'The output is not {ASC.AppleScrTrue} or {ASC.AppleScrFalse}')

    def json(self) -> dict:
        if not str(self.output):
            raise Exception(f'No output to parse: {self.output}')

        return self.convert_to_json(self.output)

    @staticmethod
    def convert_to_json(resp: str) -> dict:
        """
        Simple parser.
        """
        if resp == '{}':
            return {}

        if resp.startswith('{'):
            resp = resp[1:]
        if resp.endswith('}'):
            resp = resp[:-1]
        parsed_json = {}

        for k_v in re.findall(r'[^ =,\s]{2}[\w\s\d]+:{[\d, ]*}', resp):
            k, v = k_v.split(KVDELIMITER)

            if k in (ObjProp.Size, ObjProp.Position):
                if v == '{}':
                    v = {}
                elif re.search(r'\{[\d, ]+\}', v):
                    v = tuple(map(int, v[1:-1].split(DELIMITER)))

            parsed_json[k] = v
            resp = resp.replace(k_v + DELIMITER, '')

        for key_value in resp.split(DELIMITER):
            key, value = key_value.split(KVDELIMITER)
            if value == ASC.MissValue:
                value = None
            elif value == ASC.AppleScrTrue:
                value = True
            elif value == ASC.AppleScrFalse:
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
