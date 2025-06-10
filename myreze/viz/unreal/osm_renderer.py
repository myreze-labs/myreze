from myreze.viz.unreal.unreal import UnrealRenderer
from typing import Dict, Any

import numpy as np

@UnrealRenderer.register
class OSMRenderer(UnrealRenderer):
    """Render a OSMRenderer object."""

    def render(self, data: "MyrezeDataPackage", params: Dict[str, Any]) -> str:
        """Render the data package as a Unreal Engine object."""

        rgba = data.get("grid")
        rgba_uint8 = (rgba * 255).astype(np.uint8)

        return rgba_uint8
