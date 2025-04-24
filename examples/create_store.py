from myreze.store.product import Product
from myreze.store.provider import ProductProvider
from myreze.store.server import StoreServer
from myreze.data import MyrezeDataPackage, Geometry, Time
import numpy as np
from typing import Dict, Any, Optional, List
import uuid


class WeatherProduct(Product):
    """A product for weather data."""

    async def generate_package(
        self,
        spatial_region: Dict[str, Any],
        temporal_region: Dict[str, Any],
        visualization: Optional[Dict[str, Any]] = None,
    ) -> MyrezeDataPackage:
        # Mock data fetching (replace with real source, e.g., ECMWF)
        data = {
            "temperature": np.random.rand(10, 10),
            "precipitation": np.random.rand(10, 10),
        }
        return MyrezeDataPackage(
            id=f"pkg-{uuid.uuid4()}",
            geometry=Geometry.from_dict(spatial_region),
            time=Time.from_dict(temporal_region),
            data=data,
            unreal_visualization=None,
            threejs_visualization=None,
        )


class FlexibleProductProvider(ProductProvider):
    """
    A provider that offers multiple products
    """

    async def get_products(self) -> List[Product]:
        """Return a list of available products with their capabilities."""
        return [
            WeatherProduct(
                product_id="weather-historical",
                name="Historical Weather Data",
                description="Past weather data from various sources.",
                source="Weather archive",
                data_types=["temperature", "precipitation", "humidity"],
                spatial_coverage={
                    "type": "BoundingBox",
                    "coordinates": [[-180, -90], [180, 90]],
                },
                temporal_coverage={
                    "type": "Capability",
                    "supports_historical": True,
                    "earliest_date": "1950-01-01T00:00:00Z",
                    "latest_date": "2023-12-31T23:59:59Z",
                    "supports_forecast": False,
                },
                availability={"public": True},
            ),
            WeatherProduct(
                product_id="weather-forecast",
                name="Weather Forecast",
                description="Future weather forecasts updated daily.",
                source="Weather model",
                data_types=["temperature", "precipitation", "wind"],
                spatial_coverage={
                    "type": "BoundingBox",
                    "coordinates": [[-180, -90], [180, 90]],
                },
                temporal_coverage={
                    "type": "Capability",
                    "supports_historical": False,
                    "supports_forecast": True,
                    "forecast_days_ahead": 10,
                    "update_frequency": "daily",
                },
                availability={"public": True},
            ),
        ]


# Run the store
if __name__ == "__main__":
    provider = FlexibleProductProvider()
    server = StoreServer(provider)
    server.run()


"""
After starting the store, you can make requests to the store using the following curl commands:

1. To get a list of available products (metadata only):
curl -X GET http://localhost:8000/products

2. To order a specific product (specifying the exact temporal range at order time):
curl -X POST http://localhost:8000/orders \\
  -H "Content-Type: application/json" \\
  -d '{
    "product_id": "weather-historical", 
    "spatial_region": {
      "type": "BoundingBox", 
      "coordinates": [[-10, 35], [25, 60]]
    }, 
    "temporal_region": {
      "type": "Span", 
      "value": {
        "start": "2020-01-01T00:00:00Z", 
        "end": "2020-01-31T23:59:59Z"
      }
    }
  }'
"""
