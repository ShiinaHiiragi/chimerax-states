import sys
from chimerax.core.toolshed import BundleAPI
from chimerax.core.commands import register

class _MyAPI(BundleAPI):
    api_version = 1

    @staticmethod
    def register_command(bi, ci, logger):
        from . import cmds
        cmd_name = ci.name
        cmd_desc = getattr(cmds, f"{cmd_name}_desc")
        cmd_func = getattr(cmds, cmd_name)
        register(cmd_name, cmd_desc, cmd_func)

bundle_api = _MyAPI()
