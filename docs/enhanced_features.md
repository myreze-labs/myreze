# Enhanced MyrezeDataPackage Features

This document describes the comprehensive enhancements made to the MyrezeDataPackage to optimize it for LLM-based agents, multimodal AI systems, and MCP/RAG integration while maintaining full backwards compatibility.

## Overview of Enhancements

The enhanced MyrezeDataPackage now provides:

1. **Visual Representations** for multimodal LLM consumption
2. **Semantic Context** with natural language descriptions 
3. **Multi-Resolution Data** for different processing needs
4. **MCP/RAG Integration** metadata for search and retrieval
5. **Auto-Generated Insights** and contextual information
6. **Platform-Agnostic Export** in multiple formats

## Key New Classes

### VisualSummary
Container for visual representations that multimodal LLMs can interpret:

```python
visual_summary = VisualSummary(
    thumbnail_png=thumbnail_bytes,      # Small PNG for multimodal LLMs
    preview_svg=svg_string,             # Vector preview
    visual_hash="content_hash",         # For similarity detection
    color_palette=["#440154", "#fde725"], # Dominant colors
    visual_stats={                      # Visual characteristics
        "contrast_level": "high",
        "pattern_type": "radial_gradient"
    }
)
```

### SemanticContext
Semantic metadata for MCP/RAG integration and LLM interpretation:

```python
semantic_context = SemanticContext(
    natural_description="Human-readable description for LLMs",
    semantic_tags=["weather", "urban", "temperature"],
    geographic_context={"city": "NYC", "region": "Northeast"},
    temporal_context={"season": "summer", "time_of_day": "afternoon"},
    data_insights={"mean_value": 25.3, "pattern": "heat_island"},
    relationships=[{"type": "temporal", "related": "other_packages"}],
    search_keywords=["NYC weather", "urban heat", "temperature"]
)
```

### MultiResolutionData
Multi-resolution data support for different processing capabilities:

```python
multi_resolution = MultiResolutionData(
    overview={"data_type": "temperature", "key_stats": {...}},
    summary_stats={"percentiles": {...}, "spatial_stats": {...}},
    reduced_resolution={"grid": downsampled_data},
    full_resolution={"grid": full_data},
    processed_variants={"normalized": {...}, "anomaly": {...}}
)
```

## Enhanced MyrezeDataPackage API

### New Constructor Parameters

```python
package = MyrezeDataPackage(
    # ... existing parameters ...
    visual_summary=visual_summary,           # NEW: Visual representations
    semantic_context=semantic_context,       # NEW: Semantic metadata  
    multi_resolution_data=multi_resolution   # NEW: Multi-resolution support
)
```

### Auto-Generation Features

The package now automatically generates semantic context when not provided:

```python
# Auto-generates natural description, tags, geographic context, etc.
package = MyrezeDataPackage(
    id="weather-data",
    data=temperature_data,
    time=Time.timestamp("2023-01-01T12:00:00Z"),
    visualization_type="heatmap"
    # semantic_context will be auto-generated
)
```

### New Methods

#### get_llm_summary()
Get comprehensive summary optimized for LLM consumption:

```python
summary = package.get_llm_summary()
# Returns:
# {
#     "package_id": "weather-data",
#     "visualization_type": "heatmap", 
#     "time_info": {"type": "Timestamp", "value": "..."},
#     "data_structure": {"fields": [...], "field_types": {...}},
#     "semantic_context": {...},
#     "visual_info": {...},
#     "metadata": {...}
# }
```

#### generate_visual_summary()
Generate visual summary for multimodal LLMs:

```python
visual_summary = package.generate_visual_summary(auto_generate=True)
```

#### Enhanced Serialization
Control inclusion of enhanced features:

```python
# Full enhanced format (default)
full_json = package.to_json(include_enhanced_features=True)

# Legacy compatible format
legacy_json = package.to_json(include_enhanced_features=False)
```

## LLM Agent Integration Patterns

### 1. Creating Enhanced Packages

```python
import numpy as np
from myreze.data import MyrezeDataPackage, Time
from myreze.data.core import SemanticContext

# Create data
data = {
    "grid": np.random.rand(100, 100) * 30 + 10,
    "bounds": [-74.0, 40.7, -73.9, 40.8],
    "units": "celsius"
}

# Create semantic context
semantic_context = SemanticContext(
    natural_description="Temperature distribution across NYC showing urban heat patterns",
    semantic_tags=["weather", "urban", "temperature"],
    geographic_context={"city": "New York", "region": "Northeast US"}
)

# Create enhanced package
package = MyrezeDataPackage(
    id="nyc-temperature-enhanced",
    data=data,
    time=Time.timestamp("2023-07-15T14:30:00Z"),
    visualization_type="heatmap",
    semantic_context=semantic_context
)
```

### 2. Processing Received Packages

```python
def process_enhanced_package(json_data: str):
    """Process enhanced package with LLM-friendly extraction."""
    
    # Load package
    package = MyrezeDataPackage.from_json(json_data)
    
    # Get LLM-optimized summary
    summary = package.get_llm_summary()
    
    # Extract semantic information
    if package.semantic_context:
        description = package.semantic_context.natural_description
        tags = package.semantic_context.semantic_tags
        geo_context = package.semantic_context.geographic_context
        
        print(f"Description: {description}")
        print(f"Tags: {tags}")
        print(f"Location: {geo_context.get('city', 'Unknown')}")
    
    # Access multi-resolution data if available
    if package.multi_resolution_data:
        # Use overview for quick processing
        overview = package.multi_resolution_data.overview
        
        # Use reduced resolution for faster analysis
        reduced_data = package.multi_resolution_data.reduced_resolution
        
        # Use full resolution for detailed work
        full_data = package.multi_resolution_data.full_resolution
    
    return summary
```

### 3. MCP/RAG Integration

```python
def extract_for_rag_system(package: MyrezeDataPackage) -> dict:
    """Extract information for RAG system indexing."""
    
    if not package.semantic_context:
        return {}
    
    sc = package.semantic_context
    
    return {
        "document_id": package.id,
        "content": sc.natural_description,
        "keywords": sc.search_keywords,
        "tags": sc.semantic_tags,
        "geographic_bounds": sc.geographic_context.get("bounding_box"),
        "temporal_info": {
            "timestamp": package.time.value,
            "type": package.time.type
        },
        "data_type": package.visualization_type,
        "relationships": sc.relationships,
        "embeddings_metadata": {
            "text_content": sc.natural_description,
            "structured_tags": sc.semantic_tags,
            "geographic_terms": list(sc.geographic_context.values())
        }
    }
```

## Multimodal LLM Support

### Visual Information Access

```python
# Access visual summary for multimodal processing
if package.visual_summary:
    # Get thumbnail for visual analysis
    thumbnail_bytes = package.visual_summary.thumbnail_png
    
    # Get color palette for style analysis
    colors = package.visual_summary.color_palette
    
    # Get visual statistics
    visual_stats = package.visual_summary.visual_stats
    
    # Use visual hash for similarity detection
    visual_hash = package.visual_summary.visual_hash
```

### Natural Language Descriptions

```python
# Auto-generated descriptions optimized for LLM understanding
description = package.semantic_context.natural_description

# Example output:
# "This package contains a heat map showing spatial distribution of values 
#  at 2023-07-15T14:30:00Z covering area from -74.10, 40.60 to -73.90, 40.90 
#  measured in celsius."
```

## Backwards Compatibility

All enhancements are fully backwards compatible:

```python
# Legacy packages work unchanged
old_package = MyrezeDataPackage(
    id="legacy-data",
    data=data,
    time=time,
    visualization_type="heatmap"
)

# New features are optional
json_output = old_package.to_json()  # Works exactly as before

# Legacy JSON can be loaded
restored = MyrezeDataPackage.from_json(legacy_json)  # Works
```

## Discovery and Validation

Enhanced discovery capabilities for LLM agents:

```python
# Get all available semantic categories
from myreze.data.core import SEMANTIC_CATEGORIES
print(SEMANTIC_CATEGORIES)

# Validate enhanced packages
from myreze.data.validate import validate_visualization_data
errors = validate_visualization_data(package.data, package.visualization_type)

# Auto-suggest visualization types
from myreze.data.validate import suggest_visualization_type
suggestions = suggest_visualization_type(data)
```

## Use Cases

### 1. Multimodal LLM Processing
- Visual thumbnails for content-based analysis
- Natural language descriptions for understanding
- Color palettes for style transfer
- Visual hashes for similarity detection

### 2. MCP/RAG Integration
- Structured search keywords and tags
- Natural language content for embedding
- Relationship mapping for knowledge graphs
- Geographic and temporal indexing

### 3. Multi-Resolution Processing
- Overview for quick analysis
- Reduced resolution for fast processing
- Full resolution for detailed work
- Processed variants for specialized tasks

### 4. Automated Data Understanding
- Auto-generated semantic context
- Statistical insights extraction
- Geographic context identification
- Temporal pattern recognition

## Performance Considerations

### Size Optimization
- Enhanced features are optional in serialization
- Multi-resolution data allows size/quality tradeoffs
- Visual summaries are compact representations
- Legacy format maintains small size

### Processing Efficiency
- LLM summaries provide quick understanding
- Reduced resolution data enables fast processing
- Auto-generated context avoids manual annotation
- Visual hashes enable fast similarity checks

This enhanced architecture makes MyrezeDataPackage ideal for modern LLM-based systems while maintaining full compatibility with existing code. 