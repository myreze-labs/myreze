# Multi-Agent Context System Guide

This guide explains how MyrezeDataPackage handles cumulative context from multiple LLM agents, addressing the need for expert opinions, analysis results, and contextual insights to accumulate as packages move through different systems.

## Overview

The Multi-Agent Context System provides:

- **Attribution Tracking**: Know which agent added what context
- **Audit Trails**: Full timestamp and metadata tracking
- **Structured Expert Opinions**: Organized by type and confidence
- **Context Accumulation**: Multiple agents can add context without conflicts
- **Narrative Generation**: Automatic summaries of all accumulated context

## Problem Solved

Previously, adding context like "A weather forecasting expert report regarding this data states that..." required manual management in metadata or description fields without proper attribution or structure.

Now you can:
```python
# Add expert opinion with full attribution
package.add_agent_context(
    "The intensity of this wind is record high for this region",
    agent_id="weather_forecasting_expert_v2.1",
    context_type="expert_opinion", 
    confidence=0.95
)

# Get narrative summary of all accumulated context
narrative = package.get_context_narrative()
# Output: "Expert opinions:
#         • weather_forecasting_expert_v2.1: The intensity of this wind is record high..."
```

## Core Components

### AgentAnnotation
Individual piece of context from a specific agent:

```python
from myreze.data import AgentAnnotation

annotation = AgentAnnotation(
    content="This temperature pattern shows extreme heat dome conditions",
    agent_id="climate_expert_v3", 
    agent_type="expert_system",
    annotation_type="expert_opinion",
    confidence=0.92,
    metadata={
        "specialization": "extreme_weather",
        "model_version": "3.0"
    }
)
```

### AgentContextChain  
Chain of related annotations by type:

```python
from myreze.data import AgentContextChain

chain = AgentContextChain(context_type="expert_opinion")
chain.add_annotation(
    "Record-breaking heat intensity detected",
    agent_id="weather_expert",
    confidence=0.95
)
```

### MultiAgentContext
Complete context management for a package:

```python
from myreze.data import MultiAgentContext

context = MultiAgentContext(package_id="weather-data-123")
context.add_context(
    "Statistical analysis shows 3.8 sigma deviation from normal",
    agent_id="statistical_engine",
    context_type="analysis"
)
```

## Usage Patterns

### 1. Simple Expert Opinion

```python
from myreze.data import MyrezeDataPackage, add_expert_opinion

# Create or receive a data package
package = MyrezeDataPackage(...)

# Add expert opinion
add_expert_opinion(
    package,
    "A weather forecasting expert report regarding this data states that: This represents a once-in-decade storm system with unprecedented wind patterns",
    expert_id="weather_forecasting_expert_noaa",
    confidence=0.93
)
```

### 2. Multiple Agent Analysis

```python
# Multiple agents add different types of context
package.add_agent_context(
    "Historical analysis indicates this is a 200-year flood event",
    agent_id="hydrological_expert",
    context_type="expert_opinion",
    annotation_type="historical_analysis"
)

package.add_agent_context(
    "Emergency response protocols level 5 should be activated immediately", 
    agent_id="emergency_management_ai",
    context_type="expert_opinion",
    annotation_type="emergency_response"
)

package.add_agent_context(
    "Mean flow rate: 2,340 m³/s (σ=4.2 above historical mean)",
    agent_id="statistical_analysis_engine", 
    context_type="analysis",
    annotation_type="statistical_summary"
)
```

### 3. Package Handoff Workflow

```python
# Data collector adds initial context
package.add_agent_context(
    "Initial data validation complete, all sensors operational",
    agent_id="data_collection_service",
    context_type="validation"
)

# Package moves to weather analysis service
package.add_agent_context(
    "Meteorological analysis: Exceptional atmospheric river event detected",
    agent_id="weather_analysis_service", 
    context_type="analysis"
)

# Package moves to emergency management
package.add_agent_context(
    "ALERT: Evacuation recommended for zones A-C due to flood risk",
    agent_id="emergency_alert_system",
    context_type="expert_opinion",
    confidence=1.0
)

# Get complete context history
summary = package.get_agent_context_summary()
print(f"Package analyzed by {summary['unique_agents']} different agents")
```

## Context Retrieval Methods

### Get All Context as Narrative

```python
narrative = package.get_context_narrative()
print(narrative)
# Output:
# Expert opinions:
# • weather_expert: Record-breaking heat intensity detected
# • emergency_system: Evacuation protocols should be activated
# Analysis: Statistical variance shows 3.8 sigma deviation
```

### Get Expert Opinions Only

```python
expert_opinions = package.get_expert_opinions()
for opinion in expert_opinions:
    print(f"{opinion.agent_id}: {opinion.content}")
    print(f"Confidence: {opinion.confidence}")
    print(f"Timestamp: {opinion.timestamp}")
```

### Get Context Summary

```python
summary = package.get_agent_context_summary()
print(f"Total annotations: {summary['total_annotations']}")
print(f"Unique agents: {summary['unique_agents']}")  
print(f"Context types: {summary['context_types']}")
print(f"Expert opinions: {len(summary.get('expert_opinions', []))}")
```

### Enhanced LLM Summary

```python
llm_summary = package.get_llm_summary()

# Now includes agent context
if 'agent_context' in llm_summary:
    agent_info = llm_summary['agent_context']
    print(f"Agents contributed: {agent_info['unique_agents']}")
    print(f"Context narrative: {llm_summary['context_narrative']}")
```

## Advanced Features

### Context Types

Organize context by purpose:
- `"expert_opinion"` - Expert analysis and opinions
- `"analysis"` - Statistical and technical analysis  
- `"validation"` - Data quality and validation notes
- `"emergency_response"` - Emergency management context
- `"research"` - Research insights and notes
- `"historical"` - Historical context and comparisons

### Annotation Types

Specific types within context categories:
- `"expert_opinion"`, `"health_assessment"`, `"emergency_response"`
- `"statistical_summary"`, `"historical_analysis"`, `"meteorological_analysis"`
- `"quality_check"`, `"data_validation"`

### Confidence Scores

Track confidence in annotations:
```python
package.add_agent_context(
    "Preliminary analysis suggests possible data anomaly",
    agent_id="anomaly_detector",
    confidence=0.65  # Lower confidence for preliminary findings
)

package.add_agent_context(
    "Confirmed: This is a genuine extreme weather event",
    agent_id="expert_validator", 
    confidence=0.98  # High confidence after validation
)
```

### Metadata and References

Add rich metadata to annotations:
```python
package.add_agent_context(
    "Wind speeds exceed design specifications for infrastructure",
    agent_id="structural_engineering_ai",
    metadata={
        "engineering_standard": "ASCE-7",
        "wind_speed_threshold": "120_mph",
        "infrastructure_type": "bridges_buildings"
    },
    references=["annotation_id_123", "external_report_456"]
)
```

## Backwards Compatibility

The multi-agent context system is fully backwards compatible:

```python
# Legacy packages work unchanged
legacy_package = MyrezeDataPackage(id="old", data={}, time=Time.now())

# Can add context to legacy packages
legacy_package.add_agent_context("New analysis", agent_id="new_agent")

# Serialization supports both formats
full_json = package.to_json(include_enhanced_features=True)  # With context
legacy_json = package.to_json(include_enhanced_features=False)  # Without context
```

## Best Practices

### 1. Use Descriptive Agent IDs
```python
# Good
agent_id="weather_forecasting_expert_v2.1_noaa"
agent_id="statistical_analysis_engine_scipy"

# Avoid  
agent_id="agent1"
agent_id="system"
```

### 2. Include Confidence Scores
```python
# For uncertain analysis
confidence=0.65

# For validated expert opinions  
confidence=0.95

# For automated confirmations
confidence=1.0
```

### 3. Use Appropriate Context Types
```python
# Expert analysis
context_type="expert_opinion"

# Technical analysis
context_type="analysis" 

# Data validation
context_type="validation"

# Emergency management
context_type="emergency_response"
```

### 4. Add Meaningful Metadata
```python
metadata={
    "model_version": "3.1.2",
    "data_sources": ["satellite", "ground_stations"],
    "analysis_method": "machine_learning",
    "quality_score": 0.94
}
```

## JSON Serialization

Agent context is preserved in JSON:

```python
# Full serialization with agent context
json_str = package.to_json(include_enhanced_features=True)

# Reconstruct with all context preserved
reconstructed = MyrezeDataPackage.from_json(json_str)

# All agent context is preserved
assert len(reconstructed.get_expert_opinions()) == len(package.get_expert_opinions())
```

## Integration with Existing Features

### Works with Semantic Context
```python
package = MyrezeDataPackage(
    id="enhanced-data",
    data=data,
    time=time,
    semantic_context=SemanticContext(
        natural_description="Base temperature data for NYC",
        semantic_tags=["weather", "temperature"]
    )
)

# Add agent context on top of semantic context
package.add_agent_context(
    "Expert analysis confirms this is an extreme heat event",
    agent_id="heat_expert"
)

# LLM summary includes both semantic and agent context
summary = package.get_llm_summary()
# Contains both semantic_context and agent_context sections
```

### Works with Visual Summaries
```python
# Visual and agent context work together
if package.visual_summary:
    package.add_agent_context(
        f"Visual analysis of thermal signature confirms heat dome pattern with color saturation indicating {max_temp}°C peaks",
        agent_id="visual_analysis_engine",
        context_type="analysis",
        annotation_type="visual_analysis"
    )
```

This multi-agent context system transforms MyrezeDataPackage from a static data container into a collaborative platform where multiple LLM agents can contribute their expertise with full attribution and audit trails. 