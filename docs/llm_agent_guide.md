# Myreze LLM Agent Guide

This guide provides comprehensive information for LLM-based agents working with the Myreze toolkit. It covers discovery methods, usage patterns, and best practices for creating and interpreting geospatial data packages.

## Quick Start for LLM Agents

### 1. Module Discovery
```python
# Import core components
from myreze.data import MyrezeDataPackage, Time, VISUALIZATION_TYPES, VISUALIZATION_SCHEMAS
from myreze.data.validate import validate_visualization_data, suggest_visualization_type

# Discover available visualization types
print("Available types:", VISUALIZATION_TYPES)

# Get schema for specific type
from myreze.data.core import VISUALIZATION_SCHEMAS
heatmap_schema = VISUALIZATION_SCHEMAS["heatmap"]
print("Required fields:", heatmap_schema["required_fields"])
```

### 2. Create Data Package
```python
import numpy as np

# Example: Temperature heatmap
data = {
    "grid": np.random.rand(50, 50) * 30 + 10,  # Temperature data
    "bounds": [-74.0, 40.7, -73.9, 40.8],     # Geographic bounds
    "units": "celsius"
}

package = MyrezeDataPackage(
    id="temperature-map",
    data=data,
    time=Time.timestamp("2023-01-01T12:00:00Z"),
    visualization_type="heatmap",
    metadata={
        "description": "Temperature heatmap",
        "colormap": "viridis"
    }
)
```

### 3. Validate and Export
```python
# Validate data structure
errors = validate_visualization_data(data, "heatmap")
if errors:
    print("Validation errors:", errors)

# Export for transfer
json_output = package.to_json()
```

## Visualization Types and Data Patterns

### Grid-Based Data (flat_overlay, heatmap)
```python
data = {
    "grid": [[value, value, ...], ...],        # 2D array of values
    "bounds": [west, south, east, north],      # Geographic bounds in degrees
    "resolution": 0.01,                        # Optional: degrees per pixel
    "units": "measurement_unit"                # Optional: data units
}
```

**Use cases:** Weather maps, satellite imagery, temperature fields, pressure maps

### Point-Based Data (point_cloud)
```python
data = {
    "locations": [                             # Array of geographic points
        {"lat": 40.7, "lon": -74.0, "elevation": 10},
        {"lat": 40.8, "lon": -74.1, "elevation": 15}
    ],
    "values": [25.3, 24.1],                   # Measurements at each location
    "point_ids": ["sensor_001", "sensor_002"] # Optional: unique identifiers
}
```

**Use cases:** Weather stations, sensor networks, GPS points, survey data

### Vector Data (vector_field)
```python
data = {
    "grid_points": {"lats": [...], "lons": [...]},  # Grid coordinates
    "u_component": [[...], [...]],                  # East-west components
    "v_component": [[...], [...]],                  # North-south components
    "magnitude": [[...], [...]]                     # Optional: vector magnitudes
}
```

**Use cases:** Wind patterns, ocean currents, magnetic fields, flow data

### Trajectory Data (trajectory)
```python
data = {
    "positions": [                             # Time-ordered positions
        {"lat": 25.0, "lon": -80.0, "timestamp": "2023-01-01T00:00:00Z"},
        {"lat": 26.0, "lon": -81.0, "timestamp": "2023-01-01T06:00:00Z"}
    ],
    "track_id": "TRACK_001"                   # Optional: trajectory identifier
}
```

**Use cases:** Storm tracks, vehicle routes, animal migration, movement analysis

## Schema Validation Patterns

### Check Data Structure
```python
from myreze.data.validate import validate_visualization_data

# Validate against specific type
errors = validate_visualization_data(data, "heatmap")
if errors:
    print("Fix these issues:", errors)
```

### Auto-Suggest Visualization Type
```python
from myreze.data.validate import suggest_visualization_type

# Get suggestions based on data structure
suggestions = suggest_visualization_type(data)
print("Recommended types:", suggestions)
```

### Discovery Methods
```python
# Get available schemas
from myreze.data.validate import get_schemas
schemas = get_schemas()

# Get requirements for specific type
from myreze.data.validate import get_visualization_requirements
reqs = get_visualization_requirements("point_cloud")
print("Required fields:", reqs["required_fields"])
```

## Time Handling Patterns

### Single Timestamp
```python
time_obj = Time.timestamp("2023-01-01T12:00:00Z")
```

### Time Range
```python
time_obj = Time.span("2023-01-01T00:00:00Z", "2023-01-02T00:00:00Z")
```

### Time Series
```python
timestamps = [
    "2023-01-01T00:00:00Z",
    "2023-01-01T01:00:00Z", 
    "2023-01-01T02:00:00Z"
]
time_obj = Time.series(timestamps)
```

## Common Error Patterns and Solutions

### Data Validation Errors
- **Missing required fields**: Check schema requirements with `get_visualization_requirements()`
- **Wrong data types**: Ensure arrays are 2D for grids, objects for locations
- **Dimension mismatches**: Grid dimensions must match for u/v components

### Time Format Issues
- **Invalid ISO format**: Use `YYYY-MM-DDTHH:MM:SSZ` format
- **Unsorted series**: Time series must be chronologically ordered
- **Invalid spans**: Start time must be before end time

### Visualization Type Selection
- **Grid + bounds**: Use `flat_overlay` or `heatmap`
- **Locations + values**: Use `point_cloud`
- **Grid + vectors**: Use `vector_field`
- **Time sequence**: Use `trajectory`

## Metadata Best Practices

Include rich metadata to improve visualization quality:

```python
metadata = {
    "description": "Clear description of the data",
    "units": "Physical units (celsius, meters, etc.)",
    "colormap": "viridis|plasma|coolwarm|...",
    "opacity": 0.8,                        # For overlays
    "min_value": 0,                        # Data range
    "max_value": 100,
    "data_source": "Source identifier",
    "created_at": "2023-01-01T12:00:00Z"
}
```

## Working with Received Packages

### Load and Inspect
```python
# Load from JSON
package = MyrezeDataPackage.from_json(json_string)

# Inspect properties
print("ID:", package.id)
print("Visualization type:", package.visualization_type)
print("Time type:", package.time.type)
print("Data fields:", list(package.data.keys()))
print("Metadata:", package.metadata)
```

### Process by Type
```python
def process_package(package: MyrezeDataPackage):
    viz_type = package.visualization_type
    
    if viz_type == "heatmap":
        grid = package.data["grid"]
        bounds = package.data["bounds"]
        # Process as 2D surface data
        
    elif viz_type == "point_cloud":
        locations = package.data["locations"]
        values = package.data["values"]
        # Process as discrete points
        
    elif viz_type == "vector_field":
        u_comp = package.data["u_component"]
        v_comp = package.data["v_component"]
        # Process as directional data
        
    else:
        # Handle unknown types gracefully
        print(f"Unknown type: {viz_type}")
```

## Discovery Functions Reference

### Core Discovery
```python
# Available visualization types
from myreze.data.core import VISUALIZATION_TYPES
print(VISUALIZATION_TYPES)

# Schema definitions
from myreze.data.core import VISUALIZATION_SCHEMAS
print(VISUALIZATION_SCHEMAS["heatmap"])

# Package methods
types = MyrezeDataPackage.get_available_visualization_types()
schema = MyrezeDataPackage.get_visualization_schema("heatmap")
info = package.get_schema_info()  # For specific package
```

### Validation Functions
```python
from myreze.data.validate import (
    validate_visualization_data,    # Validate data structure
    suggest_visualization_type,     # Auto-suggest type
    get_visualization_requirements, # Get type requirements
    get_schemas                     # Get all schemas
)
```

## Example Workflows

### Creating Weather Data Package
```python
import numpy as np

# Generate temperature grid
temp_grid = np.random.rand(100, 100) * 30 + 10

# Create package
package = MyrezeDataPackage(
    id="weather-temp",
    data={
        "grid": temp_grid,
        "bounds": [-74.1, 40.6, -73.9, 40.9],
        "units": "celsius"
    },
    time=Time.timestamp("2023-07-15T14:30:00Z"),
    visualization_type="heatmap",
    metadata={
        "description": "Temperature heatmap",
        "colormap": "viridis",
        "parameter": "air_temperature"
    }
)

# Validate and export
errors = validate_visualization_data(package.data, "heatmap")
if not errors:
    json_output = package.to_json()
```

### Processing Sensor Data
```python
# Structure sensor readings
sensor_data = {
    "locations": [
        {"lat": 40.7128, "lon": -74.0060, "elevation": 10},
        {"lat": 40.6892, "lon": -74.0445, "elevation": 5}
    ],
    "values": [22.5, 21.8],
    "point_ids": ["NYC001", "NYC002"]
}

# Auto-suggest type
suggestions = suggest_visualization_type(sensor_data)
print("Suggested types:", suggestions)  # Should suggest "point_cloud"

# Create package
package = MyrezeDataPackage(
    id="sensor-readings",
    data=sensor_data,
    time=Time.timestamp("2023-07-15T14:30:00Z"),
    visualization_type="point_cloud",
    metadata={"parameter": "temperature", "units": "celsius"}
)
```

## Error Recovery Patterns

### Validation Failure Recovery
```python
# Try to determine correct type
suggestions = suggest_visualization_type(data)
if suggestions:
    for suggested_type in suggestions:
        errors = validate_visualization_data(data, suggested_type)
        if not errors:
            print(f"Use visualization_type='{suggested_type}'")
            break
```

### Data Structure Fixes
```python
# Fix common issues
if "grid" in data and "bounds" not in data:
    # Add bounds for grid data
    data["bounds"] = [-180, -90, 180, 90]  # Global bounds

if "locations" in data and isinstance(data["locations"][0], list):
    # Convert [lat, lon] lists to objects
    data["locations"] = [
        {"lat": point[0], "lon": point[1]} 
        for point in data["locations"]
    ]
```

This guide provides comprehensive patterns for LLM agents to effectively work with the Myreze toolkit. Use the discovery functions to understand capabilities, follow the data patterns for different visualization types, and use validation to ensure data quality. 