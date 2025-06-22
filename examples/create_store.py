from myreze.store.product import Product
from myreze.store.provider import ProductProvider
from myreze.store.server import StoreServer
from myreze.data import MyrezeDataPackage, Time
from myreze.viz.threejs.flat_overlay import (
    DummyRenderer,
)
from myreze.viz.threejs.png_renderer import PNGTexture
import numpy as np
from typing import Dict, Any, Optional, List
import uuid
import requests
import io
from PIL import Image


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
            "texture": np.random.randint(0, 255, (100, 100, 4), dtype=np.uint8),
        }
        return MyrezeDataPackage(
            id=f"pkg-{uuid.uuid4()}",
            time=Time.from_dict(temporal_region),
            data=data,
            unreal_visualization=None,
            threejs_visualization=DummyRenderer(),
        )


class TransparentPNGProduct(Product):
    """A product that returns a hardcoded transparent PNG from URL."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use a reliable transparent PNG from a public CDN
        base_url = "https://via.placeholder.com/500x500/FF0000/FFFFFF.png"
        self.png_url = f"{base_url}?text=Myreze+Test"
        # Alternative transparent PNGs you could use:
        # self.png_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/HD_transparent_picture.png/64px-HD_transparent_picture.png"  # noqa
        # self.png_url = "https://dummyimage.com/400x300/000000/ffffff.png&text=Transparent+Test"  # noqa

    async def generate_package(
        self,
        spatial_region: Dict[str, Any],
        temporal_region: Dict[str, Any],
        visualization: Optional[Dict[str, Any]] = None,
    ) -> MyrezeDataPackage:
        # Fetch the PNG from the URL
        try:
            response = requests.get(self.png_url, timeout=10)
            response.raise_for_status()

            # Convert to PIL Image then to numpy array
            image = Image.open(io.BytesIO(response.content))

            # Ensure RGBA format for transparency
            if image.mode != "RGBA":
                image = image.convert("RGBA")

            # Convert to numpy array
            texture_array = np.array(image)

            # Create data package with the fetched PNG
            data = {
                "texture": texture_array,
                "source_url": self.png_url,
                "image_size": texture_array.shape[:2],
                "format": "RGBA",
            }

            return MyrezeDataPackage(
                id=f"pkg-{uuid.uuid4()}",
                time=Time.from_dict(temporal_region),
                data=data,
                unreal_visualization=None,
                threejs_visualization=PNGTexture(),  # Use new PNG renderer
                visualization_type="png_overlay",
                metadata={
                    "description": "Hardcoded transparent PNG test",
                    "source_url": self.png_url,
                    "image_dimensions": (
                        f"{texture_array.shape[1]}x{texture_array.shape[0]}"
                    ),
                    "channels": (
                        texture_array.shape[2] if len(texture_array.shape) > 2 else 1
                    ),
                },
            )

        except Exception as e:
            # Fallback to a generated transparent image if URL fails
            print(f"Failed to fetch PNG from URL: {e}")
            print("Generating fallback transparent image...")

            # Create a simple transparent test pattern
            fallback_image = np.zeros((200, 200, 4), dtype=np.uint8)
            # Add some red squares with transparency
            fallback_image[50:150, 50:150] = [255, 0, 0, 128]  # Red
            fallback_image[25:75, 25:75] = [0, 255, 0, 200]  # Green
            fallback_image[125:175, 125:175] = [0, 0, 255, 150]  # Blue

            data = {
                "texture": fallback_image,
                "source_url": "fallback_generated",
                "image_size": fallback_image.shape[:2],
                "format": "RGBA",
            }

            return MyrezeDataPackage(
                id=f"pkg-{uuid.uuid4()}",
                time=Time.from_dict(temporal_region),
                data=data,
                unreal_visualization=None,
                threejs_visualization=PNGTexture(),
                visualization_type="flat_overlay",
                metadata={
                    "description": "Fallback transparent PNG test pattern",
                    "source_url": "generated",
                    "image_dimensions": (
                        f"{fallback_image.shape[1]}x{fallback_image.shape[0]}"
                    ),
                    "channels": fallback_image.shape[2],
                },
            )


class FlexibleProductProvider(ProductProvider):
    """
    A provider that offers multiple products
    """

    async def get_products(self) -> List[Product]:
        """Return a list of available products with their capabilities."""
        return [
            WeatherProduct(
                product_id="15-day-clouds",
                name="15 Day global cloud forecast",
                description="Blablabla",
                source="Myreze",
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
                visualization_type="flat_overlay",
            ),
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
                visualization_type="flat_overlay",
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
                visualization_type="flat_overlay",
            ),
            TransparentPNGProduct(
                product_id="test-transparent-png",
                name="Test Transparent PNG",
                description=(
                    "A test product that returns a hardcoded transparent "
                    "PNG from an online URL."
                ),
                source="Online PNG URL",
                data_types=["image", "test"],
                spatial_coverage={
                    "type": "BoundingBox",
                    "coordinates": [[-180, -90], [180, 90]],
                },
                temporal_coverage={
                    "type": "Capability",
                    "supports_historical": True,
                    "earliest_date": "2020-01-01T00:00:00Z",
                    "latest_date": "2030-12-31T23:59:59Z",
                    "supports_forecast": False,
                },
                availability={"public": True},
                visualization_type="flat_overlay",
            ),
        ]


# Run the store
if __name__ == "__main__":
    provider = FlexibleProductProvider()
    server = StoreServer(provider)
    server.run()


"""
After starting the store, you can make requests to the store using the
following curl commands:

1. To get a list of available products (metadata only):
curl -X GET http://localhost:8000/products

2. To order a specific product (specifying the exact temporal range at
order time):
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

3. To test the new transparent PNG product:
curl -X POST http://localhost:8000/orders \\
  -H "Content-Type: application/json" \\
  -d '{
    "product_id": "test-transparent-png", 
    "spatial_region": {
      "type": "BoundingBox", 
      "coordinates": [[-10, 35], [25, 60]]
    }, 
    "temporal_region": {
      "type": "Timestamp", 
      "value": "2023-01-01T12:00:00Z"
    }
  }'
"""
