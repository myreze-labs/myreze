#!/usr/bin/env python
"""
Multi-Agent Context Demonstration

This example demonstrates the new multi-agent context system in MyrezeDataPackage,
showing how different LLM agents can add cumulative context with proper attribution,
audit trails, and structured expert opinions.

Features demonstrated:
1. Multiple agents adding different types of context
2. Attribution tracking and timestamps
3. Expert opinions with confidence scores
4. Analysis results from specialized agents
5. Context narrative generation
6. Consensus building across multiple agents
"""

import numpy as np
from myreze.data import MyrezeDataPackage, Time
from myreze.data.core import SemanticContext
from myreze.data.agent_context import add_expert_opinion, add_analysis_result


def create_base_weather_package():
    """Create a base weather data package."""
    print("🌡️  Creating Base Weather Package")
    print("=" * 50)

    # Generate temperature data with extreme heat pattern
    np.random.seed(42)
    temp_grid = np.random.normal(38, 4, (50, 50))  # High temperature base

    # Add extreme heat spots
    center = 25
    y, x = np.ogrid[:50, :50]
    extreme_heat = 8 * np.exp(-((x - center) ** 2 + (y - center) ** 2) / 50)
    temp_grid += extreme_heat

    data = {
        "grid": temp_grid,
        "bounds": [-118.5, 34.0, -118.2, 34.3],  # Los Angeles area
        "units": "celsius",
        "measurement_type": "surface_temperature",
    }

    semantic_context = SemanticContext(
        natural_description="Temperature measurements across Los Angeles showing unusual heat patterns",
        semantic_tags=["weather", "temperature", "urban", "heat_wave"],
        geographic_context={"city": "Los Angeles", "state": "California"},
    )

    package = MyrezeDataPackage(
        id="la-extreme-heat-event",
        data=data,
        time=Time.timestamp("2023-08-15T15:30:00Z"),
        visualization_type="heatmap",
        semantic_context=semantic_context,
        metadata={
            "source": "Urban Weather Monitoring Network",
            "quality": "high",
            "measurement_height": "2m",
        },
    )

    print(f"✅ Created package: {package.id}")
    print(f"🌡️  Max temperature: {temp_grid.max():.1f}°C")
    print(f"📊 Data shape: {temp_grid.shape}")

    return package


def simulate_agent_workflow(package):
    """Simulate multiple agents adding context to the package."""
    print("\n🤖 Multi-Agent Context Addition Workflow")
    print("=" * 50)

    # Agent 1: Weather Forecasting Expert
    print("\n1. Weather Forecasting Expert Analysis")
    package.add_agent_context(
        content="This temperature pattern shows an extreme heat dome event with temperatures reaching 46.2°C, which is 8-10°C above normal for this region and time of year. The spatial pattern indicates urban heat island amplification of the dome effect.",
        agent_id="weather_forecasting_expert_v3.1",
        context_type="expert_opinion",
        agent_type="expert_system",
        annotation_type="expert_opinion",
        confidence=0.92,
        metadata={
            "specialization": "extreme_weather_events",
            "model_version": "3.1",
            "data_sources": ["satellite", "ground_stations", "historical_records"],
        },
    )
    print("   ✅ Added expert weather analysis")

    # Agent 2: Climate Research Agent
    print("\n2. Climate Research Agent Analysis")
    package.add_agent_context(
        content="Historical analysis indicates this is a 1-in-50 year heat event for the Los Angeles basin. The pattern matches climate model projections for extreme heat scenarios, with the highest temperatures concentrated in urbanized areas. This event represents a significant climate anomaly.",
        agent_id="climate_research_agent_v2.0",
        context_type="analysis",
        agent_type="llm_agent",
        annotation_type="historical_analysis",
        confidence=0.88,
        metadata={
            "research_focus": "climate_extremes",
            "historical_data_span": "1950-2023",
            "statistical_method": "extreme_value_analysis",
        },
    )
    print("   ✅ Added climate research analysis")

    # Agent 3: Public Health Agent
    print("\n3. Public Health Impact Agent")
    package.add_agent_context(
        content="HEALTH ALERT: This heat intensity poses severe public health risks. Expected heat index values exceed safe thresholds (>41°C) across 85% of the monitored area. Immediate heat emergency protocols should be activated. Vulnerable populations are at extreme risk.",
        agent_id="public_health_alert_system",
        context_type="expert_opinion",
        agent_type="expert_system",
        annotation_type="health_assessment",
        confidence=0.95,
        metadata={
            "health_agency": "LA_County_Public_Health",
            "alert_level": "extreme",
            "vulnerable_population_risk": "critical",
        },
    )
    print("   ✅ Added public health assessment")

    # Agent 4: Statistical Analysis Agent
    print("\n4. Statistical Analysis Agent")
    add_analysis_result(
        package,
        f"Statistical analysis: Mean temperature {package.data['grid'].mean():.1f}°C, std dev {package.data['grid'].std():.1f}°C. Temperature variance is 3.8 standard deviations above the 30-year normal. 95th percentile reaches {np.percentile(package.data['grid'], 95):.1f}°C. Spatial autocorrelation coefficient: 0.76 (high clustering).",
        agent_id="statistical_analysis_engine",
        analysis_type="statistical_summary",
    )
    print("   ✅ Added statistical analysis")

    # Agent 5: Urban Planning Expert
    print("\n5. Urban Planning Expert Opinion")
    package.add_agent_context(
        content="Urban infrastructure assessment: This heat pattern correlates strongly with building density and lack of green spaces. Areas showing 45°C+ temperatures align with commercial/industrial zones with minimal vegetation. Urgent need for cool corridor implementation and emergency cooling center activation.",
        agent_id="urban_planning_expert",
        context_type="expert_opinion",
        agent_type="human_expert",
        annotation_type="infrastructure_assessment",
        confidence=0.90,
        metadata={
            "expertise": "heat_resilient_design",
            "city_knowledge": "los_angeles",
            "recommendation_priority": "immediate_action",
        },
    )
    print("   ✅ Added urban planning expert opinion")

    return package


def demonstrate_context_retrieval(package):
    """Demonstrate different ways to retrieve and use accumulated context."""
    print("\n📊 Context Retrieval and Analysis")
    print("=" * 50)

    # 1. Get context summary
    print("\n1. Agent Context Summary:")
    summary = package.get_agent_context_summary()
    print(f"   • Total annotations: {summary['total_annotations']}")
    print(f"   • Unique agents: {summary['unique_agents']}")
    print(f"   • Context types: {summary['context_types']}")

    # 2. Get narrative summary
    print("\n2. Context Narrative:")
    narrative = package.get_context_narrative()
    print(f"   {narrative[:200]}...")

    # 3. Get expert opinions specifically
    print("\n3. Expert Opinions:")
    expert_opinions = package.get_expert_opinions()
    for i, opinion in enumerate(expert_opinions[:2], 1):
        print(f"   {i}. {opinion.agent_id} (confidence: {opinion.confidence})")
        print(f"      {opinion.content[:100]}...")

    # 4. Get LLM summary with all context
    print("\n4. Enhanced LLM Summary (with agent context):")
    llm_summary = package.get_llm_summary()
    if "agent_context" in llm_summary:
        agent_summary = llm_summary["agent_context"]
        print(f"   • Total agents contributed: {agent_summary['unique_agents']}")
        print(f"   • Context types: {agent_summary['context_types']}")

    # 5. Demonstrate context chains
    print("\n5. Context Chains Detail:")
    if package.agent_context:
        for context_type, chain in package.agent_context.context_chains.items():
            consensus = chain.get_consensus_view()
            print(f"   • {context_type}: {consensus['total_annotations']} annotations")
            if consensus["by_type"]:
                for ann_type, info in consensus["by_type"].items():
                    print(
                        f"     - {ann_type}: {info['count']} from {len(info['agents'])} agents"
                    )


def demonstrate_json_serialization(package):
    """Demonstrate how agent context is preserved in JSON serialization."""
    print("\n💾 JSON Serialization with Agent Context")
    print("=" * 50)

    # Serialize with full context
    json_str = package.to_json(include_enhanced_features=True)
    print(f"✅ Full JSON size: {len(json_str):,} characters")

    # Serialize without enhanced features (legacy compatible)
    legacy_json = package.to_json(include_enhanced_features=False)
    print(f"📦 Legacy JSON size: {len(legacy_json):,} characters")

    # Reconstruct from JSON
    reconstructed = MyrezeDataPackage.from_json(json_str)
    print(
        f"🔄 Reconstructed package with {reconstructed.get_agent_context_summary()['total_annotations']} annotations"
    )

    return reconstructed


def simulate_package_handoff_workflow():
    """Simulate real-world workflow of package being passed between agents."""
    print("\n🔄 Package Handoff Workflow Simulation")
    print("=" * 50)

    # Create initial package
    package = create_base_weather_package()

    # Agent 1: Data collector adds initial context
    package.add_agent_context(
        "Initial data collection complete. All sensors operational, data quality verified.",
        agent_id="data_collection_service",
        context_type="validation",
        annotation_type="quality_check",
    )

    # Package passed to weather service
    package.add_agent_context(
        "Weather pattern analysis: Exceptional heat dome formation detected. Synoptic conditions favor heat amplification.",
        agent_id="weather_analysis_service",
        context_type="analysis",
        annotation_type="meteorological_analysis",
    )

    # Package passed to emergency management
    package.add_agent_context(
        "EMERGENCY DECLARATION: Extreme heat warning issued. All cooling centers activated. Public safety protocols in effect.",
        agent_id="emergency_management_system",
        context_type="expert_opinion",
        annotation_type="emergency_response",
        confidence=1.0,
    )

    # Package passed to research system
    package.add_agent_context(
        "Research note: This event provides valuable data for heat resilience modeling. Recommending additional sensor deployment for future events.",
        agent_id="climate_research_system",
        context_type="analysis",
        annotation_type="research_insight",
    )

    print(
        f"📦 Package passed through {package.get_agent_context_summary()['unique_agents']} agents"
    )
    print(f"🔍 Final context narrative:\n{package.get_context_narrative()}")

    return package


def main():
    """Run the complete multi-agent context demonstration."""
    print("🚀 Multi-Agent Context System Demonstration")
    print("=" * 70)

    # 1. Create base package
    package = create_base_weather_package()

    # 2. Simulate multiple agents adding context
    package = simulate_agent_workflow(package)

    # 3. Demonstrate context retrieval
    demonstrate_context_retrieval(package)

    # 4. Demonstrate serialization
    reconstructed = demonstrate_json_serialization(package)

    # 5. Simulate package handoff workflow
    print("\n" + "=" * 70)
    handoff_package = simulate_package_handoff_workflow()

    print("\n✨ Demonstration Complete!")
    print(f"📊 Total examples created: 2 packages")
    print(f"🤖 Multi-agent context system ready for production use")


if __name__ == "__main__":
    main()
