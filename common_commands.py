class ArgsKeys:
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


class CommonTemplates:
    """
    Simple common applescript commands.
    """
    Tell = f'tell {ArgsKeys.Whom}{ArgsKeys.Scr}\nend tell'
    TellApplication = Tell.replace(ArgsKeys.Whom, f'application "{ArgsKeys.App}"\n')
    TellApp = TellApplication
    TellWindow = Tell.replace(ArgsKeys.Whom, f'window {ArgsKeys.Win}\n')
    Delay = f'delay {ArgsKeys.Value}'
    Click = f'click {ArgsKeys.Value}'
    ClickAt = f'click at {ArgsKeys.Value}'
    RepeatNTimes = f'repeat {ArgsKeys.Value} times\n{ArgsKeys.Script}\nend repeat'
    SetVariable = f'set {ArgsKeys.VariableName} to {ArgsKeys.Value}'
    CopyTo = f'copy {ArgsKeys.Property} to {ArgsKeys.VariableName}'
    CreateProperty = f'property {ArgsKeys.VariableName} : {ArgsKeys.Value}'
    PropertiesOf = f'properties of {ArgsKeys.Object}'
    KeyStroke = f'keystroke {ArgsKeys.Value}'
    DoShellScript = f'do shell script "{ArgsKeys.Script}"'
    Exists = f'exists {ArgsKeys.Object}'
    Return = f'return {ArgsKeys.Value}'
    Screencapture = f'screencapture {ArgsKeys.Options} {ArgsKeys.File}'
    MultipleKeys = '{k}'.replace('k', ArgsKeys.Values)
    KeyUp = f'key up {ArgsKeys.Value}'
    KeyDown = f'key down {ArgsKeys.Value}'

    @staticmethod
    def get_copy_to_command(prop: str, dest=ArgsKeys.VariableName) -> str:
        """
        Copy template. copy prop to
        :param prop: property name etc.
        :param dest: destination -> key, variable name or some another logic
        :return: string for example: copy position to variable_name
        """
        return CommonTemplates.CopyTo.replace(ArgsKeys.Property, prop).replace(ArgsKeys.VariableName, dest)

    copy_to = get_copy_to_command

    @staticmethod
    def key_up(key: str) -> str:
        return CommonTemplates.KeyUp.replace(ArgsKeys.Value, key)

    @staticmethod
    def key_down(key: str) -> str:
        return CommonTemplates.KeyDown.replace(ArgsKeys.Value, key)

    @staticmethod
    def get_multiple_keys(keys) -> str:
        return CommonTemplates.MultipleKeys.replace(ArgsKeys.Values, ', '.join(keys))

    @staticmethod
    def get_properties_of_command(obj) -> str:
        return CommonTemplates.PropertiesOf.replace(ArgsKeys.Object, obj)

    properties_of = get_properties_of_command

    @staticmethod
    def get_screencapture_command(file, options) -> str:
        return CommonTemplates.Screencapture.replace(ArgsKeys.Options, options).replace(ArgsKeys.File, file)

    screencapture = get_screencapture_command

    @staticmethod
    def get_return_command(value) -> str:
        return CommonTemplates.Return.replace(ArgsKeys.Value, value)

    @staticmethod
    def get_exists_command(obj) -> str:
        return CommonTemplates.Exists.replace(ArgsKeys.Object, obj)

    exists = get_exists_command

    @staticmethod
    def get_do_shell_script_command(script) -> str:
        return CommonTemplates.DoShellScript.replace(ArgsKeys.Script, script)

    do_shell_script = get_do_shell_script_command

    @staticmethod
    def get_keystroke_command(value) -> str:
        return CommonTemplates.KeyStroke.replace(ArgsKeys.Value, value)

    keystroke = get_keystroke_command

    @staticmethod
    def get_create_property_command(name, value=ArgsKeys.Value) -> str:
        return CommonTemplates.CreateProperty.replace(ArgsKeys.VariableName, name).replace(ArgsKeys.Value, value)

    property = get_create_property_command

    @staticmethod
    def get_set_variable_command(name, value=ArgsKeys.Value) -> str:
        return CommonTemplates.SetVariable.replace(ArgsKeys.VariableName, name).replace(ArgsKeys.Value, value)

    set_var = get_set_variable_command

    @staticmethod
    def get_repeat_command(times: str) -> str:
        return CommonTemplates.RepeatNTimes.replace(ArgsKeys.Value, times)

    repeat = get_repeat_command

    @staticmethod
    def get_tell_app_command(app: str) -> str:
        return CommonTemplates.TellApp.replace(ArgsKeys.App, app)

    tell_app = get_tell_app_command

    @staticmethod
    def get_tell_window_command(window: str, script: str = ArgsKeys.Script) -> str:
        window = window if type(window) is int else f'"{window}"'
        return CommonTemplates.TellWindow.replace(ArgsKeys.Win, window).replace(ArgsKeys.Script, script)

    tell_window = get_tell_window_command

    @staticmethod
    def get_tell_command(whom: str, script: str = ArgsKeys.Script) -> str:
        return CommonTemplates.Tell.replace(ArgsKeys.Whom, whom).replace(ArgsKeys.Script, script)

    tell = get_tell_command

    @staticmethod
    def get_delay_command(delay) -> str:
        return CommonTemplates.Delay.replace(ArgsKeys.Value, delay)

    delay = get_delay_command

    @staticmethod
    def get_click_command(obj):
        return CommonTemplates.Click.replace(ArgsKeys.Value, obj)

    click = get_click_command

    @staticmethod
    def get_click_at_command(position: tuple) -> str:
        pos = '{p}'.replace('p', ', '.join(map(str, position[:2])))
        return CommonTemplates.ClickAt.replace(ArgsKeys.Value, pos)

    click_at = get_click_at_command


CTemps = CommonTemplates
