from base import AScript
from const import ObjProp
from common_commands import ArgsKeys


class ScreenshotOfWindow(AScript):
    def __init__(self, screen_path,
                 tell_wraps: AScript or str = ArgsKeys.Script,
                 set_frontmost=True,
                 x_pos='x', y_pos='y',
                 h_size='x_size', v_size='y_size',
                 key_after_screenshot=None,
                 delay_after_frontmost=1,
                 ):
        self.screen_path = screen_path

        super().__init__(tell_wraps)
        if set_frontmost:
            self.set_frontmost()
            self.add_delay(delay_after_frontmost)
        self.copy_to(ObjProp.Position, ''.join(('{', x_pos, ', ', y_pos, '}')))
        self.copy_to(ObjProp.Size, ''.join(('{', h_size, ', ', v_size, '}')))
        self.do_screen(options=f'-R " & {x_pos} & "," & {y_pos} & "," & {h_size} & "," & {v_size} &"',
                       file=screen_path, next_key=key_after_screenshot)


if __name__ == '__main__':
    s = ScreenshotOfWindow('test.png', tell_wraps='tell application "System Events"\n@script\nend tell')
    print(s)