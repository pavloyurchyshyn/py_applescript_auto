class ArgsKeys:
    Script = '@script'
    Scr = Script
    Window = '@window'
    Win = Window
    Application = '@application'
    App = Application
    Value = '@value'


class AppleScrConst:
    SysEvents = 'System Events'


class CommonScripts:
    TellApplication = f'tell application "{ArgsKeys.App}"\n{ArgsKeys.Scr}\nend tell\n'
    TellApp = TellApplication
    Delay = f'delay {ArgsKeys.Value}\n'
    Click = f'click {ArgsKeys.Value}\n'
    ClickAt = f'click at {ArgsKeys.Value}\n'

    @staticmethod
    def get_tell_app(app: str) -> str:
        return CommonScripts.TellApp.replace(ArgsKeys.App, app, 1)

    tell_app = get_tell_app

    @staticmethod
    def get_delay(delay) -> str:
        return CommonScripts.Delay.replace(ArgsKeys.Value, delay)

    delay = get_delay

    @staticmethod
    def get_click(obj):
        return CommonScripts.Click.replace(ArgsKeys.Value, obj)

    @staticmethod
    def get_click_at(position: tuple) -> str:
        pos = '{p}'.replace('p', ', '.join(map(str, position[:2])))
        return CommonScripts.ClickAt.replace(ArgsKeys.Value, pos)


class AScript:
    def __init__(self, body: str = ArgsKeys.Script):
        self.body = str(body)

    def add(self, script, key=ArgsKeys.Script, pos=0, n_arg=None, delay=0):
        if delay:
            script = f'{script}\ndelay {delay}'
        if n_arg:
            script = f'{script}\n{n_arg}'
        self.body = self.replace_to_position(self.body, script, key, pos)

        return self

    def add_kwargs(self, kwargs: dict):
        for k, v in kwargs.items():
            self.body.replace(k, v, 1)

        return self

    def add_delay(self, delay=5, n_arg=None):
        self.add('', delay=delay, n_arg=n_arg)
        return self

    @staticmethod
    def replace_to_position(body, script, key=ArgsKeys.Script, position=0):
        body: list = body.split(key)
        body[position] = f'{body[position]}{script}{body[position + 1]}'
        body.pop(position + 1)
        return key.join(body)

    def click(self, obj, key=ArgsKeys.Script, pos=0, n_arg=None, delay=0):
        self.add(CommonScripts.get_click(obj), key=key, pos=pos, n_arg=n_arg, delay=delay)
        return self

    def __str__(self):
        return self.body


if __name__ == '__main__':
    ascript = AScript()
    ascript.add_delay(n_arg=ArgsKeys.Script)
    ascript
    print(ascript)