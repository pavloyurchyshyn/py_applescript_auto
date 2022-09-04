from common_commands import ArgsKeys, CTemps
from const import AppleScrConst, ObjProp


class BaseAScript:
    def __init__(self, body: str = ArgsKeys.Script):
        self.body = str(body)

    def add_script(self, script, **kwargs):
        return self.add(script, key=ArgsKeys.Script, **kwargs)

    def add_value(self, script, **kwargs):
        return self.add(script, key=ArgsKeys.Value, **kwargs)

    def add(self, script, key: str = ArgsKeys.Script, pos: int = 0,
            next_key: str = ArgsKeys.Script, next_key_delim='\n',
            delay=0):
        """
        Main method of script creation.
        :param script: str or AScript object
        :param key: a key which will be replaced by script
        :param pos: which key replace in case of a few same keys in the body
        :param next_key: add key after script
        :param next_key_delim: symbol between script and new key
        :param delay: delay after script. Note: no output returns after a delay.
        :return: AScript object
        """
        script = str(script)
        if delay:
            script = f'{script}delay {delay}'
        if next_key:
            script = f'{script}{next_key_delim}{next_key}'
        self.body = self.replace_to_position(self.body, script, key, pos)

        return self

    def insert_scripts(self, *scripts,
                       key: str = ArgsKeys.Script,
                       pos: int = 0,
                       delimiter: str = '\n', **kwargs):
        """
        Place few scripts in some position.
        :param scripts: the iterable object which contains str or AScript objects
        """
        self.add(delimiter.join(map(str, scripts)), key=key, pos=pos, **kwargs)
        return self

    def add_kwargs(self, kwargs: dict):
        """
        Replacing keys by values.
        :type kwargs: dict
        :return:
        """
        for k, v in kwargs.items():
            self.body.replace(k, v, 1)

        return self

    def add_delay(self, delay=5, **kwargs):
        """
        Add delay in applescript, equal to sleep in python.
        :param delay: seconds
        :type delay: int
        """
        self.add('', delay=delay, **kwargs)
        return self

    @staticmethod
    def replace_to_position(body, script, key=ArgsKeys.Script, position=0) -> str:
        if key in body:
            if position < 0:
                position = len(body.split(key)) - 1 + position
                position = 0 if position < 0 else position

            if position > len(body.split(key)) - 1:
                if body.endswith(key):
                    body = body[:len(body) - len(key)]
                return body + script

            else:
                body: list = body.split(key)
                body[position] = f'{body[position]}{script}{body.pop(position + 1)}'
                return key.join(body)
        else:
            raise KeyError(f'Not key in script:\n {body}')

    def join_scripts(self, *scripts):
        """
        Add scripts in the end.
        """
        self.body = '\n'.join((self.body, *map(str, scripts)))
        return self

    def __str__(self):
        parts = self.body.split('\n')
        t_ind = 0
        for i, string in enumerate(parts.copy()):
            if string.startswith('tell'):
                parts[i] = '\t' * t_ind + parts[i]
                t_ind += 1

            elif string == 'end tell':
                t_ind -= 1
                parts[i] = '\t' * t_ind + parts[i]

            else:
                parts[i] = '\t' * t_ind + parts[i]

        return '\n'.join(parts)


class AScript(BaseAScript):
    def is_selected(self, obj, **kwargs):
        return self.property_of(ObjProp.Selected, obj=obj, **kwargs)

    def is_focused(self, obj, **kwargs):
        return self.property_of(ObjProp.Focused, obj=obj, **kwargs)

    # todo, get screen of element
    def set_frontmost(self, v=True, **kwargs):
        return self.set_variable(ObjProp.Frontmost, value=str(v).lower(), **kwargs)

    def get_obj_size(self, obj, **kwargs):
        return self.property_of(ObjProp.Size, obj=obj, **kwargs)

    def get_obj_pos(self, obj, **kwargs):
        return self.property_of(ObjProp.Position, obj=obj, **kwargs)

    def property_of(self, prop: str, obj: str, **kwargs):
        return self.add(f'{prop} of {obj}', **kwargs)

    def do_screen_of_area(self, file: str, rect: tuple, **kwargs):
        """
        :param file: where to save the screen capture, 1 file per screen.
        :param rect: -R x,y,w,h Capture a screen rectangle, top,left,width,height.
        """
        return self.do_screen(file, options=f'-R {",".join(map(str, rect[:4]))}', **kwargs)

    def get_properties_of(self, object_, **kwargs):
        return self.add(CTemps.properties_of(object_), **kwargs)

    def do_screen(self, file: str, options: str, **kwargs):
        """
        https://ss64.com/osx/screencapture.html
        """
        return self.do_shell_script(CTemps.screencapture(file, options), **kwargs)

    def do_shell_script(self, script: str or tuple, **kwargs):
        script = ' '.join(script) if type(script) is tuple else str(script)
        return self.add(CTemps.do_shell_script(script), **kwargs)

    def keystroke(self, value, **kwargs):
        return self.add(CTemps.keystroke(value), **kwargs)

    def set_variable(self, name: str, value=None, **kwargs):
        return self.add(CTemps.set_var(name, value=value), **kwargs)

    def tell_system_events(self, **kwargs):
        return self.add(CTemps.tell_app(AppleScrConst.SysEvents), **kwargs)

    def repeat_n_times(self, times: int, **kwargs):
        return self.add(CTemps.repeat(str(times)), **kwargs)

    def click(self, obj, key=ArgsKeys.Script, pos=0, next_key=None, delay=0):
        return self.add(CTemps.click(obj), key=key, pos=pos, next_key=next_key, delay=delay)

    def click_at(self, position, **kwargs):
        return self.add(CTemps.click_at(position), **kwargs)

    def exists(self, obj, **kwargs):
        return self.add(CTemps.exists(obj), **kwargs)

    def copy_to(self, obj, to=ArgsKeys.Value, **kwargs):
        return self.add(CTemps.copy_to(obj, to), **kwargs)


if __name__ == '__main__':
    ascript = AScript()
    ascript.tell_system_events()
    ascript.click_at((100, 100), next_key=ArgsKeys.Script)
    ascript.repeat_n_times(10, next_key=ArgsKeys.Script)
    ascript.add_delay(5, next_key=ArgsKeys.Script)
    ascript.set_variable('test_var').add('1', key=ArgsKeys.Value)
    ascript.do_screen_of_area('test.png', (1, 2, 3, 4, 5, 6, 7, 8))
    print(ascript)
