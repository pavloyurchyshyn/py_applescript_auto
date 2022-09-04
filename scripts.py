from base import AScript
from const import ObjProp


class ScreenshotOfWindow(AScript):
    def __init__(self, screen_path,
                 tell_to: AScript or str = None,
                 sys_events=True,
                 set_frontmost=True,
                 x_pos='x', y_pos='y',
                 width='w_size', height='h_size',
                 key_after_screenshot=None,
                 delay_after_frontmost=1,
                 ):
        """
        Template for window screenshot.
        :param screen_path: where the file should be stored
        :param tell_to: tell application/process/etc. NAME\n@script\nend tell
        :param sys_events: add tell application "System Events"
        :param set_frontmost: place program window over other
        :param x_pos: variable name for x coordinate
        :param y_pos: variable name for y coordinate
        :param width: variable name for program width
        :param height: variable name for program height
        :param key_after_screenshot: key for the next script
        :param delay_after_frontmost: for slow systems
        """
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
        self.copy_to(ObjProp.Size, ''.join(('{', width, ', ', height, '}')))
        self.do_screen(options=f'-R " & {x_pos} & "," & {y_pos} & "," & {width} & "," & {height} &"',
                       file=screen_path, next_key=key_after_screenshot)


class GetAllElements(AScript):
    def __init__(self,
                 window: str,
                 tell_to: str = None,
                 container_type='window',
                 sys_events=True,
                 set_frontmost=True,
                 as_type='list'
                 ):
        """
        Template to get UI objects in window, etc.
        :param window: window, application, etc.
        :param tell_to: tell application/process/etc. NAME\n@script\nend tell
        :param container_type:
        :param sys_events: add tell application "System Events"
        :param set_frontmost: place program window over other
        :param as_type: type which returns, recommended list
        """
        super().__init__()
        if sys_events:
            self.tell_system_events()

        if tell_to is not None:
            self.tell(tell_to)

        if set_frontmost:
            self.set_frontmost()
        window = window if type(window) is int else f'"{window}"'
        self.get_entire_content(f'{container_type} {window} as {as_type}', next_key=None)


if __name__ == '__main__':
    s = ScreenshotOfWindow('~Desktop/test.png', tell_to='application "TEST"\n')
    print(s, '\n')
    s = GetAllElements('TEST_WINDOW', tell_to='application "TEST"\n')
    print(s)
