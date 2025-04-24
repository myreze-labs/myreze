# Myreze Tutorial

## Creating a Data Package

```python
from myreze.data import MyrezeDataPackage

# Create a new data package
data_package = MyrezeDataPackage()
```

## Visualization

### Unreal Engine

```python
from myreze.viz import UnrealRenderer

renderer = UnrealRenderer()
```

### Three.js

```python
from myreze.viz import ThreeJSRenderer

renderer = ThreeJSRenderer()
```

### PNG

```python
from myreze.viz import PNGRenderer

renderer = PNGRenderer()
``` 