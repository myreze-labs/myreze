from typing import Dict, Any, Optional, Union
import json
import numpy as np
from myreze.viz.visualization import Visualization
from myreze.data.validate import validate_mdp
from typing import Union, List
from datetime import datetime
import isodate  # For ISO 8601 parsing


class Geometry:
    """Represents a geometry in GeoJSON format."""

    def __init__(self, type: str, value: Union[dict, List[dict]]):
        self.type = type
        self.value = value

    @classmethod
    def from_dict(cls, data: dict) -> "Geometry":
        """Create a Geometry instance from a dictionary."""
        return cls(type=data["type"], value=data["value"])


class Time:
    """Represents a timestamp, time span, or series of timestamps in ISO 8601 format."""

    def __init__(self, type: str, value: Union[str, dict, List[str]]):
        self.type = type
        self.value = value
        self._validate()

    def _validate(self) -> None:
        """Validate the time definition."""
        if self.type not in ["Timestamp", "Span", "Series"]:
            raise ValueError(f"Invalid time type: {self.type}")

        if self.type == "Timestamp":
            if not isinstance(self.value, str):
                raise ValueError("Timestamp value must be a string")
            isodate.parse_datetime(self.value)  # Raises ValueError if invalid

        elif self.type == "Span":
            if (
                not isinstance(self.value, dict)
                or "start" not in self.value
                or "end" not in self.value
            ):
                raise ValueError("Span value must be a dict with 'start' and 'end'")
            start = isodate.parse_datetime(self.value["start"])
            end = isodate.parse_datetime(self.value["end"])
            if start >= end:
                raise ValueError("Span start must be before end")

        elif self.type == "Series":
            if not isinstance(self.value, list):
                raise ValueError("Series value must be a list")
            times = [isodate.parse_datetime(t) for t in self.value]
            if not times:
                raise ValueError("Series cannot be empty")
            if times != sorted(times):
                raise ValueError("Series timestamps must be sorted")

    def to_dict(self) -> dict:
        """Convert to a JSON-serializable dictionary."""
        return {"type": self.type, "value": self.value}

    @classmethod
    def from_dict(cls, data: dict) -> "Time":
        """Create from a dictionary."""
        return cls(type=data["type"], value=data["value"])

    @classmethod
    def timestamp(cls, timestamp: str) -> "Time":
        """Create a Timestamp instance."""
        return cls(type="Timestamp", value=timestamp)

    @classmethod
    def span(cls, start: str, end: str) -> "Time":
        """Create a Span instance."""
        return cls(type="Span", value={"start": start, "end": end})

    @classmethod
    def series(cls, timestamps: List[str]) -> "Time":
        """Create a Series instance."""
        return cls(type="Series", value=timestamps)


class MyrezeDataPackage:
    """A class representing a Myreze Data Package for geolocated data and visualization."""

    def __init__(
        self,
        id: str,
        geometry: Geometry,
        data: Dict[str, Any],
        time: Time,
        unreal_visualization: Optional[Visualization] = None,
        threejs_visualization: Optional[Visualization] = None,
        metadata: Optional[Dict[str, Any]] = None,
        version: str = "1.0.0",
    ):
        self.id = id
        self.geometry = geometry  # data needed to build the visual representation
        self.data = data  # May include NumPy arrays
        self.time = time
        self.unreal_visualization = unreal_visualization
        self.threejs_visualization = threejs_visualization
        self.metadata = metadata or {}
        self.version = version
        self._validate()  # Validate on initialization

    def _validate(self) -> None:
        """Validate the data package against the MDP schema."""
        validate_mdp(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """Convert the data package to a JSON-serializable dictionary."""
        data = self.data.copy()
        for key, value in data.items():
            if isinstance(value, np.ndarray):
                data[key] = value.tolist()  # Convert NumPy arrays to lists
        return {
            "version": self.version,
            "type": "MyrezeDataPackage",
            "id": self.id,
            "geometry": self.geometry.to_dict(),
            "data": data,
            "visualization": (
                self.visualization.to_dict() if self.visualization else None
            ),
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert the data package to a JSON string."""
        return json.dumps(self.to_dict())

    def visualize(self) -> Visualization:
        """Get the visualization."""
        return self.visualization(self)

    def to_threejs(self):
        return None

    def to_unreal(self):
        return None

    @classmethod
    def from_json(cls, json_str: str) -> "MyrezeDataPackage":
        """Create a data package from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MyrezeDataPackage":
        """Create a data package from a dictionary."""
        geometry = Geometry.from_dict(data["geometry"])
        visualization = (
            Visualization.from_dict(data["visualization"])
            if data.get("visualization")
            else None
        )
        return cls(
            id=data["id"],
            geometry=geometry,
            data=data["data"],  # Lists remain lists; convert to arrays later if needed
            visualization=visualization,
            metadata=data.get("metadata", {}),
            version=data["version"],
        )
