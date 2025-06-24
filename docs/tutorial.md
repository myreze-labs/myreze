# Myreze Tutorial

This comprehensive tutorial will guide you through creating data packages, setting up data stores, and rendering visualizations with different engines. Perfect for junior developers getting started with Myreze.

## Table of Contents

1. [Getting Started: Your First Data Package](#getting-started)
2. [Understanding Visualization Types](#understanding-visualization-types)
3. [Working with Time](#working-with-time)
4. [Creating Data Stores and Products](#creating-data-stores-and-products)
5. [Visualization Engines](#visualization-engines)
6. [Best Practices](#best-practices)
7. [Common Patterns](#common-patterns)

## Getting Started: Your First Data Package {#getting-started}

Let's start with the basics. A `MyrezeDataPackage` is like a smart container for your geospatial data.

```python
from myreze.data import MyrezeDataPackage, Time
import numpy as np

# Step 1: Create some sample data (temperature readings)
temperature_data = {
    "grid": np.array([[20.5, 21.0, 19.8], 
                      [22.1, 23.5, 21.9], 
                      [19.2, 20.8, 22.3]]),  # 3x3 grid of temperatures
    "bounds": [-74.1, 40.6, -73.9, 40.9],    # NYC area [west, south, east, north]
    "units": "celsius"
}

# Step 2: Create time information
time_data = Time.timestamp("2023-01-01T12:00:00Z")

# Step 3: Package it all together
data_package = MyrezeDataPackage(
    id="tutorial-example-1",
    data=temperature_data,
    time=time_data,
    visualization_type="heatmap",  # This tells receivers how to visualize the data
    metadata={
        "source": "weather_station", 
        "description": "Temperature readings from NYC area",
        "units": "celsius"
    }
)

print(f"Created package with ID: {data_package.id}")
print(f"Visualization type: {data_package.visualization_type}")
print(f"Data keys: {list(data_package.data.keys())}")
```

**Key Points for Beginners:**
- The `visualization_type` is crucial - it tells anyone receiving your package how to display the data
- Always include metadata - it helps others understand your data
- The `bounds` array follows the pattern [west, south, east, north] (longitude, latitude order)

## Understanding Visualization Types

The `visualization_type` field is like giving instructions to a visualization engine. Here's how to choose the right one:

### 1. Heatmaps and Flat Overlays (Grid Data)

Use `"heatmap"` or `"flat_overlay"` when you have data arranged in a regular grid.

```python
# Weather radar data showing precipitation intensity
radar_data = {
    "grid": np.random.rand(100, 100),  # Precipitation intensity (0-1)
    "bounds": [-74.5, 40.5, -73.5, 41.0],  # Geographic area
    "resolution": 0.01,  # degrees per grid cell
    "units": "mm/hour"
}

radar_package = MyrezeDataPackage(
    id="precipitation-radar",
    data=radar_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    visualization_type="heatmap",  # Continuous data surface
    metadata={
        "parameter": "precipitation_intensity",
        "colormap": "blues",  # Suggestion for visualization
        "opacity": 0.7,
        "data_source": "weather_radar"
    }
)

print(f"Grid dimensions: {radar_data['grid'].shape}")
print(f"Coverage area: {radar_data['bounds']}")
```

**When to use:**
- ✅ Temperature maps, pressure fields, elevation data
- ✅ Weather radar, satellite imagery
- ✅ Any data that varies continuously across space

### 2. Point Clouds (Scattered Data)

Use `"point_cloud"` for discrete measurements at specific locations.

```python
# Weather stations with readings at specific locations
station_data = {
    "locations": [
        {"lat": 40.7128, "lon": -74.0060, "elevation": 10, "station_id": "NYC001"},
        {"lat": 40.6892, "lon": -74.0445, "elevation": 5, "station_id": "JC002"},
        {"lat": 40.7505, "lon": -73.9934, "elevation": 20, "station_id": "QNS003"},
        {"lat": 40.8176, "lon": -73.9782, "elevation": 15, "station_id": "BX004"}
    ],
    "values": [22.5, 21.8, 23.1, 20.9],  # Temperature readings
    "parameter": "air_temperature",
    "measurement_time": "2023-06-15T14:30:00Z"
}

station_package = MyrezeDataPackage(
    id="weather-stations-nyc",
    data=station_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    visualization_type="point_cloud",
    metadata={
        "parameter": "temperature",
        "units": "celsius",
        "point_size": 8,  # Visualization hint
        "color_scale": "temperature",  # How to color the points
        "network": "NYC Weather Network"
    }
)

print(f"Number of stations: {len(station_data['locations'])}")
print(f"Temperature range: {min(station_data['values']):.1f}°C to {max(station_data['values']):.1f}°C")
```

**When to use:**
- ✅ Weather stations, air quality sensors
- ✅ GPS tracking points, survey data
- ✅ Any measurements at discrete locations

### 3. Vector Fields (Directional Data)

Use `"vector_field"` for data that has both magnitude and direction.

```python
# Wind field data - wind has both speed and direction
grid_size = 15
lats = np.linspace(40.6, 40.9, grid_size)
lons = np.linspace(-74.1, -73.9, grid_size)

# Create a realistic wind pattern (simplified)
wind_data = {
    "grid_points": {
        "lats": lats.tolist(),
        "lons": lons.tolist()
    },
    "u_component": (np.random.randn(grid_size, grid_size) * 3 + 5).tolist(),  # East-west wind
    "v_component": (np.random.randn(grid_size, grid_size) * 2).tolist(),      # North-south wind
    "units": "m/s",
    "measurement_height": "10m"
}

# Calculate magnitude for metadata
u_array = np.array(wind_data["u_component"])
v_array = np.array(wind_data["v_component"])
magnitude = np.sqrt(u_array**2 + v_array**2)

wind_package = MyrezeDataPackage(
    id="wind-field-nyc",
    data=wind_data,
    time=Time.timestamp("2023-06-15T14:30:00Z"),
    visualization_type="vector_field",
    metadata={
        "parameter": "wind_velocity",
        "arrow_scale": 2.0,  # How big to draw arrows
        "color_by": "magnitude",  # Color arrows by wind speed
        "wind_speed_range": [float(magnitude.min()), float(magnitude.max())],
        "data_source": "weather_model"
    }
)

print(f"Wind grid: {grid_size}x{grid_size} points")
print(f"Wind speed range: {magnitude.min():.1f} to {magnitude.max():.1f} m/s")
```

**When to use:**
- ✅ Wind patterns, ocean currents
- ✅ Magnetic fields, flow fields
- ✅ Any data with direction and magnitude

### 4. Trajectories (Paths Over Time)

Use `"trajectory"` for data that represents movement or paths over time.

```python
# Hurricane track - positions over time
track_times = [
    "2023-08-20T00:00:00Z",
    "2023-08-20T06:00:00Z", 
    "2023-08-20T12:00:00Z",
    "2023-08-20T18:00:00Z",
    "2023-08-21T00:00:00Z"
]

hurricane_data = {
    "positions": [
        {"lat": 25.0, "lon": -80.0, "pressure": 980, "timestamp": track_times[0]},
        {"lat": 26.2, "lon": -81.1, "pressure": 975, "timestamp": track_times[1]},
        {"lat": 27.4, "lon": -82.2, "pressure": 970, "timestamp": track_times[2]},
        {"lat": 28.6, "lon": -83.3, "pressure": 965, "timestamp": track_times[3]},
        {"lat": 29.8, "lon": -84.4, "pressure": 960, "timestamp": track_times[4]}
    ],
    "wind_speeds": [65, 70, 75, 80, 85],  # mph
    "storm_categories": [1, 1, 1, 2, 2],  # Saffir-Simpson scale
    "storm_id": "AL042023"
}

hurricane_package = MyrezeDataPackage(
    id="hurricane-track-2023",
    data=hurricane_data,
    time=Time.series(track_times),
    visualization_type="trajectory",
    metadata={
        "storm_name": "Hurricane Example",
        "data_source": "National Hurricane Center",
        "animate": True,
        "trail_length": 24,  # Show 24 hours of trail
        "color_by": "wind_speed"
    }
)

print(f"Track duration: {len(track_times)} points over {len(track_times)*6} hours")
print(f"Peak wind speed: {max(hurricane_data['wind_speeds'])} mph")
```

**When to use:**
- ✅ Storm tracks, flight paths, vehicle routes
- ✅ Animal migration, ship tracking
- ✅ Any data that represents movement over time

## Working with Time

Myreze supports three types of time representations. Choose based on your data:

### Timestamp (Single Point in Time)

```python
from myreze.data import Time

# For data captured at a specific moment
single_time = Time.timestamp("2023-07-15T14:30:00Z")
print(f"Timestamp: {single_time.to_dict()}")
```

### Time Span (Duration/Range)

```python
# For data covering a time period
time_range = Time.span("2023-07-01T00:00:00Z", "2023-07-31T23:59:59Z")
print(f"Time span: {time_range.to_dict()}")
```

### Time Series (Multiple Points)

```python
# For data at multiple specific times
measurement_times = [
    "2023-07-15T12:00:00Z",
    "2023-07-15T13:00:00Z",
    "2023-07-15T14:00:00Z",
    "2023-07-15T15:00:00Z"
]
time_series = Time.series(measurement_times)
print(f"Time series: {len(measurement_times)} time points")
```

## Creating Data Stores and Products

Now let's learn how to create data services that can generate packages on demand. This is powerful for creating APIs that serve data.

### Understanding the Store Concept

Think of a store as a data vending machine:
- **Products**: Different types of data you offer (weather, traffic, etc.)
- **Provider**: Your catalog of available products
- **Server**: The web service that handles requests

### Step 1: Create a Simple Product

```python
from myreze.store.product import Product
from myreze.data import MyrezeDataPackage, Time
import numpy as np
from typing import Dict, Any, Optional

class TemperatureProduct(Product):
    """A product that generates temperature data for any requested area."""
    
    async def generate_package(
        self,
        spatial_region: Dict[str, Any],
        temporal_region: Dict[str, Any],
        visualization: Optional[Dict[str, Any]] = None
    ) -> MyrezeDataPackage:
        
        # Extract the requested area bounds
        coords = spatial_region["coordinates"]
        west, south = coords[0]
        east, north = coords[1]
        
        # Generate synthetic temperature data for the requested area
        # In a real application, you'd fetch this from a database or API
        grid_size = 50
        temp_grid = np.random.rand(grid_size, grid_size) * 20 + 15  # 15-35°C
        
        # Add some realistic spatial variation
        center_y, center_x = grid_size // 2, grid_size // 2
        y, x = np.ogrid[:grid_size, :grid_size]
        distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        temp_grid += 3 * np.exp(-distance_from_center / 15)  # Urban heat island effect
        
        data = {
            "grid": temp_grid,
            "bounds": [west, south, east, north],
            "resolution": (east - west) / grid_size,
            "units": "celsius"
        }
        
        return MyrezeDataPackage(
            id=f"temperature-{temporal_region['value']}-{hash(str(coords)) % 10000}",
            data=data,
            time=Time.from_dict(temporal_region),
            visualization_type="heatmap",
            metadata={
                "product": "temperature_analysis",
                "generated_at": temporal_region['value'],
                "spatial_bounds": coords,
                "description": f"Temperature data for area ({west:.2f}, {south:.2f}) to ({east:.2f}, {north:.2f})"
            }
        )
```

### Step 2: Create a Provider

```python
from myreze.store.provider import ProductProvider
from typing import List

class WeatherDataProvider(ProductProvider):
    """A provider that offers weather-related products."""
    
    async def get_products(self) -> List[Product]:
        """Return the list of products this provider offers."""
        return [
            TemperatureProduct(
                product_id="real-time-temperature",
                name="Real-time Temperature Data",
                description="Current temperature readings and analysis",
                source="Weather Network",
                data_types=["temperature", "heat_index"],
                spatial_coverage={
                    "type": "BoundingBox",
                    "coordinates": [[-180, -90], [180, 90]]  # Global coverage
                },
                temporal_coverage={
                    "type": "Capability",
                    "supports_historical": True,
                    "earliest_date": "2020-01-01T00:00:00Z",
                    "latest_date": "2030-12-31T23:59:59Z",
                    "supports_forecast": False
                },
                availability={"public": True, "requires_auth": False},
                visualization_type="heatmap"
            ),
            # You can add more products here
        ]
```

### Step 3: Run the Store Server

```python
from myreze.store.server import StoreServer

def run_weather_store():
    """Start the weather data store server."""
    provider = WeatherDataProvider()
    server = StoreServer(provider)
    
    print("Starting weather data store on http://localhost:8000")
    print("Available endpoints:")
    print("  GET /products - List available products")
    print("  POST /orders - Order data packages")
    
    server.run()

# Run this in your main script
if __name__ == "__main__":
    run_weather_store()
```

### Step 4: Using Your Store

Once your store is running, you can test it:

```bash
# List available products
curl http://localhost:8000/products

# Order temperature data for Manhattan
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "real-time-temperature",
    "spatial_region": {
      "type": "BoundingBox", 
      "coordinates": [[-74.02, 40.70], [-73.93, 40.78]]
    },
    "temporal_region": {
      "type": "Timestamp", 
      "value": "2023-07-15T14:30:00Z"
    }
  }'
```

## Visualization Engines

### Three.js for Web Applications

Three.js is perfect for interactive web visualizations:

```python
from myreze.viz import ThreeJSRenderer

# Create a package with Three.js visualization
web_package = MyrezeDataPackage(
    id="web-temperature-viz",
    data=temperature_data,
    time=Time.timestamp("2023-07-15T14:30:00Z"),
    threejs_visualization=ThreeJSRenderer(),
    visualization_type="heatmap",
    metadata={"target_platform": "web"}
)

# Generate the visualization
threejs_output = web_package.to_threejs(params={
    "format": "glb",  # 3D model format
    "quality": "medium",
    "interactive": True
})

print("Generated Three.js visualization for web deployment")
```

### Unreal Engine for High-Quality 3D

Unreal Engine provides broadcast-quality 3D visualizations:

```python
from myreze.viz import UnrealRenderer

# Create terrain data for Unreal
terrain_data = {
    "elevation": np.random.rand(200, 200) * 1000,  # Elevation in meters
    "bounds": [-74.1, 40.6, -73.9, 40.9],
    "texture_layers": {
        "base_color": np.random.rand(200, 200, 3),  # RGB base texture
        "normal_map": np.random.rand(200, 200, 3)   # Surface normals
    }
}

unreal_package = MyrezeDataPackage(
    id="unreal-terrain",
    data=terrain_data,
    time=Time.timestamp("2023-07-15T14:30:00Z"),
    unreal_visualization=UnrealRenderer(),
    visualization_type="terrain",
    metadata={"target_platform": "unreal_engine"}
)

# Generate high-quality 3D visualization
unreal_output = unreal_package.to_unreal(params={
    "quality": "ultra",
    "lighting": "dynamic",
    "materials": "pbr"  # Physically-based rendering
})
```

## Best Practices

### 1. Choose the Right Visualization Type

```python
# ✅ Good: Clear, appropriate visualization type
weather_data = {
    "grid": temperature_grid,
    "bounds": bounds,
    "units": "celsius"
}

good_package = MyrezeDataPackage(
    id="clear-weather-data",
    data=weather_data,
    time=time_data,
    visualization_type="heatmap",  # Perfect for grid data
    metadata={"parameter": "temperature"}
)

# ❌ Avoid: Wrong visualization type for data structure
scattered_points = {
    "locations": [{"lat": 40.7, "lon": -74.0}],
    "values": [25.0]
}

bad_package = MyrezeDataPackage(
    id="confused-data",
    data=scattered_points,
    time=time_data,
    visualization_type="heatmap",  # Wrong! This is point data, not a grid
    metadata={}
)
```

### 2. Include Rich Metadata

```python
# ✅ Good: Comprehensive metadata
detailed_package = MyrezeDataPackage(
    id="well-documented-data",
    data=wind_data,
    time=time_data,
    visualization_type="vector_field",
    metadata={
        "parameter": "wind_velocity",
        "units": "m/s",
        "measurement_height": "10m",
        "data_source": "NOAA Weather Station Network",
        "quality_level": "research_grade",
        "arrow_scale": 1.5,  # Visualization hint
        "color_scale": "magnitude",  # How to color the arrows
        "min_magnitude": 0,
        "max_magnitude": 25,
        "description": "10-meter wind measurements from automated weather stations"
    }
)
```

### 3. Validate Your Data Structure

```python
# Always validate before sending
from myreze.data.validate import validate_visualization_data

data = {"grid": temperature_grid, "bounds": bounds}
errors = validate_visualization_data(data, "heatmap")

if errors:
    print(f"Data validation errors: {errors}")
    # Fix the errors before proceeding
else:
    print("✅ Data structure is valid")
    # Create the package
```

### 4. Handle Time Zones Properly

```python
# ✅ Good: Always use UTC timestamps
utc_time = Time.timestamp("2023-07-15T14:30:00Z")  # 'Z' indicates UTC

# ✅ Good: Be explicit about time zones in metadata
package = MyrezeDataPackage(
    id="timezone-aware",
    data=data,
    time=utc_time,
    visualization_type="heatmap",
    metadata={
        "local_timezone": "America/New_York",
        "local_time": "2023-07-15T10:30:00-04:00",
        "utc_time": "2023-07-15T14:30:00Z"
    }
)
```

## Common Patterns

### Pattern 1: Loading and Processing Received Packages

```python
def process_received_package(json_data: str):
    """Process a data package received from another system."""
    
    # Load the package
    package = MyrezeDataPackage.from_json(json_data)
    
    # Check the visualization type to determine processing
    if package.visualization_type == "heatmap":
        grid = package.data["grid"]
        bounds = package.data["bounds"]
        print(f"Processing heatmap: {grid.shape} grid covering {bounds}")
        
    elif package.visualization_type == "point_cloud":
        locations = package.data["locations"]
        values = package.data["values"]
        print(f"Processing {len(locations)} point measurements")
        
    elif package.visualization_type == "vector_field":
        u_comp = package.data["u_component"]
        v_comp = package.data["v_component"]
        print(f"Processing vector field with {len(u_comp)} vectors")
        
    else:
        print(f"Unknown visualization type: {package.visualization_type}")
    
    return package
```

### Pattern 2: Creating Multi-Layer Packages

```python
def create_weather_analysis_package():
    """Create a package with multiple data layers."""
    
    # Base temperature layer
    temp_data = {
        "grid": np.random.rand(100, 100) * 20 + 15,
        "bounds": [-74.1, 40.6, -73.9, 40.9],
        "units": "celsius"
    }
    
    # Wind overlay
    wind_data = {
        "u_component": np.random.randn(20, 20) * 5,
        "v_component": np.random.randn(20, 20) * 3,
        "grid_points": {
            "lats": np.linspace(40.6, 40.9, 20).tolist(),
            "lons": np.linspace(-74.1, -73.9, 20).tolist()
        }
    }
    
    # Combined package
    combined_data = {
        "temperature_layer": temp_data,
        "wind_layer": wind_data,
        "layer_types": ["heatmap", "vector_field"]
    }
    
    return MyrezeDataPackage(
        id="multi-layer-weather",
        data=combined_data,
        time=Time.timestamp("2023-07-15T14:30:00Z"),
        visualization_type="multi_layer",
        metadata={
            "description": "Combined temperature and wind analysis",
            "primary_layer": "temperature",
            "overlay_layers": ["wind"]
        }
    )
```

### Pattern 3: Error Handling

```python
def safe_package_creation(data, visualization_type):
    """Safely create a package with proper error handling."""
    
    try:
        # Validate the data structure first
        from myreze.data.validate import validate_visualization_data
        errors = validate_visualization_data(data, visualization_type)
        
        if errors:
            raise ValueError(f"Data validation failed: {errors}")
        
        # Create the package
        package = MyrezeDataPackage(
            id=f"safe-package-{int(time.time())}",
            data=data,
            time=Time.timestamp("2023-07-15T14:30:00Z"),
            visualization_type=visualization_type
        )
        
        # Test serialization
        json_str = package.to_json()
        restored = MyrezeDataPackage.from_json(json_str)
        
        print("✅ Package created and validated successfully")
        return package
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return None
```

This tutorial should give you a solid foundation for working with Myreze. Remember to always think about your data structure first, choose the appropriate visualization type, and include rich metadata to help others understand your data.

For more advanced features and examples, check out the `examples/` directory in the Myreze repository.