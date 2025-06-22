# Myreze Tutorial

This tutorial will guide you through creating data packages with different visualization types and rendering them with various engines.

## Basic Data Package Creation

```python
from myreze.data import MyrezeDataPackage, Time
import numpy as np

# Create time information
time_data = Time.timestamp("2023-01-01T12:00:00Z")

# Create a basic data package
data_package = MyrezeDataPackage(
    id="tutorial-example",
    data={"temperature": [20.5, 21.0, 19.8]},
    time=time_data,
    visualization_type="point_cloud",
    metadata={"source": "weather_station", "units": "celsius"}
)

print(f"Created package with visualization type: {data_package.visualization_type}")
```

## Understanding Visualization Types

The `visualization_type` field is crucial for telling receivers how to interpret your data. Here are common patterns:

### 1. Flat Overlays (2D Map Layers)

Use `"flat_overlay"` for data that should be displayed as a 2D layer on a map.

```python
from myreze.data import MyrezeDataPackage, Time
from myreze.viz import ThreeJSRenderer
import numpy as np

# Weather radar data
radar_data = {
    "grid": np.random.rand(200, 200),  # Precipitation intensity
    "bounds": [-74.5, 40.5, -73.5, 41.0],  # NYC area bounds
    "resolution": 0.005  # degrees per pixel
}

weather_overlay = MyrezeDataPackage(
    id="weather-radar",
    data=radar_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    threejs_visualization=ThreeJSRenderer(),
    visualization_type="flat_overlay",
    metadata={
        "layer_name": "Precipitation",
        "opacity": 0.7,
        "colormap": "blues"
    }
)

# When receiver gets this package, they know to render it as a 2D overlay
print(f"Visualization type: {weather_overlay.visualization_type}")
```

### 2. Point Clouds (Scattered Data)

Use `"point_cloud"` for discrete data points like sensor readings.

```python
# Weather station data
station_data = {
    "locations": [
        {"lat": 40.7128, "lon": -74.0060, "elevation": 10},   # NYC
        {"lat": 40.6892, "lon": -74.0445, "elevation": 5},    # Jersey City  
        {"lat": 40.7505, "lon": -73.9934, "elevation": 20}    # Queens
    ],
    "values": [22.5, 21.8, 23.1],  # Temperature readings
    "station_ids": ["NYC001", "JC002", "QNS003"]
}

station_package = MyrezeDataPackage(
    id="weather-stations",
    data=station_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    visualization_type="point_cloud",
    metadata={
        "parameter": "temperature",
        "units": "celsius",
        "point_size": 5,
        "color_scale": "temperature"
    }
)
```

### 3. Vector Fields (Directional Data)

Use `"vector_field"` for data with direction and magnitude like wind or currents.

```python
# Wind data
wind_data = {
    "grid_points": {
        "lats": np.linspace(40.5, 41.0, 20),
        "lons": np.linspace(-74.5, -73.5, 20)
    },
    "u_component": np.random.randn(20, 20) * 5,  # East-west wind
    "v_component": np.random.randn(20, 20) * 3,  # North-south wind
    "magnitude": np.random.rand(20, 20) * 10     # Wind speed
}

wind_package = MyrezeDataPackage(
    id="wind-field",
    data=wind_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    visualization_type="vector_field",
    metadata={
        "parameter": "wind_velocity",
        "units": "m/s",
        "arrow_scale": 2.0,
        "color_by": "magnitude"
    }
)
```

### 4. Time Series Data

Use `"trajectory"` for data that changes over time along a path.

```python
# Hurricane track
track_times = [
    "2023-08-20T00:00:00Z",
    "2023-08-20T06:00:00Z", 
    "2023-08-20T12:00:00Z",
    "2023-08-20T18:00:00Z"
]

hurricane_data = {
    "positions": [
        {"lat": 25.0, "lon": -80.0, "pressure": 980},
        {"lat": 26.0, "lon": -81.0, "pressure": 975},
        {"lat": 27.0, "lon": -82.0, "pressure": 970},
        {"lat": 28.0, "lon": -83.0, "pressure": 965}
    ],
    "wind_speeds": [65, 70, 75, 80],  # mph
    "categories": [1, 1, 1, 2]
}

hurricane_package = MyrezeDataPackage(
    id="hurricane-track",
    data=hurricane_data,
    time=Time.series(track_times),
    visualization_type="trajectory",
    metadata={
        "storm_name": "Hurricane Example",
        "animate": True,
        "trail_length": 24  # hours
    }
)
```

## Visualization with Different Engines

### Unreal Engine Visualization

```python
from myreze.viz import UnrealRenderer

# 3D terrain data
terrain_data = {
    "elevation": np.random.rand(100, 100) * 1000,  # Elevation in meters
    "bounds": [-74.0, 40.7, -73.9, 40.8],         # Geographic bounds
    "texture_layers": {
        "satellite": "path/to/satellite_image.jpg",
        "vegetation": np.random.rand(100, 100, 3)   # RGB vegetation data
    }
}

terrain_package = MyrezeDataPackage(
    id="terrain-3d",
    data=terrain_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    unreal_visualization=UnrealRenderer(),
    visualization_type="terrain",
    metadata={
        "vertical_scale": 2.0,
        "material_type": "pbr",
        "lighting": "dynamic"
    }
)

# Generate Unreal Engine visualization
# The visualization_type tells Unreal how to interpret the data
unreal_output = terrain_package.to_unreal(params={"quality": "high"})
```

### Three.js Visualization

```python
from myreze.viz import ThreeJSRenderer

# Heatmap data
heatmap_data = {
    "grid": np.random.rand(50, 50),
    "bounds": [-74.1, 40.6, -73.8, 40.9],
    "values_range": [0, 100]
}

heatmap_package = MyrezeDataPackage(
    id="temperature-heatmap",
    data=heatmap_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    threejs_visualization=ThreeJSRenderer(),
    visualization_type="heatmap",
    metadata={
        "colormap": "viridis",
        "opacity": 0.8,
        "smooth_interpolation": True
    }
)

# Generate Three.js visualization
# The visualization_type guides the Three.js renderer
threejs_output = heatmap_package.to_threejs(params={"format": "glb"})
```

## Best Practices

### 1. Choose Appropriate Visualization Types

```python
# ✅ Good: Clear visualization type for the data
weather_stations = MyrezeDataPackage(
    id="stations",
    data=point_data,
    time=time_data,
    visualization_type="point_cloud"  # Clear intent
)

# ❌ Avoid: Generic or missing visualization type
unclear_package = MyrezeDataPackage(
    id="data",
    data=some_data,
    time=time_data,
    visualization_type=""  # Unclear how to visualize
)
```

### 2. Include Relevant Metadata

```python
# ✅ Good: Rich metadata that helps with visualization
detailed_package = MyrezeDataPackage(
    id="wind-vectors",
    data=wind_data,
    time=time_data,
    visualization_type="vector_field",
    metadata={
        "units": "m/s",
        "color_scale": "magnitude",
        "arrow_scale": 1.5,
        "min_magnitude": 0,
        "max_magnitude": 25
    }
)
```

### 3. Match Data Structure to Visualization Type

```python
# ✅ Good: Data structure matches visualization type
overlay_data = {
    "grid": np.array([[...]]),      # 2D grid for overlay
    "bounds": [west, south, east, north],
    "resolution": 0.01
}

overlay_package = MyrezeDataPackage(
    id="temperature-overlay",
    data=overlay_data,
    time=time_data,
    visualization_type="flat_overlay"  # Matches the data structure
)
```

## Working with Received Packages

When you receive a `MyrezeDataPackage`, use the `visualization_type` to determine how to process it:

```python
def process_package(package: MyrezeDataPackage):
    """Process a data package based on its visualization type."""
    
    if package.visualization_type == "flat_overlay":
        # Handle as 2D map overlay
        return render_2d_overlay(package)
    
    elif package.visualization_type == "point_cloud":
        # Handle as scattered points
        return render_points(package)
    
    elif package.visualization_type == "vector_field":
        # Handle as directional vectors
        return render_vectors(package)
    
    elif package.visualization_type == "heatmap":
        # Handle as continuous surface
        return render_heatmap(package)
    
    else:
        # Fallback for unknown types
        print(f"Unknown visualization type: {package.visualization_type}")
        return render_generic(package)

# Load and process a package
received_package = MyrezeDataPackage.from_json(json_data)
visualization = process_package(received_package) 