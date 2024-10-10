import sys
from chimerax.core.toolshed import BundleAPI
from chimerax.core.commands import register

class _MyAPI(BundleAPI):
    api_version = 1

    @staticmethod
    def register_command(bi, ci, logger):
        from . import states
        register(ci.name, states.states_desc, states.states)

bundle_api = _MyAPI()
