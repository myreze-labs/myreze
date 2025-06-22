#!/usr/bin/env python
"""
Comprehensive example of creating Myreze data packages.

This example demonstrates the key patterns LLM agents should follow when
creating data packages with different visualization types. It shows:

1. How to determine appropriate visualization types
2. How to structure data for each type
3. How to set proper metadata
4. How to validate packages
5. How to handle errors

Run this script to see working examples of all major visualization types.
"""

import numpy as np
from myreze.data import MyrezeDataPackage, Time
from myreze.viz import FlatOverlayRenderer
from myreze.data.validate import (
    validate_visualization_data,
    suggest_visualization_type,
    get_visualization_requirements,
)


def create_heatmap_example():
    """
    Create a temperature heatmap data package.

    This demonstrates the flat_overlay/heatmap pattern for continuous
    2D data like temperature, pressure, or elevation fields.
    """
    print("Creating heatmap example...")

    # Generate synthetic temperature data for NYC area
    # Temperature varies from 15°C to 35°C across a 50x50 grid
    temperature_grid = np.random.rand(50, 50) * 20 + 15  # 15-35°C

    # Add some realistic patterns (warmer in center, cooler at edges)
    center_y, center_x = 25, 25
    y, x = np.ogrid[:50, :50]
    distance_from_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    temperature_grid += 5 * np.exp(-distance_from_center / 10)

    # Structure data according to heatmap schema
    data = {
        "grid": temperature_grid,
        "bounds": [-74.1, 40.6, -73.9, 40.9],  # NYC area bounds
        "resolution": 0.004,  # degrees per pixel
        "units": "celsius",
        "values_range": [temperature_grid.min(), temperature_grid.max()],
    }

    # Create the data package
    package = MyrezeDataPackage(
        id="nyc-temperature-heatmap",
        data=data,
        time=Time.timestamp("2023-07-15T14:30:00Z"),  # Hot summer afternoon
        threejs_visualization=ThreeJSRenderer(),
        visualization_type="heatmap",
        metadata={
            "description": "Temperature heatmap for NYC area",
            "colormap": "viridis",
            "parameter": "air_temperature",
            "data_source": "synthetic_example",
            "opacity": 0.8,
        },
    )

    # Validate the data structure
    validation_errors = validate_visualization_data(data, "heatmap")
    if validation_errors:
        print(f"  ❌ Validation errors: {validation_errors}")
    else:
        print("  ✅ Data structure valid for heatmap visualization")

    # Show schema information
    schema = package.get_schema_info()
    print(f"  📋 Required fields: {schema.get('required_fields', [])}")
    print(f"  📝 Description: {schema.get('description', 'N/A')}")

    return package


def create_point_cloud_example():
    """
    Create a weather stations point cloud data package.

    This demonstrates the point_cloud pattern for discrete measurements
    at specific geographic locations.
    """
    print("\nCreating point cloud example...")

    # Generate synthetic weather station data
    np.random.seed(42)  # For reproducible example
    num_stations = 15

    # Random locations within NYC area
    lats = np.random.uniform(40.6, 40.9, num_stations)
    lons = np.random.uniform(-74.1, -73.9, num_stations)
    elevations = np.random.uniform(0, 100, num_stations)  # 0-100m elevation

    # Generate temperature readings (varies with elevation)
    base_temp = 25  # 25°C base temperature
    temperatures = base_temp - (elevations * 0.006)  # Lapse rate effect
    temperatures += np.random.normal(0, 2, num_stations)  # Measurement noise

    # Structure data according to point_cloud schema
    data = {
        "locations": [
            {"lat": float(lat), "lon": float(lon), "elevation": float(elev)}
            for lat, lon, elev in zip(lats, lons, elevations)
        ],
        "values": temperatures.tolist(),
        "point_ids": [f"NYC_STATION_{i:03d}" for i in range(num_stations)],
        "timestamps": ["2023-07-15T14:30:00Z"] * num_stations,  # All simultaneous
    }

    # Create the data package
    package = MyrezeDataPackage(
        id="nyc-weather-stations",
        data=data,
        time=Time.timestamp("2023-07-15T14:30:00Z"),
        threejs_visualization=ThreeJSRenderer(),
        visualization_type="point_cloud",
        metadata={
            "description": "Weather station temperature readings",
            "parameter": "air_temperature",
            "units": "celsius",
            "point_size": 8,
            "color_scale": "temperature",
            "data_source": "synthetic_weather_network",
        },
    )

    # Validate and show info
    validation_errors = validate_visualization_data(data, "point_cloud")
    if validation_errors:
        print(f"  ❌ Validation errors: {validation_errors}")
    else:
        print("  ✅ Data structure valid for point cloud visualization")

    print(f"  📊 Generated {num_stations} weather stations")
    print(
        f"  🌡️  Temperature range: {temperatures.min():.1f}°C to {temperatures.max():.1f}°C"
    )

    return package


def create_vector_field_example():
    """
    Create a wind field data package.

    This demonstrates the vector_field pattern for directional data
    like wind, ocean currents, or magnetic fields.
    """
    print("\nCreating vector field example...")

    # Create a 20x20 grid covering NYC area
    lats = np.linspace(40.6, 40.9, 20)
    lons = np.linspace(-74.1, -73.9, 20)

    # Generate synthetic wind field
    # Create a circular wind pattern (like around a low pressure system)
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing="ij")
    center_lat, center_lon = 40.75, -74.0

    # Calculate distance and angle from center
    dlat = lat_grid - center_lat
    dlon = lon_grid - center_lon
    distance = np.sqrt(dlat**2 + dlon**2)

    # Create circular wind pattern
    wind_speed = 15 * np.exp(-distance / 0.1)  # Wind speed decreases with distance
    wind_angle = np.arctan2(dlat, dlon) + np.pi / 2  # Circular flow

    # Convert to u/v components
    u_component = wind_speed * np.cos(wind_angle)  # East-west
    v_component = wind_speed * np.sin(wind_angle)  # North-south
    magnitude = np.sqrt(u_component**2 + v_component**2)

    # Structure data according to vector_field schema
    data = {
        "grid_points": {"lats": lats.tolist(), "lons": lons.tolist()},
        "u_component": u_component.tolist(),
        "v_component": v_component.tolist(),
        "magnitude": magnitude.tolist(),
        "units": "m/s",
    }

    # Create the data package
    package = MyrezeDataPackage(
        id="nyc-wind-field",
        data=data,
        time=Time.timestamp("2023-07-15T14:30:00Z"),
        threejs_visualization=ThreeJSRenderer(),
        visualization_type="vector_field",
        metadata={
            "description": "Wind field over NYC area",
            "parameter": "wind_velocity",
            "arrow_scale": 2.0,
            "color_by": "magnitude",
            "data_source": "synthetic_weather_model",
        },
    )

    # Validate and show info
    validation_errors = validate_visualization_data(data, "vector_field")
    if validation_errors:
        print(f"  ❌ Validation errors: {validation_errors}")
    else:
        print("  ✅ Data structure valid for vector field visualization")

    print(f"  💨 Wind speed range: {magnitude.min():.1f} to {magnitude.max():.1f} m/s")
    print(f"  🎯 Grid size: {len(lats)} x {len(lons)} points")

    return package


def create_trajectory_example():
    """
    Create a storm track trajectory data package.

    This demonstrates the trajectory pattern for time-based paths
    like storm tracks, vehicle routes, or animal migration.
    """
    print("\nCreating trajectory example...")

    # Generate synthetic hurricane track moving northeast
    start_lat, start_lon = 25.0, -80.0  # Start near Florida

    # Track points over 4 days (6-hour intervals)
    times = []
    positions = []
    intensities = []

    for hour in range(0, 96, 6):  # Every 6 hours for 4 days
        # Move northeast with some randomness
        lat = start_lat + (hour / 24) * 1.5 + np.random.normal(0, 0.2)
        lon = start_lon + (hour / 24) * 2.0 + np.random.normal(0, 0.3)

        # Storm intensifies then weakens
        if hour < 48:
            intensity = 80 + hour * 0.5  # Strengthening
        else:
            intensity = 104 - (hour - 48) * 0.8  # Weakening

        time_str = f"2023-08-20T{hour:02d}:00:00Z"
        times.append(time_str)
        positions.append(
            {
                "lat": float(lat),
                "lon": float(lon),
                "pressure": int(1013 - intensity),  # Lower pressure = stronger storm
                "timestamp": time_str,
            }
        )
        intensities.append(float(intensity))

    # Structure data for trajectory visualization
    data = {
        "positions": positions,
        "intensities": intensities,
        "track_id": "EXAMPLE_2023",
        "storm_category": [1 if i < 96 else 2 if i < 111 else 1 for i in intensities],
    }

    # Create the data package
    package = MyrezeDataPackage(
        id="hurricane-example-track",
        data=data,
        time=Time.series(times),
        threejs_visualization=ThreeJSRenderer(),
        visualization_type="trajectory",
        metadata={
            "description": "Hurricane Example track forecast",
            "storm_name": "Hurricane Example",
            "data_source": "synthetic_nhc",
            "animate": True,
            "trail_length": 48,  # Show 48 hours of trail
            "color_by": "intensity",
        },
    )

    print(f"  ✅ Created trajectory with {len(positions)} positions")
    print(f"  🌀 Peak intensity: {max(intensities):.0f} kt")
    print(f"  📅 Duration: {len(times)} time points over 4 days")

    return package


def demonstrate_discovery_features():
    """
    Demonstrate the discovery features that help LLM agents understand
    the module capabilities.
    """
    print("\n" + "=" * 60)
    print("DISCOVERY FEATURES FOR LLM AGENTS")
    print("=" * 60)

    # Show available visualization types
    viz_types = MyrezeDataPackage.get_available_visualization_types()
    print(f"\n📋 Available visualization types: {viz_types}")

    # Show schema information for each type
    for viz_type in ["heatmap", "point_cloud", "vector_field"]:
        print(f"\n🔍 Schema for '{viz_type}':")
        reqs = get_visualization_requirements(viz_type)
        if reqs:
            print(f"  Description: {reqs.get('description', 'N/A')}")
            print(f"  Required fields: {reqs.get('required_fields', [])}")
            print(f"  Optional fields: {reqs.get('optional_fields', [])}")

    # Demonstrate auto-suggestion
    print(f"\n🤖 Auto-suggestion examples:")

    test_data_cases = [
        {"grid": [[1, 2], [3, 4]], "bounds": [-74, 40, -73, 41]},
        {"locations": [{"lat": 40.7, "lon": -74.0}], "values": [25.0]},
        {"grid_points": {"lats": [], "lons": []}, "u_component": [], "v_component": []},
    ]

    for i, test_data in enumerate(test_data_cases):
        suggestions = suggest_visualization_type(test_data)
        print(f"  Data {i+1}: {list(test_data.keys())} -> Suggested: {suggestions}")


def main():
    """
    Main function demonstrating comprehensive myreze usage patterns.
    """
    print("🚀 MYREZE DATA PACKAGE EXAMPLES")
    print("=" * 60)
    print("This script demonstrates key patterns for LLM agents using Myreze\n")

    try:
        # Create examples of different visualization types
        examples = []
        examples.append(create_heatmap_example())
        examples.append(create_point_cloud_example())
        examples.append(create_vector_field_example())
        examples.append(create_trajectory_example())

        # Show discovery features
        demonstrate_discovery_features()

        # Demonstrate serialization
        print(f"\n" + "=" * 60)
        print("SERIALIZATION EXAMPLES")
        print("=" * 60)

        for i, package in enumerate(examples):
            print(f"\n📦 Package {i+1}: {package.id}")

            # JSON serialization
            json_str = package.to_json()
            print(f"  JSON size: {len(json_str):,} characters")

            # Demonstrate deserialization
            restored_package = MyrezeDataPackage.from_json(json_str)
            print(f"  ✅ Successfully restored from JSON")
            print(f"  🏷️  Visualization type: {restored_package.visualization_type}")

            # Show metadata
            metadata_keys = list(restored_package.metadata.keys())
            print(f"  📝 Metadata keys: {metadata_keys}")

        print(f"\n✅ All examples completed successfully!")
        print(f"\nKey takeaways for LLM agents:")
        print(f"1. Always set visualization_type to match your data structure")
        print(f"2. Use schema validation to catch errors early")
        print(f"3. Include rich metadata for better visualization")
        print(f"4. Use discovery methods to understand capabilities")

    except Exception as e:
        print(f"❌ Error running examples: {e}")
        raise


if __name__ == "__main__":
    main()
