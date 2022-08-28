from common_scripts import ArgsKeys, CommonScripts
from constants import AppleScrConst


class BaseAScript:
    def __init__(self, body: str = ArgsKeys.Script):
        self.body = str(body)

    def add_script(self, script, **kwargs):
        return self.add(script, key=ArgsKeys.Script, **kwargs)

    def add_value(self, script, **kwargs):
        return self.add(script, key=ArgsKeys.Value, **kwargs)

    def add(self, script, key: str = ArgsKeys.Script, pos: int = 0,
            next_key: str = None, next_key_delim='\n',
            delay: int = 0):
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

    def insert_scripts(self, *scripts, key: str = ArgsKeys.Script, pos: int = 0, **kwargs):
        """
        Place few scripts in some position.
        :param scripts: the iterable object which contains str or AScript objects
        """
        self.add('\n'.join(map(str, scripts)), key=key, pos=pos, **kwargs)
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

    def add_delay(self, delay=5, next_key=None):
        """
        Add delay in applescript, equal to sleep in python.
        :param delay: seconds
        :type delay: int
        """
        self.add('', delay=delay, next_key=next_key)
        return self

    @staticmethod
    def replace_to_position(body, script, key=ArgsKeys.Script, position=0) -> str:
        body: list = body.split(key)
        body[position] = f'{body[position]}{script}{body.pop(position + 1)}'
        return key.join(body)

    def join_scripts(self, *scripts):
        """
        Add scripts in the end.
        """
        self.body = '\n'.join((self.body, *map(str, scripts)))


class AScript(BaseAScript):

    # todo, get screen of element

    def get_obj_size(self, obj, **kwargs):
        return self.property_of(AppleScrConst.ObjProp.Size, obj=obj, **kwargs)

    def get_obj_pos(self, obj, **kwargs):
        return self.property_of(AppleScrConst.ObjProp.Position, obj=obj, **kwargs)

    def property_of(self, prop: str, obj: str, **kwargs):
        return self.add(f'{prop} of {obj}', **kwargs)

    def do_screen_of_area(self, file: str, rect: tuple, **kwargs):
        """
        :param file: where to save the screen capture, 1 file per screen.
        :param rect: -R x,y,w,h Capture a screen rectangle, top,left,width,height.
        """
        return self.do_screen(file, options=f'-R {",".join(map(str, rect[:4]))}', **kwargs)

    def get_properties_of(self, object_, **kwargs):
        return self.add(CommonScripts.properties_of(object_), **kwargs)

    def do_screen(self, file: str, options: str, **kwargs):
        """
        https://ss64.com/osx/screencapture.html
        """
        return self.do_shell_script(CommonScripts.screencapture(file, options), **kwargs)

    def do_shell_script(self, script: str or tuple, **kwargs):
        script = script if type(script) is str else ' '.join(script)
        return self.add(CommonScripts.do_shell_script(script), **kwargs)

    def keystroke(self, value, **kwargs):
        return self.add(CommonScripts.keystroke(value), **kwargs)

    def set_variable(self, name: str, **kwargs):
        return self.add(CommonScripts.set_var(name), **kwargs)

    def tell_system_events(self, **kwargs):
        return self.add(CommonScripts.tell_app(AppleScrConst.SysEvents), **kwargs)

    def repeat_n_times(self, times: int, **kwargs):
        return self.add(CommonScripts.repeat(str(times)), **kwargs)

    def click(self, obj, key=ArgsKeys.Script, pos=0, next_key=None, delay=0):
        return self.add(CommonScripts.click(obj), key=key, pos=pos, next_key=next_key, delay=delay)

    def click_at(self, position, **kwargs):
        return self.add(CommonScripts.click_at(position), **kwargs)

    def exists(self, obj, **kwargs):
        return self.add(CommonScripts.exists(obj), **kwargs)

    def __str__(self):
        return self.body


if __name__ == '__main__':
    ascript = AScript()
    ascript.tell_system_events()
    ascript.click_at((100, 100), next_key=ArgsKeys.Script)
    ascript.repeat_n_times(10, next_key=ArgsKeys.Script)
    ascript.add_delay(5, next_key=ArgsKeys.Script)
    ascript.set_variable('test_var').add('1', key=ArgsKeys.Value)
    ascript.do_screen_of_area('test.png', (1, 2, 3, 4, 5, 6, 7, 8))
    print(ascript)
