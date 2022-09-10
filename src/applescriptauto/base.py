from typing import Union, Iterable
from common_commands import ArgsKeys, CTemps
from const import AppleScrConst, ObjProp, TELL, END_TELL, END_IF
from ascr_abstractions import AbsBaseAScript as AbsScr


class BaseAScript(AbsScr):
    Keys = ArgsKeys

    def __init__(self, body: Union[AbsScr, str, None] = ArgsKeys.Script):
        """
        Base class to build applescript code.
        Uses the simple principle of replacing keys with values.
        :param body: first script value.
        """
        body = self.Keys.Script if body is None else body
        self.body = str(body)

    def add_script(self, script: Union[AbsScr, str], **kwargs):
        """
        Replaces script key by passed script.
        """
        return self.add(script, key=ArgsKeys.Script, **kwargs)

    def add_value(self, script: Union[AbsScr, str], **kwargs):
        return self.add(script, key=ArgsKeys.Value, **kwargs)

    def add(self, script,
            key: Union[AbsScr, str, None] = None,
            pos: int = 0,
            next_key: Union[AbsScr, str, None] = 0,
            next_key_delim='\n',
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

        next_key = ArgsKeys.Script if next_key == 0 else next_key
        if next_key:
            script = f'{script}{next_key_delim}{next_key}'

        key = self.Keys.Script if key is None else key
        self.body = self.replace_to_position(self.body, script, key=key, position=pos)

        return self

    def insert_scripts(self, *scripts,
                       key: str = None,
                       pos: int = 0,
                       delimiter: str = '\n', **kwargs):
        """
        Place few scripts in some position.
        :param scripts: the iterable object which contains str or AScript objects
        """
        key = self.Keys.Script if key is None else key
        self.add(delimiter.join(map(str, scripts)), key=key, pos=pos, **kwargs)
        return self

    def add_kwargs(self, kwargs: dict[str, AbsScr]):
        """
        Replacing keys by values.
        :type kwargs: dict
        :return:
        """
        for k, v in kwargs.items():
            self.body.replace(k, str(v), 1)

        return self

    def add_delay(self, delay: Union[str, int] = 5, **kwargs):
        """
        Add delay in applescript, equal to sleep in python.
        :param delay: seconds
        :type delay: int
        """
        self.add('', delay=delay, **kwargs)
        return self

    @staticmethod
    def replace_to_position(body: Union[AbsScr, str],
                            script: Union[AbsScr, str],
                            key: str, position: int = 0) -> str:
        body: str = str(body)
        script: str = str(script)

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
            raise KeyError(f'Not key "{key}" in script:\n {body}')

    def join_scripts(self, *scripts):
        """
        Add scripts in the end.
        """
        self.body = '\n'.join((self.body, *map(str, scripts)))
        return self

    def __str__(self) -> str:
        return self.body

    @property
    def pretty_str(self) -> str:
        parts = list(filter(bool, self.body.split('\n')))
        t_ind = 0
        if_cond_in_line = lambda l: any((l.startswith(k) for k in ('else if', 'if', 'else')))

        for i, string in enumerate(parts.copy()):
            if string.startswith(TELL):
                parts[i] = '\t' * t_ind + parts[i]
                if END_TELL not in parts[i]:
                    t_ind += 1

            elif if_cond_in_line(string):
                t_ind_ = t_ind
                if string.startswith('else') or string.startswith('else if'):
                    t_ind_ -= 1
                else:
                    t_ind += 1

                parts[i] = '\t' * t_ind_ + parts[i]

            elif string == END_TELL or string == END_IF:
                t_ind -= 1
                parts[i] = '\t' * t_ind + parts[i]

            else:
                parts[i] = '\t' * t_ind + parts[i]

        return '\n'.join(parts)


class AScript(BaseAScript):
    def is_selected(self, obj: Union[BaseAScript, str], **kwargs):
        return self.property_of(ObjProp.Selected, obj=obj, **kwargs)

    def is_focused(self, obj: Union[BaseAScript, str], **kwargs):
        return self.property_of(ObjProp.Focused, obj=obj, **kwargs)

    def set_frontmost(self, v: Union[bool, str] = True, **kwargs):
        return self.set_variable(ObjProp.Frontmost, value=str(v).lower(), **kwargs)

    def get_obj_size(self, obj: Union[BaseAScript, str], **kwargs):
        return self.property_of(ObjProp.Size, obj=obj, **kwargs)

    def if_(self, condition: str, script: Union[BaseAScript, str] = None, elif_=False, else_=False, **kwargs):
        script = self.__if_helper(script, elif_=elif_, else_=else_)
        return self.add(CTemps.if_(condition, script), **kwargs)

    def elif_(self, condition: Union[BaseAScript, str],
              script: Union[BaseAScript, str, None] = None,
              elif_: bool = False, else_: bool = False,
              next_key: Union[str, None] = None,
              key: Union[str, None] = None,
              **kwargs):
        key = self.Keys.Elif if key is None else key
        script = self.__if_helper(script, elif_=elif_, else_=else_)
        return self.add(CTemps.elif_(condition, script=script), key=key, next_key=next_key, **kwargs)

    def else_(self, script: Union[BaseAScript, str] = None, key: str = None, next_key: str = None, **kwargs):
        key = self.Keys.Else if key is None else key
        return self.add(CTemps.else_(script=script), key=key, next_key=next_key, **kwargs)

    @staticmethod
    def __if_helper(script, elif_=False, else_=False):
        if elif_ or else_:
            script = f'{ArgsKeys.Script}' if script is None else script
        if elif_:
            script = f'{script}\n{ArgsKeys.Elif}'
        if else_:
            script = f'{script}\n{ArgsKeys.Else}'
        return script

    def get_obj_pos(self, obj: Union[BaseAScript, str], **kwargs):
        return self.property_of(ObjProp.Position, obj=obj, **kwargs)

    def get_entire_content(self, obj: Union[BaseAScript, str], **kwargs):
        return self.property_of(ObjProp.EntireContents, obj=obj, **kwargs)

    def property_of(self, prop: str, obj: Union[BaseAScript, str], **kwargs):
        return self.add(f'{prop} of {obj}', **kwargs)

    def do_screen_of_area(self, file: str, rect: tuple, **kwargs):
        """
        :param file: where to save the screen capture, 1 file per screen.
        :param rect: -R x,y,w,h Capture a screen rectangle, top,left,width,height.
        """
        return self.do_screen(file, options=f'-R {",".join(map(str, rect[:4]))}', **kwargs)

    def get_properties_of(self, obj: Union[BaseAScript, str], **kwargs):
        return self.add(CTemps.properties_of(obj), **kwargs)

    def do_screen(self, file: str, options: str, **kwargs):
        """
        https://ss64.com/osx/screencapture.html
        """
        return self.do_shell_script(CTemps.screencapture(file, options), **kwargs)

    def do_shell_script(self, script: Union[BaseAScript, str, Iterable], **kwargs):
        script = str(script) if isinstance(script, (BaseAScript, str)) else ' '.join(script)
        return self.add(CTemps.do_shell_script(script), **kwargs)

    def keystroke(self, value: Union[BaseAScript, str], **kwargs):
        return self.add(CTemps.keystroke(value), **kwargs)

    def set_variable(self, name: Union[BaseAScript, str], value=None, **kwargs):
        value = self.Keys.Value if value is None else value
        return self.add(CTemps.set_var(name, value=value), **kwargs)

    def tell(self, to: Union[BaseAScript, str],
             script: Union[BaseAScript, str] = None,
             next_key: str = None, **kwargs):
        script = self.Keys.Script if script is None else script
        return self.add(CTemps.tell(whom=to, script=script), next_key=next_key, **kwargs)

    def tell_system_events(self, next_key: str = None, **kwargs):
        return self.add(CTemps.tell_app(AppleScrConst.SysEvents), next_key=next_key, **kwargs)

    def tell_window(self, window: Union[BaseAScript, str], script: Union[BaseAScript, str, None] = None, **kwargs):
        return self.add(CTemps.tell_window(window, script), **kwargs)

    def repeat_n_times(self, times: int, **kwargs):
        return self.add(CTemps.repeat(str(times)), **kwargs)

    def click(self, obj: Union[BaseAScript, str],
              key: str = None, pos: int = 0,
              next_key: str = None,
              delay: int = 0):
        key = self.Keys.Script if key is None else key
        return self.add(CTemps.click(obj), key=key, pos=pos, next_key=next_key, delay=delay)

    def click_at(self, position: Union[str, Iterable], **kwargs):
        return self.add(CTemps.click_at(position), **kwargs)

    def exists(self, obj: Union[BaseAScript, str], **kwargs):
        return self.add(CTemps.exists(obj), **kwargs)

    def copy_to(self, obj: Union[BaseAScript, str], to: Union[BaseAScript, str] = None, **kwargs):
        to = self.Keys.Value if to is None else to
        return self.add(CTemps.copy_to(obj, to), **kwargs)


if __name__ == '__main__':
    # Note: better to use '' for string, because the string in a-script declares inside ""
    # Simple example:
    simple_example = AScript()  # 1)
    #   @script

    simple_example.add('tell application "System Events"\n@script\nend tell', next_key=None)  # 2)
    #   tell application "System Events"
    #         @script
    #   end tell

    simple_example.add('tell application process "TEST_APP"\n@xy_cond\nend tell', next_key=None)  # 3)
    #   tell application "System Events"
    #         tell application process "TEST_APP"
    #             @xy_cond
    #        end tell
    #   end tell

    simple_example.add('copy position of window "APP_WIN_NAME" to {x, y}', key='@xy_cond')  # 4)
    #   tell application "System Events"
    #      tell application process "TEST_APP"
    #          copy position of window "APP_WIN_NAME" to {x, y}
    #          @script
    #      end tell
    #   end tell

    simple_example.add('click at {x, y}', next_key=None)  # 5)
    #   tell application "System Events"
    #       tell application process "TEST_APP"
    #           copy position of window "APP_WIN_NAME" to {x, y}
    #           click at {x, y}
    #       end tell
    #   end tell
    print(f"Example:\n{simple_example}")

    # Also, this methods created in AScript
