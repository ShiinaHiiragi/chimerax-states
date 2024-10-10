import re

from typing import Any
from chimerax.core.commands import CmdDesc
from chimerax.core.commands import StringArg

# actual record of max depth: 21
MAX_DEPTH = 24
DUPLICATED = "«DUPLICATED»"
EXCEEDED = "«EXCEEDED»"

ids = set()
to_key = lambda key: key \
    if isinstance(key, str) \
    else re.sub(r" at 0x[0-9A-F]{16}", "", str(to_key))

def cruise(obj: Any, depth=0):
    global ids
    if depth == 0:
        ids.clear()
    obj_id = id(obj)
    if obj_id in ids:
        return DUPLICATED
    else:
        ids.add(obj_id)

    if depth >= MAX_DEPTH:
        return EXCEEDED

    if type(obj) in (int, float, bool, str, type(None)):
        return obj
    elif type(obj) in (dict,):
        return {
            to_key(key): cruise(obj[key], depth + 1)
            for key in obj
        }
    elif type(obj) in (tuple, list, set):
        return [cruise(item, depth + 1) for item in obj]
    elif hasattr(obj, "__dict__"):
        return {
            to_key(key): cruise(obj.__dict__[key], depth + 1)
            for key in obj.__dict__
            if key not in ("__objclass__",)
        }
    else:
        return str(obj)

def flatten(obj: dict, prefix=""):
    result = {}
    if type(obj) in (int, float, bool, str, type(None)):
        result[prefix[:-1]] = obj
    elif isinstance(obj, dict):
        for key in obj:
            result.update(flatten(obj[key], prefix + key + "."))
    elif hasattr(obj, "__iter__"):
        for index, item in enumerate(obj):
            result.update(flatten(item, prefix + "#" + str(index) + "."))
    return {
        key: result[key]
        for key in result
        if result[key] != DUPLICATED
    }

def states(session, filename="output"):
    with open(
        f"C:/Users/Ichinoe/Repository/dos/snippet/{filename}.json",
        mode="w",
        encoding="utf-8"
    ) as writable:
        import json
        json.dump(
            flatten(cruise(session)),
            writable,
            indent=2,
            ensure_ascii=False
        )

states_desc = CmdDesc(
    required=[("filename", StringArg)],
    synopsis="..."
)
