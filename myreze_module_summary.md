# Myreze Module Summary

## Overview

**Myreze** is an open-source Python package designed as a comprehensive geospatial data processing and visualization toolkit, specifically architected to facilitate seamless dataflow into high-quality 3D visualization engines. The module serves as the foundational scaffolding for the proprietary "Weather by Myreze" SaaS framework, enabling the delivery of professional virtual weather broadcasts and geospatial visualizations.

**Current Version**: 0.0.5 (Published on PyPI)  
**License**: MIT License  
**Python Compatibility**: >=3.6  

## Architecture

Myreze follows a modular architecture built around three core components:

### 1. Data Layer (`myreze.data`)
- **Core Data Structures**: Standardized containers for geospatial data
- **Time Handling**: Flexible temporal data representation
- **Validation**: Schema-based data integrity checking
- **Serialization**: JSON-compatible data package export/import

### 2. Visualization Layer (`myreze.viz`)
- **Multi-Platform Renderers**: Abstract renderer system supporting:
  - **Three.js**: Web-based 3D visualizations
  - **Unreal Engine**: High-fidelity 3D game engine integration
  - **PNG Export**: Static image generation
- **Specialized Renderers**: Domain-specific visualization components
- **Extensible Plugin System**: Registry-based renderer registration

### 3. Store Layer (`myreze.store`)
- **Product Management**: Catalog system for data products
- **API Server**: FastAPI-based RESTful data serving
- **Provider System**: Pluggable data source integration
- **Spatial/Temporal Validation**: Request validation against product capabilities

## Core Data Structures

### MyrezeDataPackage
The central data container that encapsulates:
- **Unique Identifier**: Package ID for tracking
- **Geospatial Data**: NumPy arrays, coordinate systems, geometric data
- **Temporal Information**: Timestamps, time spans, or time series
- **Visualization Metadata**: Rendering hints and configuration
- **Multi-Format Export**: JSON serialization with NumPy array handling

```python
data_package = MyrezeDataPackage(
    id="weather-overlay-001",
    data={"temperature_grid": numpy_array, "bounds": coordinates},
    time=Time.timestamp("2023-01-01T12:00:00Z"),
    visualization_type="flat_overlay",
    threejs_visualization=ThreeJSRenderer(),
    unreal_visualization=UnrealRenderer()
)
```

### Time System
Flexible temporal data representation supporting:
- **Timestamps**: Single point-in-time (ISO 8601)
- **Time Spans**: Duration periods with start/end
- **Time Series**: Ordered sequences of timestamps
- **Validation**: Automatic ISO 8601 format validation

### Geometry System
Standardized geometric data representation for:
- Coordinate system handling
- Geographic bounds definition
- Spatial region validation

## Visualization Capabilities

### Three.js Integration
- **Web-Ready 3D**: Browser-compatible visualization export
- **Flat Overlays**: 2D texture mapping for weather data
- **Interactive Elements**: Support for web-based user interaction
- **GLB Export**: 3D model generation with embedded textures

### Unreal Engine Integration
- **High-Fidelity Rendering**: Professional game engine visualization
- **Cloud Rendering**: Volumetric atmospheric effects
- **Terrain Integration**: 3D landscape data handling
- **Real-time Capabilities**: Dynamic data updates

### PNG Export
- **Static Visualization**: Image generation for reports
- **Transparent Overlays**: Alpha channel support
- **Multi-channel Data**: RGBA texture handling

## Store and API System

### FastAPI Server
RESTful API providing:
- **Product Catalog**: Available data product listings
- **Order Processing**: Spatial/temporal data requests
- **Validation**: Request validation against product capabilities
- **Async Operations**: Non-blocking data generation

### Product System
- **Flexible Providers**: Pluggable data source integration
- **Capability Metadata**: Spatial/temporal coverage definitions
- **Data Type Support**: Multiple data format handling
- **Access Control**: Public/private product availability

## Key Features

### 1. Standardized Data Flow
- Unified interface for diverse geospatial data sources
- Consistent data package format across visualization engines
- Seamless conversion between different output formats

### 2. Multi-Platform Visualization
- Single data source → multiple visualization targets
- Platform-specific optimization and rendering
- Extensible renderer architecture for new platforms

### 3. Professional Weather Broadcasting
- Optimized for meteorological data visualization
- Support for atmospheric effects and weather overlays
- Time-series animation capabilities
- Integration with weather data providers

### 4. Geospatial Standards Compliance
- Web Mercator WGS84 (EPSG 3857) coordinate system
- Normalized (0,1) planar region output
- Consistent spatial orientation (Y-up convention)
- Layer-based rendering at Y=0 offset

### 5. Production-Ready Infrastructure
- FastAPI-based scalable API server
- Async data processing capabilities
- Comprehensive error handling and validation
- Docker-ready deployment architecture

## Dependencies and Technical Stack

### Core Dependencies
- **NumPy**: Numerical array processing
- **Trimesh**: 3D mesh generation and manipulation
- **Isodate**: ISO 8601 datetime parsing
- **Rasterio**: Geospatial raster data processing
- **FastAPI**: Modern API framework
- **Pydantic**: Data validation and serialization

### Development Tools
- **Setuptools**: Package building and distribution
- **Twine**: PyPI package uploading
- **Uvicorn**: ASGI server for FastAPI

## Usage Patterns

### Data Package Creation
```python
from myreze.data import MyrezeDataPackage, Time

# Weather overlay example
data_package = MyrezeDataPackage(
    id="temperature-forecast",
    data={"grid": temperature_array, "bounds": geographic_bounds},
    time=Time.span("2023-01-01T00:00:00Z", "2023-01-07T23:59:59Z"),
    visualization_type="flat_overlay"
)

# Export for visualization
threejs_output = data_package.to_threejs(params={})
unreal_output = data_package.to_unreal(params={})
```

### Store Server Deployment
```python
from myreze.store import StoreServer, ProductProvider

# Set up data products
provider = WeatherProductProvider()
server = StoreServer(provider)
server.run(host="0.0.0.0", port=8000)

# API endpoints available:
# GET /products - List available data products
# POST /orders - Request data packages with spatial/temporal filters
```

## Integration with Weather by Myreze

The module serves as the technical foundation for the commercial Weather by Myreze platform:

- **Data Ingestion**: Standardized pipeline for weather data sources
- **Visualization Pipeline**: Automated conversion to broadcast-ready formats
- **API Infrastructure**: Scalable data serving for client applications
- **Quality Assurance**: Built-in validation and error handling
- **Multi-Platform Delivery**: Simultaneous output to multiple visualization engines

## Development Status

The module is actively developed and maintained, with regular PyPI releases. The current focus areas include:

- Enhanced visualization renderer capabilities
- Expanded geospatial data format support
- Performance optimization for large datasets
- Additional visualization platform integrations
- Improved documentation and examples

## Conclusion

Myreze represents a sophisticated approach to geospatial data visualization, providing a unified interface for complex 3D visualization workflows. Its modular architecture, comprehensive feature set, and production-ready infrastructure make it suitable for both standalone applications and integration into larger geospatial visualization systems. The module's particular strength in weather data visualization and broadcasting applications demonstrates its specialized capabilities while maintaining flexibility for broader geospatial use cases. 