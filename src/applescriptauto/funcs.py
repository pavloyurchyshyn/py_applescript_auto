import time
from const import AppleScrConst as const
from executor import execute, ScriptResult
from base import BaseAScript, AScript
from common_commands import ArgsKeys


def wait_for_condition(script: str or BaseAScript,
                       condition,
                       timeout=5, timeout_exception=TimeoutError,
                       delay=0) -> ScriptResult:
    """
    Wait for some result.
    :param script: script object or text
    :param condition: a function that analyzes the result object and returns True/False
    :param timeout: time in seconds
    :param timeout_exception: which exception will be raised on timeout
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
        raise timeout_exception


def wait_for_result(script: str or BaseAScript, result, timeout=5, timeout_exception=TimeoutError, delay=0) -> ScriptResult:
    return wait_for_condition(script,
                              lambda r: r.output == result,
                              timeout=timeout, timeout_exception=timeout_exception, delay=delay
                              )


def wait_for_true(script: str or BaseAScript, timeout=5, timeout_exception=TimeoutError, delay=0) -> ScriptResult:
    return wait_for_result(script, const.AppleScrTrue,
                           timeout=timeout, timeout_exception=timeout_exception, delay=delay)


def wait_for_false(script: str or BaseAScript, timeout=5, timeout_exception=TimeoutError, delay=0) -> ScriptResult:
    return wait_for_result(script, const.AppleScrFalse,
                           timeout=timeout, timeout_exception=timeout_exception, delay=delay)


def wait_for_obj_appear(obj, body=ArgsKeys.Script, timeout=5, timeout_exception=TimeoutError, delay=0):
    return wait_for_true(AScript(body).exists(obj), timeout=timeout, timeout_exception=timeout_exception, delay=delay)


def wait_for_obj_disappear(obj, body=ArgsKeys.Script, timeout=5, timeout_exception=TimeoutError, delay=0):
    return wait_for_false(AScript(body).exists(obj), timeout=timeout, timeout_exception=timeout_exception, delay=delay)


def object_exists(obj, body=ArgsKeys.Script, exception=None) -> bool:
    result: bool = execute(AScript(body).exists(obj)).output == const.AppleScrTrue
    if not result and exception:
        raise exception

    return result


def object_doesn_exists(obj, body=ArgsKeys.Script, exception=None) -> bool:
    result: bool = execute(AScript(body).exists(obj)).output == const.AppleScrFalse
    if not result and exception:
        raise exception

    return result
