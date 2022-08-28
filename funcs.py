import time
from constants import AppleScrConst as const
from executor import execute, ScriptResult
from script import BaseAScript


def wait_for_condition(script: str or BaseAScript, condition, timeout=5, exception=TimeoutError,
                       delay=0) -> ScriptResult:
    """
    Wait for some result.
    :param script: script object or text
    :param condition: a function that analyzes the result object and returns True/False
    :param timeout: time in seconds
    :param exception: which exception will be raised on timeout
    :param delay: delay between script executions
    :return: result object
    """
    timeout_ = time.time() + timeout
    while timeout_ > time.time():
        exe_result: ScriptResult = execute(script)
        if condition(exe_result):
            return exe_result
        time.sleep(delay)

    else:
        raise exception


def wait_for_true(script: str or BaseAScript, timeout=5, exception=TimeoutError, delay=0) -> ScriptResult:
    return wait_for_condition(script,
                              lambda r: r.output == const.AppleScrTrue,
                              timeout=timeout, exception=exception, delay=delay)


def wait_for_false(script: str or BaseAScript, timeout=5, exception=TimeoutError, delay=0) -> ScriptResult:
    return wait_for_condition(script,
                              lambda r: r.output == const.AppleScrFalse,
                              timeout=timeout, exception=exception, delay=delay)
