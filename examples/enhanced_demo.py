#!/usr/bin/env python
"""
Enhanced MyrezeDataPackage Demo for LLM Agents

This demonstrates the new multimodal LLM and MCP/RAG integration features.
"""

import numpy as np
import json
from myreze.data import MyrezeDataPackage, Time
from myreze.data.core import VisualSummary, SemanticContext, MultiResolutionData


def create_enhanced_package():
    """Create an enhanced weather data package."""
    print("🌡️  Creating Enhanced Weather Package")

    # Generate temperature data
    temp_grid = np.random.normal(22, 3, (50, 50))

    # Create semantic context
    semantic_context = SemanticContext(
        natural_description="Temperature map showing urban heat distribution across NYC",
        semantic_tags=["weather", "temperature", "urban", "environmental"],
        geographic_context={"city": "New York", "region": "Northeast US"},
        data_insights={"mean_temp": float(temp_grid.mean())},
        search_keywords=["NYC temperature", "urban heat", "weather"],
    )

    # Create package
    package = MyrezeDataPackage(
        id="enhanced-nyc-temperature",
        data={
            "grid": temp_grid,
            "bounds": [-74.1, 40.6, -73.9, 40.9],
            "units": "celsius",
        },
        time=Time.timestamp("2023-07-15T14:30:00Z"),
        visualization_type="heatmap",
        semantic_context=semantic_context,
    )

    print(f"✅ Created package: {package.id}")
    return package


def demonstrate_llm_features(package):
    """Demonstrate LLM-friendly features."""
    print("\n🤖 LLM Features:")

    # Get LLM summary
    summary = package.get_llm_summary()
    print(f"📋 Summary keys: {list(summary.keys())}")

    # Show natural description
    if package.semantic_context:
        print(f"💬 Description: {package.semantic_context.natural_description}")
        print(f"🏷️  Tags: {package.semantic_context.semantic_tags}")


def main():
    """Main demonstration."""
    print("🚀 Enhanced MyrezeDataPackage Demo")
    print("=" * 40)

    package = create_enhanced_package()
    demonstrate_llm_features(package)

    # Test serialization
    json_output = package.to_json()
    print(f"\n💾 JSON size: {len(json_output):,} characters")

    # Test round-trip
    restored = MyrezeDataPackage.from_json(json_output)
    print(f"✅ Round-trip successful: {restored.id == package.id}")

    print("\n✨ Demo completed!")


if __name__ == "__main__":
    main()
