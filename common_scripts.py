class ArgsKeys:
    Script = '@script'
    Scr = Script
    Object = '@object'
    Obj = Object
    Window = '@window'
    Win = Window
    Application = '@application'
    App = Application
    Value = '@value'
    VariableName = '@variable_name'
    Options = '@options'
    File = '@file'


class CommonScripts:
    TellApplication = f'tell application "{ArgsKeys.App}"\n{ArgsKeys.Scr}\nend tell\n'
    TellApp = TellApplication
    Delay = f'delay {ArgsKeys.Value}'
    Click = f'click {ArgsKeys.Value}'
    ClickAt = f'click at {ArgsKeys.Value}'
    RepeatNTimes = f'repeat {ArgsKeys.Value} times\n{ArgsKeys.Script}\nend repeat\n'
    SetVariable = f'set {ArgsKeys.VariableName} to {ArgsKeys.Value}'
    SetProperty = f'property {ArgsKeys.VariableName} : {ArgsKeys.Value}'
    PropertiesOf = f'properties of {ArgsKeys.Object}'
    KeyStroke = f'keystroke {ArgsKeys.Value}'
    DoShellScript = f'do shell script "{ArgsKeys.Script}"'
    Exists = f'exists {ArgsKeys.Object}'
    Return = f'return {ArgsKeys.Value}'
    Screencapture = f'screencapture {ArgsKeys.Options} {ArgsKeys.File}'

    @staticmethod
    def get_properties_of_command(obj) -> str:
        return CommonScripts.PropertiesOf.replace(ArgsKeys.Object, obj)
    properties_of = get_properties_of_command

    @staticmethod
    def get_screencapture_command(file, options) -> str:
        return CommonScripts.Screencapture.replace(ArgsKeys.Options, options).replace(ArgsKeys.File, file)
    screencapture = get_screencapture_command

    @staticmethod
    def get_return_command(value) -> str:
        return CommonScripts.Return.replace(ArgsKeys.Value, value)

    @staticmethod
    def get_exists_command(obj) -> str:
        return CommonScripts.Exists.replace(ArgsKeys.Object, obj)

    exists = get_exists_command

    @staticmethod
    def get_do_shell_script_command(script) -> str:
        return CommonScripts.DoShellScript.replace(ArgsKeys.Script, script)

    do_shell_script = get_do_shell_script_command

    @staticmethod
    def get_keystroke_command(value) -> str:
        return CommonScripts.KeyStroke.replace(ArgsKeys.Value, value)

    keystroke = get_keystroke_command

    @staticmethod
    def get_property_command(name) -> str:
        return CommonScripts.SetProperty.replace(ArgsKeys.VariableName, name)

    property = get_property_command

    @staticmethod
    def get_set_variable_command(name) -> str:
        return CommonScripts.SetVariable.replace(ArgsKeys.VariableName, name)

    set_var = get_set_variable_command

    @staticmethod
    def get_repeat_command(times: str) -> str:
        return CommonScripts.RepeatNTimes.replace(ArgsKeys.Value, times, 1)

    repeat = get_repeat_command

    @staticmethod
    def get_tell_app_command(app: str) -> str:
        return CommonScripts.TellApp.replace(ArgsKeys.App, app, 1)

    tell_app = get_tell_app_command

    @staticmethod
    def get_delay_command(delay) -> str:
        return CommonScripts.Delay.replace(ArgsKeys.Value, delay)

    delay = get_delay_command

    @staticmethod
    def get_click_command(obj):
        return CommonScripts.Click.replace(ArgsKeys.Value, obj)

    click = get_click_command

    @staticmethod
    def get_click_at_command(position: tuple) -> str:
        pos = '{p}'.replace('p', ', '.join(map(str, position[:2])))
        return CommonScripts.ClickAt.replace(ArgsKeys.Value, pos)

    click_at = get_click_at_command
