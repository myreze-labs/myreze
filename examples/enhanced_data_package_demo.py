#!/usr/bin/env python
"""
Enhanced MyrezeDataPackage Demonstration for LLM Agents

This example showcases the new multimodal LLM and MCP/RAG integration features
of MyrezeDataPackage, demonstrating how LLM-based agents can create, process,
and understand geospatial data packages with rich semantic context.

Features demonstrated:
1. Visual representations for multimodal LLMs
2. Semantic context and natural language descriptions
3. Multi-resolution data support
4. MCP/RAG integration metadata
5. Auto-generation of contextual information
6. Platform-agnostic serialization
"""

import numpy as np
import json
from myreze.data import MyrezeDataPackage, Time
from myreze.data.core import (
    VisualSummary,
    SemanticContext,
    MultiResolutionData,
    SEMANTIC_CATEGORIES,
)


def create_enhanced_weather_package():
    """
    Create an enhanced weather data package with full LLM/multimodal support.

    This demonstrates creating a data package with semantic context,
    visual summaries, and multi-resolution data for comprehensive
    LLM understanding and processing.
    """
    print("🌡️  Creating Enhanced Weather Data Package")
    print("=" * 50)

    # Generate realistic temperature data for NYC area
    np.random.seed(42)  # For reproducible results
    grid_size = 100

    # Create temperature grid with realistic patterns
    base_temp = 22  # Base temperature in Celsius
    temp_grid = np.random.normal(base_temp, 3, (grid_size, grid_size))

    # Add urban heat island effect (warmer in center)
    center = grid_size // 2
    y, x = np.ogrid[:grid_size, :grid_size]
    distance_from_center = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    heat_island = 5 * np.exp(-distance_from_center / 20)
    temp_grid += heat_island

    # Add some cooling near "water" (edges)
    edge_cooling = np.zeros_like(temp_grid)
    edge_cooling[:5, :] = -2  # North edge
    edge_cooling[-5:, :] = -2  # South edge
    edge_cooling[:, :5] = -3  # West edge (ocean)
    temp_grid += edge_cooling

    # Core data structure
    data = {
        "grid": temp_grid,
        "bounds": [-74.1, 40.6, -73.9, 40.9],  # NYC area
        "resolution": 0.002,  # degrees per pixel
        "units": "celsius",
        "values_range": [float(temp_grid.min()), float(temp_grid.max())],
        "data_source": "synthetic_urban_weather_model",
    }

    # Create comprehensive semantic context
    semantic_context = SemanticContext(
        natural_description=(
            "This temperature map shows the urban heat distribution across "
            "New York City area on a summer afternoon. The data reveals the "
            "classic urban heat island effect with warmer temperatures in "
            "the city center and cooler areas near water bodies. Temperature "
            f"values range from {temp_grid.min():.1f}°C to {temp_grid.max():.1f}°C."
        ),
        semantic_tags=[
            "weather",
            "temperature",
            "urban",
            "atmospheric",
            "environmental",
            "heat_island",
            "climate",
            "new_york",
            "metropolitan",
        ],
        geographic_context={
            "city": "New York City",
            "state": "New York",
            "country": "United States",
            "region": "Northeastern United States",
            "administrative_level": "metropolitan_area",
            "population_density": "high",
            "climate_zone": "humid_subtropical",
            "coastal": True,
            "major_water_bodies": ["Hudson River", "East River", "New York Harbor"],
        },
        temporal_context={
            "season": "summer",
            "time_of_day": "afternoon",
            "typical_conditions": "warm urban environment",
            "heat_island_active": True,
        },
        data_insights={
            "temperature_mean": float(temp_grid.mean()),
            "temperature_std": float(temp_grid.std()),
            "heat_island_intensity": float(heat_island.max()),
            "spatial_correlation": "strong urban heat island pattern",
            "data_quality": "synthetic but realistic",
            "grid_resolution": f"{grid_size}x{grid_size}",
            "area_coverage_km2": "approximately 20x30 km",
        },
        relationships=[
            {
                "type": "temporal_sequence",
                "description": "Part of hourly temperature series",
                "related_packages": ["nyc-temp-13:00", "nyc-temp-15:00"],
            },
            {
                "type": "spatial_context",
                "description": "Urban heat analysis series",
                "related_packages": ["nyc-humidity-14:30", "nyc-wind-14:30"],
            },
        ],
        search_keywords=[
            "NYC temperature",
            "urban heat island",
            "summer weather",
            "metropolitan climate",
            "thermal mapping",
            "city heat",
            "environmental monitoring",
            "weather analysis",
        ],
    )

    # Create multi-resolution data for different processing needs
    multi_resolution = MultiResolutionData(
        overview={
            "data_type": "temperature_grid",
            "spatial_extent": "NYC metropolitan area",
            "temporal_point": "2023-07-15T14:30:00Z",
            "primary_pattern": "urban heat island",
            "key_statistics": {
                "min_temp": float(temp_grid.min()),
                "max_temp": float(temp_grid.max()),
                "mean_temp": float(temp_grid.mean()),
                "temp_range": float(temp_grid.max() - temp_grid.min()),
            },
        },
        summary_stats={
            "percentiles": {
                "p10": float(np.percentile(temp_grid, 10)),
                "p25": float(np.percentile(temp_grid, 25)),
                "p50": float(np.percentile(temp_grid, 50)),
                "p75": float(np.percentile(temp_grid, 75)),
                "p90": float(np.percentile(temp_grid, 90)),
            },
            "spatial_stats": {
                "center_temp": float(temp_grid[center, center]),
                "edge_temp_avg": float(
                    np.mean(
                        [
                            temp_grid[0, :].mean(),
                            temp_grid[-1, :].mean(),
                            temp_grid[:, 0].mean(),
                            temp_grid[:, -1].mean(),
                        ]
                    )
                ),
                "gradient_magnitude": float(np.mean(np.gradient(temp_grid))),
            },
        },
        reduced_resolution={
            "grid": temp_grid[::4, ::4].tolist(),  # 25x25 downsampled
            "bounds": data["bounds"],
            "resolution": 0.008,  # 4x lower resolution
            "purpose": "quick_overview",
        },
        full_resolution={
            "grid": temp_grid.tolist(),
            "bounds": data["bounds"],
            "resolution": 0.002,
            "purpose": "detailed_analysis",
        },
        processed_variants={
            "normalized": {
                "grid": (
                    (temp_grid - temp_grid.min()) / (temp_grid.max() - temp_grid.min())
                ).tolist(),
                "description": "Values normalized to 0-1 range",
            },
            "anomaly": {
                "grid": (temp_grid - temp_grid.mean()).tolist(),
                "description": "Temperature anomaly from mean",
            },
        },
    )

    # Create visual summary (would normally include actual thumbnails)
    visual_summary = VisualSummary(
        visual_hash="a1b2c3d4e5f6",  # Would be computed from actual visual
        color_palette=["#440154", "#31688e", "#35b779", "#fde725"],  # Viridis
        visual_stats={
            "dominant_colors": ["blue", "green", "yellow", "purple"],
            "contrast_level": "high",
            "pattern_type": "radial_gradient",
            "visual_complexity": "medium",
            "readability": "high",
        },
    )

    # Create the enhanced data package
    package = MyrezeDataPackage(
        id="nyc-enhanced-temperature-14:30",
        data=data,
        time=Time.timestamp("2023-07-15T14:30:00Z"),
        visualization_type="heatmap",
        metadata={
            "data_source": "Enhanced Urban Weather Model v2.1",
            "model_resolution": "2m spatial, 1min temporal",
            "quality_score": 0.95,
            "processing_date": "2023-07-15T16:00:00Z",
            "colormap": "viridis",
            "opacity": 0.8,
            "creator": "LLM Agent Weather System",
            "license": "CC-BY-4.0",
        },
        semantic_context=semantic_context,
        visual_summary=visual_summary,
        multi_resolution_data=multi_resolution,
    )

    print(f"✅ Created enhanced package: {package.id}")
    print(f"📊 Data shape: {temp_grid.shape}")
    print(f"🌡️  Temperature range: {temp_grid.min():.1f}°C to {temp_grid.max():.1f}°C")
    print(f"🏷️  Semantic tags: {semantic_context.semantic_tags[:5]}...")
    print(f"🔍 Search keywords: {len(semantic_context.search_keywords)} keywords")

    return package


def demonstrate_llm_friendly_features(package):
    """
    Demonstrate how LLM agents can extract and use information from
    enhanced data packages.
    """
    print("\n🤖 LLM-Friendly Features Demonstration")
    print("=" * 50)

    # 1. Get LLM-optimized summary
    llm_summary = package.get_llm_summary()
    print("📋 LLM Summary Structure:")
    for key in llm_summary.keys():
        print(f"   • {key}")

    # 2. Natural language description
    if package.semantic_context:
        print(f"\n💬 Natural Description:")
        print(f"   {package.semantic_context.natural_description}")

    # 3. Semantic tags for categorization
    print(f"\n🏷️  Semantic Categories:")
    if package.semantic_context:
        for tag in package.semantic_context.semantic_tags[:8]:
            print(f"   • {tag}")

    # 4. Geographic context for spatial understanding
    print(f"\n🌍 Geographic Context:")
    if package.semantic_context and package.semantic_context.geographic_context:
        geo_context = package.semantic_context.geographic_context
        for key, value in list(geo_context.items())[:6]:
            print(f"   • {key}: {value}")

    # 5. Data insights for automated analysis
    print(f"\n📊 Automated Data Insights:")
    if package.semantic_context and package.semantic_context.data_insights:
        insights = package.semantic_context.data_insights
        for key, value in list(insights.items())[:6]:
            print(f"   • {key}: {value}")

    # 6. Multi-resolution access
    print(f"\n🔍 Multi-Resolution Data Available:")
    if package.multi_resolution_data:
        mr_data = package.multi_resolution_data
        print(f"   • Overview: {bool(mr_data.overview)}")
        print(f"   • Summary Stats: {bool(mr_data.summary_stats)}")
        print(f"   • Reduced Resolution: {bool(mr_data.reduced_resolution)}")
        print(f"   • Processed Variants: {len(mr_data.processed_variants)} variants")

    # 7. Visual information for multimodal LLMs
    print(f"\n🎨 Visual Information:")
    if package.visual_summary:
        vs = package.visual_summary
        print(f"   • Color palette: {vs.color_palette}")
        print(f"   • Visual hash: {vs.visual_hash}")
        print(f"   • Has thumbnail: {vs.thumbnail_png is not None}")


def demonstrate_serialization_formats(package):
    """
    Demonstrate different serialization formats for various use cases.
    """
    print("\n💾 Serialization Formats Demonstration")
    print("=" * 50)

    # 1. Full enhanced format (includes all new features)
    full_json = package.to_json(include_enhanced_features=True)
    print(f"📦 Full Enhanced Format: {len(full_json):,} characters")

    # 2. Legacy compatible format (backwards compatible)
    legacy_json = package.to_json(include_enhanced_features=False)
    print(f"🔄 Legacy Compatible Format: {len(legacy_json):,} characters")

    # 3. LLM-optimized summary
    llm_summary = package.get_llm_summary()
    llm_summary_json = json.dumps(llm_summary)
    print(f"🤖 LLM Summary Format: {len(llm_summary_json):,} characters")

    # 4. Demonstrate round-trip serialization
    restored_package = MyrezeDataPackage.from_json(full_json)
    print(f"✅ Round-trip successful: {restored_package.id == package.id}")

    # 5. Show enhanced features are preserved
    enhanced_preserved = (
        restored_package.semantic_context is not None
        and restored_package.visual_summary is not None
        and restored_package.multi_resolution_data is not None
    )
    print(f"🔧 Enhanced features preserved: {enhanced_preserved}")

    return {
        "full_format_size": len(full_json),
        "legacy_format_size": len(legacy_json),
        "llm_summary_size": len(llm_summary_json),
        "round_trip_successful": restored_package.id == package.id,
        "enhanced_features_preserved": enhanced_preserved,
    }


def demonstrate_mcp_rag_integration(package):
    """
    Demonstrate how the package supports MCP and RAG integration.
    """
    print("\n🔗 MCP/RAG Integration Demonstration")
    print("=" * 50)

    if not package.semantic_context:
        print("❌ No semantic context available")
        return

    sc = package.semantic_context

    # 1. Search and retrieval metadata
    print("🔍 Search & Retrieval Metadata:")
    print(f"   • Search keywords: {len(sc.search_keywords)} keywords")
    print(f"   • Semantic tags: {len(sc.semantic_tags)} tags")
    print(f"   • Natural description length: {len(sc.natural_description)} chars")

    # 2. Relationship mapping
    print(f"\n🕸️  Relationship Mapping:")
    print(f"   • Related packages: {len(sc.relationships)} relationships")
    for rel in sc.relationships:
        print(f"     - {rel['type']}: {rel['description']}")

    # 3. Hierarchical categorization
    print(f"\n📂 Categorization Support:")
    relevant_categories = [
        cat
        for cat in SEMANTIC_CATEGORIES
        if any(tag in cat for tag in sc.semantic_tags)
    ]
    print(f"   • Relevant categories: {relevant_categories[:5]}")

    # 4. Geographic indexing
    print(f"\n🗺️  Geographic Indexing:")
    if sc.geographic_context:
        geo = sc.geographic_context
        if "bounding_box" in geo:
            bbox = geo["bounding_box"]
            print(
                f"   • Bounding box: [{bbox['west']:.2f}, {bbox['south']:.2f}, "
                f"{bbox['east']:.2f}, {bbox['north']:.2f}]"
            )
        if "region" in geo:
            print(f"   • Administrative region: {geo['region']}")

    # 5. Temporal indexing
    print(f"\n⏰ Temporal Indexing:")
    if sc.temporal_context:
        temp_ctx = sc.temporal_context
        for key, value in temp_ctx.items():
            print(f"   • {key}: {value}")


def main():
    """
    Main demonstration function showing enhanced MyrezeDataPackage capabilities.
    """
    print("🚀 Enhanced MyrezeDataPackage Demonstration")
    print("=" * 60)
    print("Showcasing LLM, multimodal AI, and MCP/RAG integration features\n")

    try:
        # Create enhanced data package
        package = create_enhanced_weather_package()

        # Demonstrate LLM-friendly features
        demonstrate_llm_friendly_features(package)

        # Show serialization capabilities
        serialization_results = demonstrate_serialization_formats(package)

        # Demonstrate MCP/RAG integration
        demonstrate_mcp_rag_integration(package)

        # Summary of capabilities
        print("\n🎯 Summary of Enhanced Capabilities")
        print("=" * 50)
        print("✅ Visual representations for multimodal LLMs")
        print("✅ Natural language descriptions and semantic tagging")
        print("✅ Multi-resolution data support")
        print("✅ MCP/RAG integration metadata")
        print("✅ Auto-generation of contextual information")
        print("✅ Platform-agnostic serialization")
        print("✅ Backwards compatibility maintained")

        print(f"\n📊 Size Comparison:")
        print(f"   Full enhanced: {serialization_results['full_format_size']:,} chars")
        print(
            f"   Legacy format: {serialization_results['legacy_format_size']:,} chars"
        )
        print(f"   LLM summary: {serialization_results['llm_summary_size']:,} chars")

        print(f"\n🔧 Key Benefits for LLM Agents:")
        print(f"   • Rich semantic context for understanding data meaning")
        print(f"   • Visual summaries for multimodal AI processing")
        print(f"   • Multi-resolution access for different processing needs")
        print(f"   • Automated generation of descriptions and insights")
        print(f"   • Search and retrieval optimization")
        print(f"   • Relationship mapping for knowledge graphs")

        print(f"\n✨ All demonstrations completed successfully!")

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        raise


if __name__ == "__main__":
    main()
