from base import AScript
from const import ObjProp
from common_commands import ArgsKeys


class ScreenshotOfWindow(AScript):
    def __init__(self, screen_path,
                 tell_to: AScript or str = None,
                 sys_events=True,
                 set_frontmost=True,
                 x_pos='x', y_pos='y',
                 h_size='x_size', v_size='y_size',
                 key_after_screenshot=None,
                 delay_after_frontmost=1,
                 ):

        self.screen_path = screen_path
        super().__init__()
        if sys_events:
            self.tell_system_events()

        if tell_to is not None:
            self.tell(tell_to)

        if set_frontmost:
            self.set_frontmost()
            self.add_delay(delay_after_frontmost)
        self.copy_to(ObjProp.Position, ''.join(('{', x_pos, ', ', y_pos, '}')))
        self.copy_to(ObjProp.Size, ''.join(('{', h_size, ', ', v_size, '}')))
        self.do_screen(options=f'-R " & {x_pos} & "," & {y_pos} & "," & {h_size} & "," & {v_size} &"',
                       file=screen_path, next_key=key_after_screenshot)


class WindowElements(AScript):
    def __init__(self,
                 window: str,
                 tell_to: str = None,
                 sys_events=True,
                 set_frontmost=True,
                 as_type='list'
                 ):

        super().__init__()
        if sys_events:
            self.tell_system_events()

        if tell_to is not None:
            self.tell(tell_to)

        if set_frontmost:
            self.set_frontmost()
        window = window if type(window) is int else f'"{window}"'
        self.get_entire_content(f'window {window} as {as_type}', next_key=None)


if __name__ == '__main__':
    s = ScreenshotOfWindow('~Desktop/test.png', tell_to='application "TEST"\n')
    print(s, '\n')
    s = WindowElements('TEST_WINDOW', tell_to='application "TEST"\n')
    print(s)
