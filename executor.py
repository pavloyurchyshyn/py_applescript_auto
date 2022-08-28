import os
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
        print(resp)
        j = resp[1:-1].split(DELIMITER)
        json = {}
        for key_value in j:
            print(key_value)
            key, value = key_value.split(KVDELIMITER)

            if value == AppleScrConst.MissValue:
                value = None
            elif value == AppleScrConst.AppleScrTrue:
                value = True
            elif value == AppleScrConst.AppleScrFalse:
                value = False
            elif key in ('size', 'position'):
                print(key, value)
                value = value[1:-1].split(DELIMITER)

            json[key] = value

        return json


def execute(script: str):
    script = open(script).read() if os.path.exists(script) else script
    exe = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = exe.communicate(input=str(script).encode(ENCOD))

    return ScriptResult(exe.returncode, out, err, script)


if __name__ == '__main__':
    resp = execute("""tell application "System Events"
	exists window "applescript – script.py" of application process "pycharm" of application "System Events"
	tell process "pycharm"
		properties of window "applescript – executor.py" of application process "pycharm" of application "System Events"
	end tell
end tell
""")
    print(resp.output)
    print(resp.error)
    print(resp.return_code)
    print()
    print(resp.json())
