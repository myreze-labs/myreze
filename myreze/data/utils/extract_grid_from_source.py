import numpy as np
import xarray as xr
from rasterio.transform import from_origin

# Open ZARR
local_zarr_path = "C:/Users/Havard/prediction_20250403_164054_gdas_20250402_12_gencast_Enhanced.zarr"
ds = xr.open_zarr(local_zarr_path, chunks=False, decode_timedelta=True).compute()

def zarr_to_array(order, output_bbox=None, output_crs=None):
    ds = order.ds
    variable_name = order.weather_layer
    time_idx = float(order.timestep)

    # Only use level_idx if 'level' dimension exists
    has_level = 'level' in ds[variable_name].dims
    level_idx = float(getattr(order, 'level', None)) if has_level else None

    # Time interpolation indices
    time_idx_floor = int(np.floor(time_idx))
    time_idx_ceil = int(np.ceil(time_idx))

    # Handle edge case for integer time index
    if time_idx_floor == time_idx_ceil:
        time_idx_ceil = time_idx_floor + 1
        if time_idx_ceil >= len(ds.time):
            time_idx_ceil = time_idx_floor
            time_idx_floor = max(0, time_idx_floor - 1)

    time_weight = (time_idx - time_idx_floor) / max(1, time_idx_ceil - time_idx_floor)

    # Common selection parameters
    select_params = {'sample': 0, 'batch': 0}

    if has_level and level_idx is not None:
        # Level interpolation indices
        level_idx_floor = int(np.floor(level_idx))
        level_idx_ceil = int(np.ceil(level_idx))

        # Handle edge case for integer level index
        if level_idx_floor == level_idx_ceil:
            level_idx_ceil = level_idx_floor + 1
            if level_idx_ceil >= len(ds.level):
                level_idx_ceil = level_idx_floor
                level_idx_floor = max(0, level_idx_floor - 1)

        level_weight = (level_idx - level_idx_floor) / max(1, level_idx_ceil - level_idx_floor)

        # Get data for all four corners
        data_tl = ds[variable_name].isel(time=time_idx_floor, level=level_idx_floor, **select_params).values
        data_tr = ds[variable_name].isel(time=time_idx_ceil, level=level_idx_floor, **select_params).values
        data_bl = ds[variable_name].isel(time=time_idx_floor, level=level_idx_ceil, **select_params).values
        data_br = ds[variable_name].isel(time=time_idx_ceil, level=level_idx_ceil, **select_params).values

        # Bilinear interpolation
        top = (1 - time_weight) * data_tl + time_weight * data_tr
        bottom = (1 - time_weight) * data_bl + time_weight * data_br
        data_array = (1 - level_weight) * top + level_weight * bottom
    else:
        # Time interpolation only
        data_floor = ds[variable_name].isel(time=time_idx_floor, **select_params).values
        data_ceil = ds[variable_name].isel(time=time_idx_ceil, **select_params).values
        data_array = (1 - time_weight) * data_floor + time_weight * data_ceil

    # Check if latitudes need flipping
    if ds.lat[0].item() < ds.lat[-1].item():
        data_array = np.flipud(data_array)

    # Handle longitude wrapping
    lon_values = ds.lon.values
    split_index = np.where(lon_values >= 180)[0][0]
    data_array = np.roll(data_array, -split_index, axis=1)

    # Define the geospatial transform
    transform = from_origin(
        west=-180.0,
        north=90.0,
        xsize=0.25,
        ysize=0.25
    )

    # Define source CRS
    crs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

    # Return data with transform info and output parameters
    return data_array, transform, crs, output_bbox, output_crs
