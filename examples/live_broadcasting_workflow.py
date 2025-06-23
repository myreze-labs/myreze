#!/usr/bin/env python
"""
Live Weather Broadcasting Workflow Example

This example demonstrates the complete workflow from raw weather data
to broadcast-ready visualization assets for virtual studios using
MyrezeDataPackage with multi-agent context and high-quality rendering.

Workflow stages:
1. Data ingestion from multiple sources
2. MyrezeDataPackage creation with semantic context
3. Multi-agent analysis and expert opinions
4. High-quality visualization generation
5. Broadcast-ready asset export
"""

import numpy as np
import json
from datetime import datetime
from myreze.data import (
    MyrezeDataPackage,
    Time,
    SemanticContext,
    VisualSummary,
    MultiResolutionData,
)


def simulate_real_time_weather_data():
    """Simulate incoming real-time weather data from multiple sources."""
    print("🛰️  Ingesting Real-time Weather Data")
    print("=" * 50)

    # Simulate hurricane data approaching Florida coast
    grid_size = 200

    # Create realistic hurricane wind field
    center_x, center_y = 100, 120
    y, x = np.ogrid[:grid_size, :grid_size]

    # Distance from hurricane center
    distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    # Hurricane wind profile (Holland model simplified)
    max_wind = 145  # Category 4 hurricane
    radius_max_wind = 25

    # Wind speed calculation
    wind_speed = np.zeros_like(distance)
    mask = distance > 0
    wind_speed[mask] = max_wind * np.exp(-((distance[mask] / radius_max_wind) ** 0.6))

    # Add some noise for realism
    wind_speed += np.random.normal(0, 5, wind_speed.shape)
    wind_speed = np.clip(wind_speed, 0, 200)

    # Create wind direction (tangential flow)
    wind_direction = np.arctan2(y - center_y, x - center_x) + np.pi / 2
    wind_u = wind_speed * np.cos(wind_direction)
    wind_v = wind_speed * np.sin(wind_direction)

    # Geographic bounds (Florida coast)
    bounds = [-82.0, 24.0, -79.0, 27.0]  # West FL to East FL

    data = {
        "wind_speed": wind_speed,
        "wind_u": wind_u,
        "wind_v": wind_v,
        "bounds": bounds,
        "resolution": 0.015,  # degrees per pixel
        "units": "mph",
        "data_source": "HURDAT2_real_time",
        "measurement_height": "10m",
        "quality_flag": "high_confidence",
    }

    print(f"✅ Data ingested: {grid_size}x{grid_size} wind field")
    print(f"🌪️  Max wind speed: {wind_speed.max():.1f} mph")
    print(f"📍 Geographic bounds: {bounds}")

    return data


def create_broadcast_ready_package(data):
    """Create a broadcast-ready MyrezeDataPackage with full context."""
    print("\n📦 Creating Broadcast-Ready MyrezeDataPackage")
    print("=" * 50)

    # Create semantic context optimized for broadcasting
    semantic_context = SemanticContext(
        natural_description=(
            "Major Hurricane Ian approaching Florida's west coast with sustained "
            "winds of 145 mph. This Category 4 storm poses extreme danger to life "
            "and property along the coast. Storm surge of 12-16 feet expected."
        ),
        semantic_tags=[
            "hurricane",
            "major_hurricane",
            "category_4",
            "florida",
            "extreme_weather",
            "storm_surge",
            "life_threatening",
            "evacuation_zones",
            "emergency",
        ],
        geographic_context={
            "primary_impact_area": "Southwest Florida",
            "states_affected": ["Florida"],
            "major_cities": ["Fort Myers", "Naples", "Sarasota", "Tampa"],
            "evacuation_zones": ["A", "B", "C"],
            "storm_surge_risk": "extreme",
            "inland_penetration": "significant",
        },
        temporal_context={
            "storm_stage": "approaching",
            "landfall_estimate": "within_6_hours",
            "season": "peak_hurricane_season",
            "time_of_day": "afternoon",
        },
        data_insights={
            "max_wind_speed": float(data["wind_speed"].max()),
            "storm_category": "4",
            "storm_motion": "northeast_15mph",
            "pressure_estimate": "947_mb",
            "wind_field_size": "large",
        },
    )

    # Create visual summary for multimodal AI
    visual_summary = VisualSummary(
        color_palette=[
            "#000080",
            "#0000FF",
            "#00FFFF",
            "#FFFF00",
            "#FF0000",
            "#800080",
        ],
        visual_stats={
            "dominant_pattern": "spiral_circulation",
            "eye_visible": True,
            "eye_diameter": "20_miles",
            "spiral_bands": "well_defined",
            "asymmetry": "slight_northeast",
            "visual_intensity": "extreme",
        },
    )

    # Create multi-resolution data for different uses
    multi_resolution = MultiResolutionData(
        overview={
            "storm_type": "major_hurricane",
            "category": 4,
            "max_winds": 145,
            "location": "approaching_southwest_florida",
            "threat_level": "extreme",
        },
        summary_stats={
            "wind_percentiles": {
                "50th": float(np.percentile(data["wind_speed"], 50)),
                "75th": float(np.percentile(data["wind_speed"], 75)),
                "90th": float(np.percentile(data["wind_speed"], 90)),
                "95th": float(np.percentile(data["wind_speed"], 95)),
            },
            "affected_area_sq_miles": 15000,
            "population_at_risk": 2500000,
        },
        reduced_resolution={
            "wind_speed": data["wind_speed"][::4, ::4].tolist(),  # 1/4 resolution
            "bounds": data["bounds"],
            "description": "Low-res version for overview displays",
        },
        processed_variants={
            "wind_categories": {
                "description": "Saffir-Simpson categories",
                "categories": _categorize_winds(data["wind_speed"]).tolist(),
            },
            "danger_zones": {
                "description": "Risk levels for different areas",
                "zones": _create_danger_zones(data["wind_speed"]).tolist(),
            },
        },
    )

    # Create the main package
    package = MyrezeDataPackage(
        id=f"hurricane-ian-{datetime.now().strftime('%Y%m%d-%H%M')}",
        data=data,
        time=Time.timestamp(datetime.now().isoformat()),
        visualization_type="vector_field",
        semantic_context=semantic_context,
        visual_summary=visual_summary,
        multi_resolution_data=multi_resolution,
        metadata={
            "broadcast_priority": "URGENT",
            "emergency_level": "EXTREME",
            "update_frequency": "15_minutes",
            "data_latency": "5_minutes",
            "quality_score": 0.96,
            "model_run": "GFS_06Z",
            "confidence": "high",
            "broadcast_graphics": {
                "primary_colormap": "wind_speed_categorical",
                "animation_speed": "medium",
                "camera_preset": "southeast_florida_overview",
            },
        },
    )

    print(f"✅ Package created: {package.id}")
    print(f"📊 Data type: {package.visualization_type}")
    print(f"🎯 Broadcast priority: {package.metadata['broadcast_priority']}")

    return package


def add_multi_agent_analysis(package):
    """Add expert analysis from multiple specialized agents."""
    print("\n🤖 Multi-Agent Analysis & Expert Opinions")
    print("=" * 50)

    # National Hurricane Center Expert
    package.add_agent_context(
        content=(
            "URGENT: Hurricane Ian has strengthened to a dangerous Category 4 storm "
            "with maximum sustained winds of 145 mph. The storm is expected to bring "
            "catastrophic storm surge of 12-16 feet to the Fort Myers area. This is "
            "a life-threatening situation - all residents in evacuation zones should "
            "have completed evacuations by now."
        ),
        agent_id="nhc_hurricane_specialist_v2024",
        context_type="expert_opinion",
        agent_type="expert_system",
        annotation_type="official_warning",
        confidence=1.0,
        metadata={
            "agency": "National Hurricane Center",
            "warning_type": "hurricane_warning",
            "advisory_number": "11A",
            "forecaster": "NHC_Miami",
        },
    )

    # Emergency Management Assessment
    package.add_agent_context(
        content=(
            "EMERGENCY MANAGEMENT ALERT: Based on current track and intensity, "
            "recommend immediate activation of all emergency response protocols. "
            "Storm surge evacuation zones A, B, and C should be completely cleared. "
            "Post-storm rescue operations will be extremely dangerous and may be "
            "delayed 24-48 hours after passage."
        ),
        agent_id="florida_emergency_management",
        context_type="expert_opinion",
        agent_type="expert_system",
        annotation_type="emergency_response",
        confidence=0.98,
        metadata={
            "agency": "Florida Emergency Management",
            "response_level": "LEVEL_1_ACTIVATION",
            "resource_status": "full_deployment",
        },
    )

    # Storm Surge Expert Analysis
    package.add_agent_context(
        content=(
            "STORM SURGE ANALYSIS: The combination of Ian's intensity, size, and "
            "approach angle creates a worst-case scenario for SW Florida. SLOSH "
            "modeling indicates 12-16 foot surge heights with inland penetration "
            "up to 10 miles. Areas below 20 feet elevation face inundation risk."
        ),
        agent_id="storm_surge_specialist_noaa",
        context_type="analysis",
        agent_type="expert_system",
        annotation_type="storm_surge_analysis",
        confidence=0.94,
        metadata={
            "model": "SLOSH_2024",
            "surge_category": "extreme",
            "inland_penetration": "10_miles",
        },
    )

    # Broadcast Meteorologist Context
    package.add_agent_context(
        content=(
            "BROADCAST CONTEXT: This is the most dangerous hurricane to threaten "
            "Southwest Florida since Hurricane Charley in 2004. Key visual elements "
            "for broadcast: emphasize the tight wind field, well-defined eye, and "
            "the catastrophic storm surge threat. Use red/purple colors to convey "
            "the extreme danger level."
        ),
        agent_id="chief_meteorologist_broadcast",
        context_type="expert_opinion",
        agent_type="human_expert",
        annotation_type="broadcast_guidance",
        confidence=0.96,
        metadata={
            "broadcast_station": "local_affiliate",
            "experience_years": 25,
            "specialization": "hurricane_broadcasting",
        },
    )

    # Statistical Analysis
    package.add_agent_context(
        content=(
            f"STATISTICAL ANALYSIS: Current wind field shows maximum winds of "
            f"{package.data['wind_speed'].max():.0f} mph, placing this storm in "
            f"the 99.8th percentile of all Atlantic hurricanes since 1851. The "
            f"rapid intensification rate over the past 24 hours (40 mph increase) "
            f"occurs in less than 5% of all hurricanes."
        ),
        agent_id="hurricane_statistics_engine",
        context_type="analysis",
        agent_type="llm_agent",
        annotation_type="statistical_analysis",
        confidence=0.92,
    )

    print("✅ Added National Hurricane Center official warning")
    print("✅ Added Emergency Management assessment")
    print("✅ Added Storm Surge specialist analysis")
    print("✅ Added Broadcast meteorologist guidance")
    print("✅ Added Statistical analysis")

    # Show accumulated context
    context_summary = package.get_agent_context_summary()
    print(f"\n📊 Total expert inputs: {context_summary['total_annotations']}")
    print(
        f"🎯 Confidence levels: {[f'{op.confidence:.2f}' for op in package.get_expert_opinions()]}"
    )


def generate_broadcast_visualizations(package):
    """Generate broadcast-ready visualizations for different platforms."""
    print("\n🎬 Generating Broadcast Visualizations")
    print("=" * 50)

    # Unreal Engine - Virtual Studio Integration
    print("🎮 Unreal Engine Virtual Studio:")
    unreal_config = {
        "quality": "broadcast",
        "resolution": "4K",
        "framerate": 60,
        "real_time": True,
        "effects": {
            "particle_rain": True,
            "wind_animation": True,
            "storm_surge_simulation": True,
            "lightning_effects": True,
        },
        "camera": {
            "preset": "southeast_florida_overview",
            "tracking": True,
            "smooth_transitions": True,
        },
        "virtual_studio": {
            "green_screen_ready": True,
            "ar_markers": True,
            "interactive_zones": ["storm_center", "landfall_point", "surge_areas"],
        },
    }

    # Simulate Unreal output (would be actual rendering)
    print(f"   ✅ 4K/60fps real-time rendering configured")
    print(f"   ✅ Storm surge simulation enabled")
    print(
        f"   ✅ Interactive zones: {len(unreal_config['virtual_studio']['interactive_zones'])}"
    )
    print(f"   ✅ Green screen integration ready")

    # Three.js - Web Analysis Platform
    print("\n🌐 Three.js Web Analysis:")
    threejs_config = {
        "interactive": True,
        "real_time_updates": True,
        "analysis_tools": True,
        "mobile_optimized": True,
        "features": {
            "zoom_pan": True,
            "time_scrubbing": True,
            "data_probing": True,
            "measurement_tools": True,
        },
    }

    print(f"   ✅ Interactive 3D visualization")
    print(f"   ✅ Real-time data updates")
    print(f"   ✅ Analysis tools enabled")
    print(f"   ✅ Mobile compatibility")

    # High-resolution Static Export
    print("\n📸 High-Resolution Export:")
    export_config = {
        "resolution": "8K",
        "formats": ["PNG", "SVG", "PDF"],
        "colormaps": ["hurricane_winds", "viridis", "custom_broadcast"],
        "annotations": True,
        "print_ready": True,
    }

    print(f"   ✅ 8K resolution export")
    print(f"   ✅ Multiple format support")
    print(f"   ✅ Broadcast-optimized colormaps")
    print(f"   ✅ Print-ready quality")

    return {"unreal": unreal_config, "threejs": threejs_config, "export": export_config}


def demonstrate_live_broadcasting_integration(package, viz_configs):
    """Demonstrate live broadcasting integration capabilities."""
    print("\n📺 Live Broadcasting Integration")
    print("=" * 50)

    # Virtual Studio Setup
    studio_config = {
        "primary_display": {
            "source": "unreal_engine",
            "resolution": "4K_HDR",
            "refresh_rate": "60Hz",
            "color_space": "Rec.2020",
        },
        "secondary_displays": {
            "analyst_screen": "threejs_interactive",
            "teleprompter": "text_overlay",
            "producer_monitor": "technical_readouts",
        },
        "audio_integration": {
            "wind_sound_effects": True,
            "narration_triggers": True,
            "emergency_alerts": True,
        },
        "interactivity": {
            "touch_screen_controls": True,
            "gesture_recognition": True,
            "voice_commands": True,
            "preset_camera_moves": [
                "zoom_to_eye",
                "track_to_landfall",
                "surge_overview",
            ],
        },
    }

    print("🎭 Virtual Studio Configuration:")
    print(f"   ✅ Primary display: {studio_config['primary_display']['resolution']}")
    print(f"   ✅ Real-time updates: Every 15 minutes")
    print(f"   ✅ Interactive controls: Touch + Voice + Gesture")
    print(f"   ✅ Audio integration: Wind effects + Emergency alerts")

    # Live Data Integration
    print("\n📊 Live Data Integration:")
    print(f"   ✅ Data latency: 5 minutes from observation")
    print(f"   ✅ Update frequency: 15 minutes")
    print(f"   ✅ Quality monitoring: Real-time")
    print(f"   ✅ Backup data sources: 3 redundant feeds")

    # Broadcasting Outputs
    print("\n📡 Broadcasting Outputs:")
    outputs = {
        "live_tv": "4K HDR main broadcast feed",
        "streaming": "Adaptive bitrate for online platforms",
        "social_media": "Optimized clips for social sharing",
        "mobile_app": "Interactive viewer experience",
        "emergency_alerts": "Automated warning distribution",
    }

    for platform, description in outputs.items():
        print(f"   ✅ {platform.replace('_', ' ').title()}: {description}")

    return studio_config


def show_package_summary(package):
    """Display comprehensive package summary for technical review."""
    print("\n📋 Broadcast Package Summary")
    print("=" * 50)

    # Enhanced LLM summary with all context
    llm_summary = package.get_llm_summary()

    print(f"📦 Package ID: {llm_summary['package_id']}")
    print(f"🎯 Visualization Type: {llm_summary['visualization_type']}")
    print(f"⏰ Timestamp: {llm_summary['time_info']['value']}")

    # Agent context summary
    if "agent_context" in llm_summary:
        agent_info = llm_summary["agent_context"]
        print(f"\n🤖 Expert Analysis:")
        print(f"   • Total expert inputs: {agent_info['total_annotations']}")
        print(f"   • Contributing agents: {agent_info['unique_agents']}")
        print(f"   • Context types: {', '.join(agent_info['context_types'])}")

    # Context narrative for broadcast team
    narrative = package.get_context_narrative()
    print(f"\n📖 Expert Context Summary:")
    print(f"   {narrative[:200]}...")

    # Technical specifications
    print(f"\n⚙️  Technical Specifications:")
    print(
        f"   • Data resolution: {package.data.get('resolution', 'N/A')} degrees/pixel"
    )
    print(f"   • Geographic coverage: {package.data['bounds']}")
    print(f"   • Quality score: {package.metadata.get('quality_score', 'N/A')}")
    print(f"   • Update frequency: {package.metadata.get('update_frequency', 'N/A')}")
    print(
        f"   • Broadcast priority: {package.metadata.get('broadcast_priority', 'N/A')}"
    )


def _categorize_winds(wind_speed):
    """Categorize winds by Saffir-Simpson scale."""
    categories = np.zeros_like(wind_speed)
    categories[(wind_speed >= 39) & (wind_speed < 74)] = 1  # Tropical Storm
    categories[(wind_speed >= 74) & (wind_speed < 96)] = 2  # Cat 1
    categories[(wind_speed >= 96) & (wind_speed < 111)] = 3  # Cat 2
    categories[(wind_speed >= 111) & (wind_speed < 130)] = 4  # Cat 3
    categories[(wind_speed >= 130) & (wind_speed < 157)] = 5  # Cat 4
    categories[wind_speed >= 157] = 6  # Cat 5
    return categories


def _create_danger_zones(wind_speed):
    """Create danger zone classification."""
    zones = np.zeros_like(wind_speed)
    zones[(wind_speed >= 39) & (wind_speed < 96)] = 1  # Moderate danger
    zones[(wind_speed >= 96) & (wind_speed < 130)] = 2  # High danger
    zones[wind_speed >= 130] = 3  # Extreme danger
    return zones


def main():
    """Run the complete live broadcasting workflow demonstration."""
    print("🚀 Live Weather Broadcasting Workflow")
    print("=" * 70)
    print("From Real-time Data to Broadcast-Ready Virtual Studio Assets")
    print("=" * 70)

    # Stage 1: Data ingestion
    weather_data = simulate_real_time_weather_data()

    # Stage 2: Create broadcast package
    package = create_broadcast_ready_package(weather_data)

    # Stage 3: Multi-agent analysis
    add_multi_agent_analysis(package)

    # Stage 4: Generate visualizations
    viz_configs = generate_broadcast_visualizations(package)

    # Stage 5: Broadcasting integration
    studio_config = demonstrate_live_broadcasting_integration(package, viz_configs)

    # Final summary
    show_package_summary(package)

    print("\n✨ Workflow Complete!")
    print("📺 Broadcast-ready package with expert analysis delivered")
    print("🎬 Virtual studio integration configured")
    print("🌪️ Hurricane Ian coverage ready for live broadcasting")


if __name__ == "__main__":
    main()
