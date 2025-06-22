# Dynamic Data Layer Styling Implementation Guide

## Overview

This guide explains how to implement the new dynamic data layer styling system that separates geometry from visual styling, enabling real-time material updates without regenerating entire GLB files.

## Architecture

The new system uses a **three-tier approach**:

1. **Static Geometry** (cacheable) - vertices, normals, UVs only
2. **Dynamic Textures** (small updates) - styled PNG/JPEG images  
3. **Shader Parameters** (real-time) - GPU-based styling for complex data

## Benefits

- **🚀 Performance**: Only small texture files need updating, not entire GLB files
- **💾 Caching**: Geometry cached once, textures cached by style parameters
- **🎨 Real-time**: Instant visual updates through texture/shader swapping
- **📈 Scalable**: Works for 2D overlays, 3D terrain, and complex visualizations
- **🔄 Backward Compatible**: Fallback to existing GLB system when needed

## Required Backend Changes

### 1. Modify MyrezeDataPackage.to_threejs()

```python
class MyrezeDataPackage:
    def to_threejs(self, params=None):
        """
        Enhanced to_threejs method supporting multiple output modes
        
        Args:
            params (dict): Parameters controlling output format
                - geometry_only (bool): Return GLB with only geometry data
                - return_format (str): 'glb' (default), 'texture', 'shader_params'
                - styling_params (dict): Visual styling parameters
        
        Returns:
            bytes or dict: GLB data, texture data, or shader parameters
        """
        if params is None:
            params = {}
            
        # Determine output mode
        geometry_only = params.get('geometry_only', False)
        return_format = params.get('return_format', 'glb')
        
        if return_format == 'glb':
            if geometry_only:
                return self._generate_geometry_glb(params)
            else:
                return self._generate_styled_glb(params)  # Legacy behavior
        elif return_format == 'texture':
            return self._generate_styled_texture(params)
        elif return_format == 'shader_params':
            return self._generate_shader_parameters(params)
        else:
            raise ValueError(f"Unsupported return format: {return_format}")
    
    def _generate_geometry_glb(self, params):
        """Generate GLB with only geometry data (no textures/colors)"""
        # Create mesh with vertices, normals, UVs only
        # No materials, textures, or styling applied
        # This should be much smaller and faster to generate
        pass
    
    def _generate_styled_texture(self, params):
        """Generate a styled texture based on data and styling parameters"""
        styling_params = params.get('styling_params', {})
        
        # Apply colormap, value ranges, etc. to generate texture
        # Return PNG/JPEG bytes
        pass
    
    def _generate_shader_parameters(self, params):
        """Generate shader uniforms for GPU-based styling"""
        styling_params = params.get('styling_params', {})
        
        # Return JSON with shader uniforms, vertex/fragment shader code
        return {
            'uniforms': {
                'dataMin': styling_params.get('min', 0.0),
                'dataMax': styling_params.get('max', 100.0),
                # ... other uniforms
            },
            'vertexShader': self._get_vertex_shader(),
            'fragmentShader': self._get_fragment_shader(styling_params)
        }

    def to_texture(self, styling_params):
        """
        New method specifically for texture generation
        
        Args:
            styling_params (dict): Visual styling parameters
                - colormap (str): e.g., 'viridis', 'plasma'
                - min, max, middle (float): Value ranges
                - levels (int): Number of contour levels
                - opacity (float): Transparency
        
        Returns:
            bytes: PNG image data
        """
        # Generate styled texture based on data and parameters
        # This is where colormaps, value scaling, etc. are applied
        pass
```

### 2. Enhanced FastAPI Endpoints

The new endpoints have already been added to `fastapi_routes.py`:

- `/api/datalayer-geometry/{layer_id}` - Static geometry (cacheable)
- `/api/datalayer-texture/{layer_id}` - Dynamic textures
- `/api/datalayer-shader-params/{layer_id}` - Shader parameters

## Frontend Usage Examples

### 1. Loading Data Layers with Dynamic Styling

```javascript
// The system automatically uses the new approach
// Geometry is loaded once, textures applied dynamically
const visualizations = [
    {
        layer_id: 'temperature',
        url: '/api/datalayer-glb/temperature?start=2024-01-01&end=2024-01-02&bbox=-10,50,10,60'
    }
];

await window.MapContentWindowViewer.loadDataLayers(visualizations);
```

### 2. Changing Styling Parameters

```javascript
// This now triggers texture/shader updates, not GLB regeneration
const styleParams = {
    colormap: 'plasma',
    min: -5,
    max: 35,
    opacity: 0.8,
    levels: 15
};

await window.applyDataLayerStyling('temperature', styleParams);
```

### 3. Advanced Shader-Based Styling

```javascript
// For complex 3D data that needs GPU-based styling
const advancedParams = {
    colormap: 'viridis',
    vectorScale: 2.0,
    animationSpeed: 1.0,
    levels: 50  // High level count triggers shader mode
};

await window.applyDataLayerStyling('wind_vectors', advancedParams);
```

## Implementation Strategy

### Phase 1: Basic Texture Support
1. ✅ Add new FastAPI endpoints
2. ✅ Update frontend to use texture-based styling
3. 🔄 Implement `MyrezeDataPackage.to_texture()` method
4. 🔄 Test with simple 2D overlay data

### Phase 2: Geometry Separation  
1. 🔄 Implement `geometry_only` mode in `to_threejs()`
2. 🔄 Update frontend to cache geometry models
3. 🔄 Test geometry reuse with multiple style variants

### Phase 3: Shader Support
1. 🔄 Implement shader parameter generation
2. 🔄 Add GPU-based colormaps and styling
3. 🔄 Test with complex 3D terrain and vector data

### Phase 4: Optimization
1. 🔄 Add intelligent caching strategies
2. 🔄 Implement texture compression
3. 🔄 Add performance monitoring

## Data Layer Types and Recommended Approaches

| Data Type           | Geometry           | Styling Method   | Use Case              |
| ------------------- | ------------------ | ---------------- | --------------------- |
| 2D Weather Overlays | Simple quad        | Texture          | Current flat overlays |
| 3D Terrain          | Complex mesh       | Texture + Shader | Elevation data        |
| Vector Fields       | Lines/Arrows       | Shader           | Wind, currents        |
| Point Clouds        | Instanced geometry | Shader           | Weather stations      |
| Contour Lines       | Line geometry      | Texture + Shader | Pressure contours     |

## Fallback Strategy

The system includes automatic fallback to the existing GLB approach:

```javascript
// If new system fails, automatically falls back to legacy
async function loadDataLayerGroup(geometryKey, visualizations) {
    try {
        // Try new approach
        await loadWithDynamicStyling(visualizations);
    } catch (error) {
        console.log('Falling back to legacy GLB loading');
        await loadDataLayersLegacy(visualizations);
    }
}
```

## Performance Expectations

| Operation    | Current System         | New System                          | Improvement      |
| ------------ | ---------------------- | ----------------------------------- | ---------------- |
| Initial Load | 2-5MB GLB              | 0.5-2MB geometry + 50-200KB texture | 60-80% reduction |
| Style Change | 2-5MB GLB regeneration | 50-200KB texture                    | 95%+ reduction   |
| Cache Hit    | Full download          | Geometry cached, texture only       | 90%+ reduction   |

## Testing

### Unit Tests
```python
def test_geometry_only_mode():
    package = MyrezeDataPackage(sample_data)
    glb_data = package.to_threejs({'geometry_only': True})
    # Verify no textures/materials in GLB
    assert has_only_geometry(glb_data)

def test_texture_generation():
    package = MyrezeDataPackage(sample_data)
    texture = package.to_texture({
        'colormap': 'viridis',
        'min': 0,
        'max': 100
    })
    # Verify PNG format and size
    assert is_valid_png(texture)
```

### Integration Tests
```javascript
// Test dynamic styling end-to-end
async function testDynamicStyling() {
    const layer = await loadDataLayer('test_temperature');
    
    // Change colormap
    await applyDataLayerStyling('test_temperature', {
        colormap: 'plasma'
    });
    
    // Verify texture changed, geometry unchanged
    assert(hasNewTexture(layer));
    assert(geometryUnchanged(layer));
}
```

## Migration Path

1. **Implement in parallel**: New endpoints work alongside existing ones
2. **Feature flag**: Toggle between old and new systems
3. **Gradual rollout**: Start with simple 2D overlays, expand to 3D
4. **Monitor performance**: Compare load times and user experience
5. **Full migration**: Remove old GLB-only endpoints once stable

This approach provides a robust, scalable foundation for dynamic data layer styling while maintaining backward compatibility and providing clear performance benefits. 