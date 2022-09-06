from typing import List
import omni.usd
import omni.kit.commands
from pxr import Sdf


def get_selection() -> List[str]:
    """Get the list of currently selected prims"""
    return omni.usd.get_context().get_selection().get_selected_prim_paths()
