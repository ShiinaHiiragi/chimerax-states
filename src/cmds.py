import os
import sys
import json

from typing import Any
from numpy import ndarray, set_printoptions
from chimerax.core.commands import CmdDesc
from chimerax.core.commands import StringArg

# actual record of max depth: 21
MAX_DEPTH = 24
DUPLICATED = "«DUPLICATED»"
EXCEEDED = "«EXCEEDED»"
BASIC_TYPE = (int, float, bool, str, type(None))

ids = set()
# to_key = lambda key: key \
#     if isinstance(key, str) \
#     else re.sub(r" at 0x[0-9A-F]{16}", "", str(key))

def cruise(obj: Any, depth=0):
    global ids
    if depth == 0:
        ids.clear()
    if not type(obj) in BASIC_TYPE:
        obj_id = id(obj)
        if obj_id in ids:
            return DUPLICATED
        else:
            ids.add(obj_id)

    if depth >= MAX_DEPTH:
        return EXCEEDED

    if type(obj) in BASIC_TYPE:
        return obj
    elif isinstance(obj, ndarray):
        return str(obj).replace("\n", "")
    elif isinstance(obj, dict):
        return {
            str(key): cruise(obj[key], depth + 1)
            for key in obj
            if key not in ("undo",)
        }
    elif type(obj) in (tuple, list, set):
        return [cruise(item, depth + 1) for item in obj]
    elif hasattr(obj, "__dict__"):
        return {
            str(key): cruise(obj.__dict__[key], depth + 1)
            for key in obj.__dict__
            if key not in ("__objclass__", "undo")
        }
    else:
        return str(obj)

def flatten(obj: dict, prefix=""):
    result = {}
    if type(obj) in BASIC_TYPE:
        result[prefix[:-1]] = obj
    elif isinstance(obj, dict):
        for key in obj:
            result.update(flatten(obj[key], prefix + key + "."))
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            result.update(flatten(item, prefix + "#" + str(index) + "."))
    return {
        key: result[key]
        for key in result
        if result[key] != DUPLICATED
    }

def output(file_path, obj):
    with open(
        os.path.expanduser(file_path),
        mode="w",
        encoding="utf-8"
    ) as writable:
        json.dump(obj, writable, indent=2, ensure_ascii=False)

def states(session, dir_path="~", filename="output"):
    set_printoptions(threshold=sys.maxsize)
    file_path_noext = os.path.join(dir_path, filename)

    cruised = cruise(session)
    output(f"{file_path_noext}.raw.json", cruised)

    flattened = flatten(cruised)
    output(f"{file_path_noext}.json", flattened)

states_desc = CmdDesc(
    required=[
        ("dir_path", StringArg),
        ("filename", StringArg)
    ],
    synopsis="List all states of session"
)

def destroy(session):
    from chimerax.cmd_line.tool import CommandLine
    from chimerax.core.commands import run
    tool_instances = session.ui.main_window.tool_instance_to_windows
    cli_object = [
        key for key in tool_instances
        if isinstance(key, CommandLine)
    ][0]
    cli_object.text.lineEdit().returnPressed.disconnect()
    run(session, "tool hide command")

destroy_desc = CmdDesc(
    synopsis="Disable command line interface"
)

def clear(session):
    from chimerax.core.filehistory import file_history
    file_history(session).clear_file_history()

clear_desc = CmdDesc(
    synopsis="Clear file history"
)
