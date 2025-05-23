# Myreze

Myreze is a data passing, processing and visualization toolkit for handling geospatial data and rendering it through different visualization engines. It provides a unified interface for managing, validating, and visualizing geospatial data with time components.

## Installation

```bash
pip install -e .
```

## Core Concepts

Myreze is built around these core concepts:

- **Data Packages**: Container for geospatial data with time information
- **Time**: Flexible time representation (timestamps, spans, series)
- **Renderers**: Visualization schemas for different platforms

## Usage

### Creating a Data Package

```python
from myreze.data import MyrezeDataPackage, Time

# Create a timestamp for your data
time_data = Time.timestamp("2023-01-01T00:00:00Z")

# Create a data package with your geospatial data
data_package = MyrezeDataPackage(
    id="my-geodata",
    data={"points": [[lat1, lon1], [lat2, lon2]]},
    time=time_data,
    metadata={"creator": "Your Name", "description": "Sample dataset"}
)

# Export to JSON
json_data = data_package.to_json()
```

### Visualizing with Three.js

```python
from myreze.data import MyrezeDataPackage
from myreze.viz import ThreeJSRenderer

# Create a data package
data_package = MyrezeDataPackage(
    id="visualization-example",
    data=your_data,
    time=your_time,
    threejs_visualization=ThreeJSRenderer()
)

# Generate visualization
visualization = data_package.to_threejs(params={})
```

### Visualizing with Unreal Engine

```python
from myreze.data import MyrezeDataPackage
from myreze.viz import UnrealRenderer

# Create a data package
data_package = MyrezeDataPackage(
    id="unreal-example",
    data=your_data,
    time=your_time,
    unreal_visualization=UnrealRenderer()
)

# Generate visualization
visualization = data_package.to_unreal(params={})
```

## Time Handling

Myreze provides flexible time handling:

```python
from myreze.data import Time

# Single timestamp
timestamp = Time.timestamp("2023-01-01T00:00:00Z")

# Time span
timespan = Time.span("2023-01-01T00:00:00Z", "2023-01-02T00:00:00Z")

# Time series
timeseries = Time.series([
    "2023-01-01T00:00:00Z",
    "2023-01-01T01:00:00Z",
    "2023-01-01T02:00:00Z"
])
```

## Package Components

- **data**: Core data structures and validation
- **viz**: Visualization renderers for various platforms
  - **threejs**: Web-based 3D visualizations
  - **unreal**: Unreal Engine visualizations
  - **png**: Static image export

## Development

### Update PyPI 

```shell
python -m build
python -m twine upload dist/*
```

## Dependencies

- numpy: For numerical operations
- isodate: For ISO 8601 parsing

## Data conventions

For convenience, let's stick to some simple rules:

- Use Web Mercator WGS84 auxiliary sphere (EPSG 3857) when passing geolocations (like bounding boxes). See 
-  Return geolocated data normalized to the (0,1) planar region.
-  Let the second component (y) in the returned geometries point up.
-  Place any layers at y=0 offset.

## Documentation

See the [API documentation](docs/api.md) and [tutorial](docs/tutorial.md) for more information.
