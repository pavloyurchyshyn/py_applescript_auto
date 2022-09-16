from typing import Iterable, Union
from ascr_abstractions import AbsBaseAScript


class ArgsKeys(AbsBaseAScript):
    """
    Keys which will be replaced by values.
    """
    Script = '@script'
    Scr = Script
    Object = '@object'
    Obj = Object
    Window = '@window'
    Win = Window
    Application = '@application'
    App = Application
    Value = '@value'
    Values = '@values'
    VariableName = '@variable_name'
    Options = '@options'
    File = '@file'
    Whom = '@whom'
    Property = '@property'
    Condition = '@condition'
    If = '@if_condition'
    Elif = '@elif_condition'
    Else = '@else_condition'


class CommonTemplates:
    """
    Simple common applescript commands.
    """
    Keys = ArgsKeys

    @classmethod
    def get_if_command(cls, condition, script=None) -> str:
        condition = cls.Keys.Condition if condition is None else condition
        script = cls.Keys.Script if script is None else script
        return f'if {condition} then\n{script}\nend if\n'

    if_ = get_if_command

    @classmethod
    def get_elif_command(cls, condition=None, script=None) -> str:
        condition = cls.Keys.Condition if condition is None else condition
        script = cls.Keys.Script if script is None else script
        return f'else if {condition} then\n{script}'

    elif_ = get_elif_command

    @classmethod
    def get_else_command(cls, script=None) -> str:
        return f'else\n{cls.Keys.Script if script is None else script}'

    else_ = get_else_command

    @classmethod
    def get_copy_to_command(cls, prop: str, dest=None) -> str:
        """
        Copy template. copy prop to
        :param prop: property name etc.
        :param dest: destination -> key, variable name or some another logic
        :return: string for example: copy position to variable_name
        """
        return f'copy {prop} to {cls.Keys.VariableName if dest is None else dest}'

    copy_to = get_copy_to_command

    @staticmethod
    def key_up(key: str) -> str:
        return f'key up {key}'

    @staticmethod
    def key_down(key: str) -> str:
        return f'key down {key}'

    @staticmethod
    def get_multiple_keys(keys) -> str:
        if type(keys) is not str:
            keys = ', '.join(keys)

        return '{k}'.replace('k', keys)

    @staticmethod
    def get_properties_of_command(obj) -> str:
        return f'properties of {obj}'

    properties_of = get_properties_of_command

    @staticmethod
    def get_screencapture_command(file, options="") -> str:
        return f'screencapture {options} {file}'

    screencapture = get_screencapture_command

    @staticmethod
    def get_return_command(value) -> str:
        return f'return {value}'

    @staticmethod
    def get_exists_command(obj) -> str:
        return f'exists {obj}'

    exists = get_exists_command

    @classmethod
    def get_do_shell_script_command(cls, script=None) -> str:
        return f'do shell script "{cls.Keys.Script if script is None else script}"'

    do_shell_script = get_do_shell_script_command

    @staticmethod
    def get_keystroke_command(value) -> str:
        return f'keystroke {value}'

    keystroke = get_keystroke_command

    @classmethod
    def get_create_property_command(cls, name, value=None) -> str:
        return f'property {name} : {cls.Keys.Value if value is None else value}'

    property = get_create_property_command

    @classmethod
    def get_set_variable_command(cls, name, value=None) -> str:
        return f'set {name} to {cls.Keys.Value if value is None else value}'

    set_var = get_set_variable_command

    @classmethod
    def get_repeat_command(cls, times: str, script: str = None) -> str:
        return f'repeat {times} times\n{cls.Keys.Script if script is None else script}\nend repeat'

    repeat = get_repeat_command

    @classmethod
    def get_tell_app_command(cls, app, script=None) -> str:
        app = f'"{app}"' if type(app) is str else app
        return CommonTemplates.get_tell_command(f'application {app}\n', script=script)

    tell_app = get_tell_app_command

    @classmethod
    def get_tell_window_command(cls, window: str, script: str = None) -> str:
        window = window if type(window) is int else f'"{window}"'
        return CommonTemplates.get_tell_command(f'window {window}\n', script=script)

    tell_window = get_tell_window_command

    @classmethod
    def get_tell_command(cls, whom: str, script=None) -> str:
        return f'tell {whom}{cls.Keys.Script if script is None else script}\nend tell'

    tell = get_tell_command

    @staticmethod
    def get_delay_command(delay: str or int or float) -> str:
        return f'delay {delay}'

    delay = get_delay_command

    @staticmethod
    def get_click_command(obj):
        return f'click {obj}'

    click = get_click_command

    @staticmethod
    def get_click_at_command(position: Union[Iterable, str]) -> str:
        if type(position) is str:
            if not position.startswith('{'):
                position = '{' + position
            if not position.endswith('{'):
                position = position + '}'

            return 'click at pos'.replace('pos', position)
        else:
            return 'click at {pos}'.replace('pos', ', '.join(map(str, position[:2])))

    click_at = get_click_at_command


CTemps = CommonTemplates
