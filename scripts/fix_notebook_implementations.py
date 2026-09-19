"""One-time migration of implementation fixes in published teaching notebooks.

The migration is kept for provenance and is not idempotent. Do not rerun it on
already migrated notebooks; use ``validate_notebooks.py`` for routine checks.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(text: str) -> list[str]:
    return text.strip("\n").splitlines(keepends=True)


def load(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def save(relative_path: str, notebook: dict) -> None:
    (ROOT / relative_path).write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def fix_landslide_susceptibility() -> None:
    relative_path = "notebooks/01_cond_factors/landslide_susceptibility.ipynb"
    nb = load(relative_path)
    imports = "".join(nb["cells"][2]["source"])
    imports = imports.replace(
        "import rasterio\n",
        "import rasterio\nfrom rasterio.coords import BoundingBox\n"
        "from rasterio.enums import Resampling\n"
        "from rasterio.transform import array_bounds\n"
        "from rasterio.warp import reproject\n",
    )
    nb["cells"][2]["source"] = source(imports)

    nb["cells"][4]["source"] = source(r'''
def _grid(array, transform, crs, profile=None):
    return {
        "shape": array.shape,
        "transform": transform,
        "crs": crs,
        "profile": {} if profile is None else profile.copy(),
    }


def _same_grid(shape, transform, crs, reference, atol=1e-9):
    return (
        shape == reference["shape"]
        and crs == reference["crs"]
        and np.allclose(tuple(transform), tuple(reference["transform"]), atol=atol, rtol=0)
    )


def load_tiff(path, reference=None, categorical=False):
    """Read one band and, when requested, align it to a reference grid."""
    with rasterio.open(path) as src:
        source = src.read(1, masked=True).astype("float64")
        values = source.filled(np.nan)
        values[~np.isfinite(values)] = np.nan
        profile = src.profile.copy()

        if reference is not None and not _same_grid(
            values.shape, src.transform, src.crs, reference
        ):
            if src.crs is None or reference["crs"] is None:
                raise ValueError(
                    f"Raster {path!s} cannot be aligned because its CRS or the reference CRS is undefined."
                )
            aligned = np.full(reference["shape"], np.nan, dtype="float64")
            reproject(
                source=values,
                destination=aligned,
                src_transform=src.transform,
                src_crs=src.crs,
                src_nodata=np.nan,
                dst_transform=reference["transform"],
                dst_crs=reference["crs"],
                dst_nodata=np.nan,
                resampling=Resampling.nearest if categorical else Resampling.bilinear,
                init_dest_nodata=True,
            )
            values = aligned
            transform = reference["transform"]
            crs = reference["crs"]
        else:
            transform = src.transform
            crs = src.crs

    bounds = BoundingBox(*array_bounds(*values.shape, transform))
    return values, transform, crs, bounds, profile


def write_result(path, array, reference, nodata=-9999.0):
    """Write a floating-point result on the exact reference grid."""
    if array.shape != reference["shape"]:
        raise ValueError(f"Output shape {array.shape} differs from {reference['shape']}.")
    profile = reference["profile"].copy()
    profile.update(
        driver="GTiff",
        height=reference["shape"][0],
        width=reference["shape"][1],
        count=1,
        dtype="float32",
        transform=reference["transform"],
        crs=reference["crs"],
        nodata=nodata,
        compress="deflate",
    )
    output = np.where(np.isfinite(array), array, nodata).astype("float32")
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(output, 1)


def plot_field(field, bounds, title=None, cmap="viridis"):
    valid_values = np.unique(np.asarray(field)[np.isfinite(field)])
    if valid_values.size == 0:
        raise ValueError("The raster has no finite values to plot.")
    fig, ax = plt.subplots()
    extent = (bounds.left, bounds.right, bounds.bottom, bounds.top)
    if valid_values.size > n_classes:
        image = ax.imshow(field, cmap=cmap, extent=extent)
        fig.colorbar(image, ax=ax, label=title)
    else:
        field_reclassified, ticks, discrete_cmap = extract_from_discrete(field, cmap)
        image = ax.imshow(field_reclassified, cmap=discrete_cmap, extent=extent)
        colorbar = fig.colorbar(image, ax=ax, label=title, ticks=np.arange(ticks.size))
        colorbar.ax.set_yticklabels([f"{value:g}" for value in ticks])
    ax.set(xlabel="Easting [m]", ylabel="Northing [m]")
    fig.canvas.header_visible = False
    fig.canvas.toolbar_position = "bottom"
    plt.show()
    return fig


def extract_from_discrete(field, cmap="viridis"):
    ticks = np.unique(np.asarray(field)[np.isfinite(field)])
    field_reclassified = np.full_like(field, np.nan, dtype=float)
    for index, value in enumerate(ticks):
        field_reclassified[field == value] = index
    discrete_cmap = plt.colormaps.get_cmap(cmap).resampled(ticks.size)
    return field_reclassified, ticks, discrete_cmap


def nan_gaussian_filter(data, sigma):
    nan_mask = ~np.isfinite(data)
    data_filled = np.where(nan_mask, 0.0, data)
    weights = (~nan_mask).astype(float)
    filtered = sp.ndimage.gaussian_filter(data_filled, sigma=sigma, mode="constant", cval=0.0)
    filtered_weights = sp.ndimage.gaussian_filter(weights, sigma=sigma, mode="constant", cval=0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalized = np.divide(
            filtered,
            filtered_weights,
            out=np.full_like(filtered, np.nan),
            where=filtered_weights > 0,
        )
    normalized[nan_mask] = np.nan
    return normalized
''')

    nb["cells"][8]["source"] = source(r'''
if testing_data:
    base_url = "https://raw.githubusercontent.com/eamontoyaa/data4testing/main/susceptibility"
    conditioning_paths = {
        "elevation": f"{base_url}/elevation.tif",
        "slope": f"{base_url}/slope.tif",
        "aspect": f"{base_url}/aspect.tif",
        "curvature": f"{base_url}/curvature.tif",
        "flow_acc": f"{base_url}/flow_acc.tif",
        "tpi": f"{base_url}/tpi.tif",
        "roads_prox": f"{base_url}/roads_prox.tif",
        "rivers_prox": f"{base_url}/rivers_prox.tif",
        "geomorphology": f"{base_url}/geomorphology.tif",
    }

    elevation, transform, crs, bounds, profile = load_tiff(conditioning_paths["elevation"])
    reference_grid = _grid(elevation, transform, crs, profile)
    conditioning = {"elevation": elevation}
    for name, path in list(conditioning_paths.items())[1:]:
        conditioning[name], _, _, _, _ = load_tiff(
            path,
            reference=reference_grid,
            categorical=name == "geomorphology",
        )

    df_cond_fact = pd.DataFrame(
        {name: values.ravel() for name, values in conditioning.items()}
    )
    independent_vars = df_cond_fact.columns.to_list()
    independent_vars_types = ["d" if name == "geomorphology" else "c" for name in independent_vars]

    landslides, _, _, _, _ = load_tiff(
        f"{base_url}/landslides.tif",
        reference=reference_grid,
        categorical=True,
    )
    # Inventory rasters commonly store only mapped landslides and encode the
    # remaining terrain as nodata. Within the conditioning-factor domain,
    # nodata therefore represents absence (0), not an invalid analysis cell.
    landslides = np.where(landslides == 1, 1.0, 0.0)
    df_landslides = pd.Series(landslides.ravel(), name="landslide")

    plot_specs = {
        "elevation": ("Elevation [m]", "terrain"),
        "slope": ("Slope [deg]", "RdYlGn_r"),
        "aspect": ("Aspect [deg]", "twilight"),
        "curvature": ("Curvature", "seismic"),
        "flow_acc": ("Flow accumulation", "Blues"),
        "tpi": ("Topographic position index", "viridis"),
        "roads_prox": ("Distance to roads", "viridis"),
        "rivers_prox": ("Distance to rivers", "Blues_r"),
        "geomorphology": ("Geomorphology", "Accent"),
    }
    for name, (label, cmap_name) in plot_specs.items():
        plot_field(conditioning[name], bounds, title=label, cmap=cmap_name)
    plot_field(landslides, bounds, title="Landslide inventory", cmap="binary")
''')

    nb["cells"][10]["source"] = source(r'''
if not testing_data:
    outputs_folder = "outputs"
    os.makedirs(outputs_folder, exist_ok=True)
    if not local_data:
        uploaded = files.upload()
        conditioning_files = [os.path.join(os.getcwd(), name) for name in uploaded]
    else:
        conditioning_files = [
            os.path.join(local_folder_conditioning_factors, name)
            for name in sorted(os.listdir(local_folder_conditioning_factors))
        ]
    conditioning_files = [path for path in conditioning_files if path.lower().endswith((".tif", ".tiff"))]
    if not conditioning_files:
        raise FileNotFoundError("No conditioning-factor GeoTIFF files were provided.")

    df_cond_fact = pd.DataFrame()
    reference_grid = None
    for path in conditioning_files:
        file_name = os.path.splitext(os.path.basename(path))[0].split(" ")[0]
        raster, transform, crs, bounds, profile = load_tiff(
            path,
            reference=reference_grid,
            categorical=False,
        )
        if reference_grid is None:
            reference_grid = _grid(raster, transform, crs, profile)
        print(f"Loaded {file_name}: shape={raster.shape}, resolution={reference_grid['transform'].a:g}")
        plot_field(raster, bounds, title=file_name)
        df_cond_fact[file_name] = raster.ravel()

    independent_vars = df_cond_fact.columns.to_list()
    independent_vars_types = [
        "d" if df_cond_fact[name].nunique(dropna=True) <= n_classes else "c"
        for name in independent_vars
    ]
''')

    nb["cells"][12]["source"] = source(r'''
if not testing_data:
    if not local_data:
        uploaded_inventory = files.upload()
        inventory_files = [os.path.join(os.getcwd(), name) for name in uploaded_inventory]
    else:
        inventory_files = [
            os.path.join(local_folder_inventory, name)
            for name in sorted(os.listdir(local_folder_inventory))
        ]
    inventory_files = [path for path in inventory_files if path.lower().endswith((".tif", ".tiff"))]
    if len(inventory_files) != 1:
        raise ValueError("Provide exactly one landslide-inventory GeoTIFF.")

    landslides, _, _, _, _ = load_tiff(
        inventory_files[0],
        reference=reference_grid,
        categorical=True,
    )
    # Accept both conventional 0/1 inventories and presence-only rasters.
    landslides = np.where(landslides == 1, 1.0, 0.0)
    df_landslides = pd.Series(landslides.ravel(), name="landslide")
    plot_field(landslides, bounds, title="Landslide inventory", cmap="binary")
''')

    nb["cells"][13]["source"] = source(r'''
mask_nan = df_cond_fact.isna().any(axis=1) | df_landslides.isna()
df_cond_fact.loc[mask_nan, :] = np.nan
df_landslides.loc[mask_nan] = np.nan
mask_nan_mtx = mask_nan.to_numpy().reshape(reference_grid["shape"])

if (~mask_nan).sum() == 0:
    raise ValueError("The raster stack has no cells that are valid in every input layer.")
if df_landslides.loc[~mask_nan].nunique() < 2:
    raise ValueError("The valid inventory must contain both stable and landslide cells.")
''')

    nb["cells"][18]["source"] = source(r'''
df_cond_fact_p = pd.DataFrame(index=df_cond_fact.index)
n_class_by_var = {}

for variable, variable_type in zip(independent_vars, independent_vars_types):
    classes = np.full(len(df_cond_fact), -1, dtype=int)
    valid = df_cond_fact[variable].notna()
    if variable_type == "c":
        classes[valid] = pd.qcut(
            df_cond_fact.loc[valid, variable],
            q=n_classes,
            labels=False,
            duplicates="drop",
        ).astype(int)
    elif variable_type == "d":
        classes[valid] = pd.Categorical(df_cond_fact.loc[valid, variable]).codes
    else:
        raise ValueError(f"Unknown variable type {variable_type!r} for {variable!r}.")
    n_class_by_var[variable] = int(classes[valid].max() + 1)
    df_cond_fact_p[variable] = classes

df_cond_fact_p.loc[mask_nan, :] = -1
df_cond_fact_p
''')

    nb["cells"][20]["source"] = source(r'''
max_classes = max(n_class_by_var.values())
Fij = np.full((max_classes, len(independent_vars)), np.nan)
NFij = np.full_like(Fij, np.nan)

for column, variable in enumerate(independent_vars):
    for class_id in range(n_class_by_var[variable]):
        in_class = df_cond_fact_p[variable] == class_id
        Fij[class_id, column] = np.sum(in_class & (df_landslides == 1))
        NFij[class_id, column] = np.sum(in_class & (df_landslides == 0))

Nij = Fij + NFij
pd.DataFrame(Nij, columns=independent_vars, index=[f"Class {i}" for i in range(max_classes)])
''')

    nb["cells"][22]["source"] = source(r'''
Ftot = np.nansum(Fij, axis=0)
NFtot = np.nansum(NFij, axis=0)
Ntot = Ftot + NFtot
if np.any(Ftot == 0) or np.any(NFtot == 0):
    raise ValueError("Each factor requires valid cells with and without mapped landslides.")

with np.errstate(divide="ignore", invalid="ignore"):
    Dij = np.divide(Fij, Nij, out=np.full_like(Fij, np.nan), where=Nij > 0)
    Dast = Ftot / Ntot
    Wij = np.log10(Dij / Dast)

for column in range(Wij.shape[1]):
    finite = np.isfinite(Wij[:, column])
    zero_density = np.isneginf(Wij[:, column])
    if not finite.any():
        raise ValueError(f"No finite information weights for {independent_vars[column]!r}.")
    Wij[zero_density, column] = np.min(Wij[finite, column])

pd.DataFrame(Wij, columns=independent_vars, index=[f"Class {i}" for i in range(max_classes)])
''')

    nb["cells"][24]["source"] = source(r'''
df_cond_fact_w = pd.DataFrame(index=df_cond_fact.index)
for column, variable in enumerate(independent_vars):
    classes = df_cond_fact_p[variable].to_numpy()
    weights = np.full(classes.shape, np.nan, dtype=float)
    valid = classes >= 0
    weights[valid] = Wij[classes[valid], column]
    df_cond_fact_w[variable] = weights

df_cond_fact_w["ISTCU"] = df_cond_fact_w[independent_vars].sum(axis=1, min_count=len(independent_vars))
df_cond_fact_w.loc[mask_nan, :] = np.nan
df_cond_fact_w
''')

    nb["cells"][26]["source"] = source(r'''
weighted_mean = np.nansum(Wij * Nij, axis=0) / np.nansum(Nij, axis=0)
sigma = np.sqrt(
    np.nansum(Nij * (Wij - weighted_mean) ** 2, axis=0)
    / np.nansum(Nij, axis=0)
)
sigma_sorted = pd.Series(sigma, index=independent_vars).sort_values(ascending=False)
sigma_sorted
''')

    nb["cells"][35]["source"] = source(r'''
want_to_save = not testing_data
if want_to_save:
    write_result(os.path.join(outputs_folder, "ISTZU.tif"), ISTZU, reference_grid)
''')

    nb["cells"][41]["source"] = source(r'''
inventory = df_landslides.loc[~mask_nan].to_numpy(dtype=float)
zonation_index = df_cond_fact_w.loc[~mask_nan, "ISTZU"].to_numpy(dtype=float)

sorted_indices = np.argsort(zonation_index)[::-1]
sorted_index = zonation_index[sorted_indices]
sorted_inventory = inventory[sorted_indices]
total_inventory = sorted_inventory.sum()
if total_inventory <= 0:
    raise ValueError("The inventory has no mapped landslide cells.")

cumulative_inventory = np.cumsum(sorted_inventory) / total_inventory
cumulative_area = np.arange(1, sorted_index.size + 1) / sorted_index.size

idx_LM = min(np.searchsorted(cumulative_inventory, low_to_mod_perc / 100), sorted_index.size - 1)
idx_MH = min(np.searchsorted(cumulative_inventory, mod_to_high_perc / 100), sorted_index.size - 1)
threshold_LM = sorted_index[idx_LM]
threshold_MH = sorted_index[idx_MH]
susceptibility_thresholds = sorted([threshold_LM, threshold_MH])

roc_auc = roc_auc_score(inventory, zonation_index)
success_rate_auc = np.trapezoid(
    np.r_[0.0, cumulative_inventory],
    np.r_[0.0, cumulative_area],
)
print(f"ROC AUC: {roc_auc:.4f}; success-rate AUC: {success_rate_auc:.4f}")

fig, ax = plt.subplots(figsize=(5, 4))
ax.plot(
    cumulative_area * 100,
    cumulative_inventory * 100,
    color="k",
    label=f"Success-rate curve\n(AUC = {success_rate_auc:.2f})",
)
ax.fill_between(cumulative_area[:idx_MH + 1] * 100, cumulative_inventory[:idx_MH + 1] * 100,
                color=colors[-1], alpha=0.6, label="High susceptibility")
ax.fill_between(cumulative_area[idx_MH:idx_LM + 1] * 100, cumulative_inventory[idx_MH:idx_LM + 1] * 100,
                color=colors[-2], alpha=0.6, label="Moderate susceptibility")
ax.fill_between(cumulative_area[idx_LM:] * 100, cumulative_inventory[idx_LM:] * 100,
                color=colors[0], alpha=0.6, label="Low susceptibility")
ax.set(xlabel="Cumulative area [%]", ylabel="Cumulative inventory [%]")
ax.legend(loc="lower right")
ax.grid(True)
ax.set_aspect("equal")
plt.show()
''')

    nb["cells"][43]["source"] = source(r'''
if not testing_data:
    write_result(
        os.path.join(outputs_folder, "susceptibility_zonation.tif"),
        susceptibility_zonation,
        reference_grid,
    )
''')
    save(relative_path, nb)


def fix_earthquake_notebooks() -> None:
    scalar_path = "notebooks/02_trigg_factors/infinite_slope_earthquake.ipynb"
    nb = load(scalar_path)
    code = "".join(nb["cells"][4]["source"])
    code = code.replace(
        "    time, accel = record.T\n    return time, accel",
        "    record = np.asarray(record, dtype=float)\n"
        "    if record.ndim != 2 or record.shape[1] != 2:\n"
        "        raise ValueError(\"The record must contain exactly two columns: time and acceleration.\")\n"
        "    time, accel = record.T\n"
        "    if not np.all(np.isfinite(record)) or np.any(np.diff(time) <= 0):\n"
        "        raise ValueError(\"Time and acceleration must be finite, and time must increase strictly.\")\n"
        "    return time, accel",
    )
    nb["cells"][4]["source"] = source(code)
    save(scalar_path, nb)

    spatial_path = "notebooks/02_trigg_factors/infinite_slope_earthquake_spatial.ipynb"
    nb = load(spatial_path)
    nb["cells"][5]["source"] = source(r'''
url = "https://raw.githubusercontent.com/eamontoyaa/data4testing/main/pynewmarkdisp/"

earthquake_record = pd.read_csv(f"{url}earthquake_data_simple.csv", sep=";")
time = earthquake_record["Time"].to_numpy(dtype=float)
accel = earthquake_record["Acceleration"].to_numpy(dtype=float)
g = 1.0  # Acceleration is expressed as a fraction of gravity.
if not np.all(np.isfinite([time, accel])) or np.any(np.diff(time) <= 0):
    raise ValueError("The earthquake record must be finite and time must increase strictly.")

raster_names = ["dem", "slope", "zones", "zmax", "depthwt"]
spatial_data = {}
headers = {}
for name in raster_names:
    spatial_data[name], headers[name] = load_ascii_raster(
        f"{url}spatial_data_dummy_example/{name}.asc"
    )

header = headers["dem"]
grid_keys = ("ncols", "nrows", "xllcorner", "yllcorner", "cellsize")
for name in raster_names[1:]:
    for key in grid_keys:
        first, second = header[key], headers[name][key]
        if not np.isclose(first, second):
            raise ValueError(f"Raster {name!r} does not match the DEM grid at {key!r}.")

dem = spatial_data["dem"]
slope = spatial_data["slope"]
zones = spatial_data["zones"]
depth = spatial_data["zmax"]
depth_w = spatial_data["depthwt"]
valid_mask = np.logical_and.reduce(
    [np.isfinite(spatial_data[name]) for name in raster_names]
)
for array in (dem, slope, zones, depth, depth_w):
    array[~valid_mask] = np.nan
''')
    save(spatial_path, nb)


def fix_probability_notebook() -> None:
    relative_path = "notebooks/03_rupture/prob_failure_infinite_slope.ipynb"
    nb = load(relative_path)
    code = "".join(nb["cells"][4]["source"])
    code = code.replace("def compute_pf_variation_vector(data, confidence_level=0.95):", "def compute_pf_variation_vector(data):")
    code = code.replace("def random_sample_uniform(min, max, n, seed=None):", "def random_sample_uniform(lower, upper, n, seed=None):")
    code = code.replace("return rng.uniform(min, max, n)", "return rng.uniform(lower, upper, n)")
    nb["cells"][4]["source"] = source(code)
    save(relative_path, nb)


def fix_mohr_defaults() -> None:
    relative_path = "notebooks/01_cond_factors/mohr_circles_and_stress_paths.ipynb"
    nb = load(relative_path)
    defaults = {
        4: '{"c": 5, "𝜙": 27}',
        5: '{"c": 20, "𝜙": 35}',
        6: '{"c": 10, "𝜙": 30}',
    }
    for index, default in defaults.items():
        code = "".join(nb["cells"][index]["source"])
        code = code.replace("envelope={'c': 5, '𝜙': 27}", "envelope=None")
        code = code.replace("envelope={'c': 20, '𝜙': 35}", "envelope=None")
        code = code.replace('envelope={"c": 10, "𝜙": 30}', "envelope=None")
        marker = "):\n"
        if "envelope=None" in code and "if envelope is None:" not in code:
            position = code.find(marker, code.find("envelope=None"))
            if position >= 0:
                position += len(marker)
                code = code[:position] + f"    if envelope is None:\n        envelope = {default}\n" + code[position:]
        nb["cells"][index]["source"] = source(code)
    save(relative_path, nb)


def fix_runout() -> None:
    relative_path = "notebooks/04_propagation/runout_semiempirical.ipynb"
    nb = load(relative_path)
    nb["cells"][6]["source"] = source(r'''
working_dir = "./data/"
os.makedirs(working_dir, exist_ok=True)
path2dem = os.path.join(working_dir, "DEM.tif")

if testing_data:
    url = "https://raw.githubusercontent.com/eamontoyaa/data4testing/main/runout/DEM.tif"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(path2dem, "wb") as file:
        file.write(response.content)
elif "google.colab" in str(get_ipython()):
    uploaded = files.upload()
    if len(uploaded) != 1:
        raise ValueError("Upload exactly one DEM GeoTIFF.")
    shutil.move(next(iter(uploaded)), path2dem)
else:
    tk.Tk().withdraw()
    selected_path = askopenfilename(filetypes=[("GeoTIFF", "*.tif *.tiff")])
    if not selected_path:
        raise FileNotFoundError("No DEM was selected.")
    shutil.copy2(selected_path, path2dem)

DEM, transform_DEM, bounds_DEM, crs_DEM, nodata_DEM = gt.sig_helper.load_raster(path2dem)
if crs_DEM is None or not crs_DEM.is_projected:
    raise ValueError("The DEM must use a projected CRS with linear horizontal units.")
pixel_width = abs(transform_DEM.a)
pixel_height = abs(transform_DEM.e)
if not np.isclose(transform_DEM.b, 0.0, atol=1e-12) or not np.isclose(transform_DEM.d, 0.0, atol=1e-12):
    raise ValueError("The DEM must be north-up and must not contain grid rotation.")
if not np.isclose(pixel_width, pixel_height, rtol=0.01, atol=1e-9):
    raise ValueError("The DEM pixels must be square within a 1% tolerance.")
cellsize = (pixel_width + pixel_height) / 2

dem_values = np.ma.asarray(DEM).filled(np.nan).astype(float)
dem_values[~np.isfinite(dem_values)] = np.nan
valid_dem = np.isfinite(dem_values)
if not valid_dem.any():
    raise ValueError("The DEM contains no valid elevation cells.")

extent = (bounds_DEM.left, bounds_DEM.right, bounds_DEM.bottom, bounds_DEM.top)
HSD = gt.sig_helper.get_hillshade(
    np.ma.masked_invalid(dem_values),
    azimuth=315,
    altitude=35,
    cellsize=cellsize,
)

with rasterio.open(path2dem) as source_dem:
    dem_profile = source_dem.profile.copy()


def write_dem_grid(path, values, nodata):
    """Write a result on the DEM's exact grid with explicit nodata metadata."""
    array = np.asarray(values)
    if array.shape != dem_values.shape:
        raise ValueError("The result shape does not match the DEM grid.")
    if np.issubdtype(array.dtype, np.floating):
        array = np.where(np.isfinite(array), array, nodata)
    profile = dem_profile.copy()
    profile.update(driver="GTiff", count=1, dtype=array.dtype.name, nodata=nodata, compress="deflate")
    with rasterio.open(path, "w", **profile) as destination:
        destination.write(array, 1)
''')
    code = "".join(nb["cells"][9]["source"]).replace("ax.imshow(DEM,", "ax.imshow(dem_values,").replace("ax.contour(DEM,", "ax.contour(dem_values,")
    nb["cells"][9]["source"] = source(code)
    nb["cells"][11]["source"] = source(r'''
height, width = dem_values.shape
sources_array = np.zeros((height, width), dtype=np.int16)
for x, y in sources_coords:
    row, col = rasterio.transform.rowcol(transform_DEM, x, y)
    if not (0 <= row < height and 0 <= col < width):
        raise ValueError(f"Release point {(x, y)} lies outside the DEM extent.")
    if not valid_dem[row, col]:
        raise ValueError(f"Release point {(x, y)} falls on a DEM nodata cell.")
    sources_array[row, col] = 1

path2sources = os.path.join(working_dir, "sources.tif")
write_dem_grid(path2sources, sources_array, nodata=0)
''')
    nb["cells"][16]["source"] = source(r'''
z_delta_plot = np.asarray(z_delta, dtype=float)
z_delta_plot[(z_delta_plot == 0) | ~valid_dem] = np.nan

write_dem_grid(
    os.path.join(working_dir, "z_delta.tif"),
    z_delta_plot.astype("float32"),
    nodata=-9999.0,
)
''')
    code = "".join(nb["cells"][17]["source"]).replace("ax.imshow(DEM,", "ax.imshow(dem_values,").replace("ax.contour(DEM,", "ax.contour(dem_values,")
    nb["cells"][17]["source"] = source(code)
    save(relative_path, nb)


def fix_rainfall_spatial() -> None:
    relative_path = "notebooks/02_trigg_factors/infinite_slope_rainfall_spatial.ipynb"
    nb = load(relative_path)

    code = "".join(nb["cells"][2]["source"])
    code = code.replace('"nodata_value": eval(header[5, 1]),', '"nodata_value": float(header[5, 1]),')
    code = code.replace("yll = transform.f - nrows * transform.e", "yll = transform.f + nrows * transform.e")
    code = code.replace(
        "def save_raster(file_path, array, crs, transform, nodata=None, format=\"tif\"):\n"
        "    if format == \"asc\":\n"
        "        print(\"Writing ASCII file...\")\n"
        "        _save_asc(file_path, array, transform, nodata)\n"
        "    else:\n"
        "        print(\"Writing GeoTIFF file...\")\n"
        "        driver = \"GTiff\"\n"
        "        with rasterio.open(\n"
        "            file_path, \"w\", driver=driver,\n"
        "            height=array.shape[0], width=array.shape[1],\n"
        "            count=1, dtype=array.dtype,\n"
        "            crs=crs, transform=transform, nodata=nodata,\n"
        "        ) as dst:\n"
        "            dst.write(array, 1)",
        "def save_raster(file_path, array, crs, transform, nodata=None, format=\"tif\"):\n"
        "    values = np.ma.asarray(array)\n"
        "    if values.ndim != 2:\n"
        "        raise ValueError(\"Only single-band 2-D rasters are supported.\")\n"
        "    if nodata is None and np.ma.getmaskarray(values).any():\n"
        "        nodata = -9999.0\n"
        "    output = values.filled(nodata) if nodata is not None else np.asarray(values)\n"
        "    if format == \"asc\":\n"
        "        print(\"Writing ASCII file...\")\n"
        "        _save_asc(file_path, output, transform, nodata)\n"
        "    else:\n"
        "        print(\"Writing GeoTIFF file...\")\n"
        "        with rasterio.open(\n"
        "            file_path, \"w\", driver=\"GTiff\",\n"
        "            height=output.shape[0], width=output.shape[1],\n"
        "            count=1, dtype=output.dtype,\n"
        "            crs=crs, transform=transform, nodata=nodata, compress=\"deflate\",\n"
        "        ) as dst:\n"
        "            dst.write(output, 1)",
    )
    code = code.replace(
        "    dst_height,\n    is_categorical=False,",
        "    dst_height,\n    dst_crs,\n    is_categorical=False,",
    )
    code = code.replace("        dst_crs=src_crs,", "        dst_crs=dst_crs,")
    validation = r'''

def assert_matching_grids(metadata, reference_name="dem", atol=1e-9):
    """Fail before combining rasters that do not use one exact grid."""
    reference = metadata[reference_name]
    for name, item in metadata.items():
        if name == reference_name:
            continue
        same = (
            item["shape"] == reference["shape"]
            and item["crs"] == reference["crs"]
            and np.allclose(tuple(item["transform"]), tuple(reference["transform"]), atol=atol, rtol=0)
        )
        if not same:
            raise ValueError(
                f"Raster {name!r} is not aligned with {reference_name!r}. "
                "Set resample_data=True or preprocess the stack on a common grid."
            )


def assert_matching_ascii_headers(headers, reference_name="dem"):
    reference = headers[reference_name]
    keys = ("ncols", "nrows", "xllcorner", "yllcorner", "cellsize")
    for name, header_item in headers.items():
        if any(not np.isclose(header_item[key], reference[key]) for key in keys):
            raise ValueError(f"ASCII raster {name!r} does not match the DEM grid.")
'''
    code = code.rstrip() + validation
    nb["cells"][2]["source"] = source(code)

    nb["cells"][6]["source"] = source(r'''
def upload_raster_to_colab(file_name):
    """Select one raster in Colab or locally and copy it to the input folder."""
    destination = os.path.join(inputs_dir, f"{file_name}.tif")
    if "google.colab" in str(get_ipython()):
        uploaded = files.upload()
        if len(uploaded) != 1:
            raise ValueError(f"Upload exactly one raster for {file_name!r}.")
        shutil.move(next(iter(uploaded)), destination)
    else:
        tk.Tk().withdraw()
        selected = askopenfilename(filetypes=[("GeoTIFF", "*.tif *.tiff")])
        if not selected:
            raise FileNotFoundError(f"No raster was selected for {file_name!r}.")
        shutil.copy2(selected, destination)
    return destination
''')

    nb["cells"][8]["source"] = source(r'''
if testing_data:
    ascii_headers = {}
    spatial_arrays = {}
    for name in ["dem", "zmax", "depthwt", "slope", "directions", "rizero", "zones"]:
        get_asc_from_url(name)
        spatial_arrays[name], ascii_headers[name] = load_ascii_raster(f"{inputs_dir}/{name}.asc")
    assert_matching_ascii_headers(ascii_headers)
    header = ascii_headers["dem"]
    cellsize = header["cellsize"]
    dem = spatial_arrays["dem"]
    slope = spatial_arrays["slope"]
    directions = spatial_arrays["directions"]
    zones = spatial_arrays["zones"]
    depth = spatial_arrays["zmax"]
    rizero = spatial_arrays["rizero"]
    depth_w = spatial_arrays["depthwt"]
    valid_mask = np.logical_and.reduce(
        [np.isfinite(spatial_arrays[name]) for name in spatial_arrays]
    )
    for values in spatial_arrays.values():
        values[~valid_mask] = np.nan
else:
    paths = {"dem": os.path.join(inputs_dir, "dem.tif"), "directions": os.path.join(inputs_dir, "directions.tif")}
    for name, prompt in [
        ("slope", "Uploading the slope raster..."),
        ("zones", "Uploading the zones raster..."),
        ("zmax", "Uploading the maximum-depth raster..."),
        ("depthwt", "Uploading the water-table-depth raster..."),
    ]:
        print(prompt)
        paths[name] = upload_raster_to_colab(name)

    loaded = {name: load_raster(path, masked=True) for name, path in paths.items()}
    dem, transform_dem, bounds_dem, crs_dem, nodata_dem = loaded["dem"]
    directions, transform_directions, bounds_directions, crs_directions, nodata_directions = loaded["directions"]
    slope, transform_slope, bounds_slope, crs_slope, nodata_slope = loaded["slope"]
    zones, transform_zones, bounds_zones, crs_zones, nodata_zones = loaded["zones"]
    depth, transform_depth, bounds_depth, crs_depth, nodata_depth = loaded["zmax"]
    depth_w, transform_depth_w, bounds_depth_w, crs_depth_w, nodata_depth_w = loaded["depthwt"]

    raster_metadata = {
        name: {"shape": item[0].shape, "transform": item[1], "crs": item[3]}
        for name, item in loaded.items()
    }
    if not resample_data:
        assert_matching_grids(raster_metadata)
''')

    code = "".join(nb["cells"][9]["source"])
    code = code.replace(
        "target_transform, target_width, target_height,\n        is_categorical=",
        "target_transform, target_width, target_height, crs_dem,\n        is_categorical=",
    )
    # Handle indentation variants in all six calls.
    code = code.replace(
        "target_transform, target_width, target_height,\n            is_categorical=",
        "target_transform, target_width, target_height, crs_dem,\n            is_categorical=",
    )
    nb["cells"][9]["source"] = source(code)

    code = "".join(nb["cells"][14]["source"])
    code = code.replace(
        '_ = subprocess.run([f"chmod +x ./{project_name}/Exe_TopoIndex"], shell=True, capture_output=True, text=True)',
        'subprocess.run(["chmod", "+x", f"./{project_name}/Exe_TopoIndex"], check=True)',
    )
    code = code.replace(
        '_ = subprocess.run([f"chmod +x {exe}"], shell=True, capture_output=True, text=True)  # Change permission',
        'subprocess.run(["chmod", "+x", exe], check=True)',
    )
    code = code.replace(
        "[f'mpirun -np {trg_inputs[\"NP\"]} {exe}'],",
        '["mpirun", "-np", str(trg_inputs["NP"]), exe],',
    )
    code = code.replace("os.rename(", "os.replace(")
    nb["cells"][14]["source"] = source(code)

    code = "".join(nb["cells"][16]["source"])
    code = code.replace('output_path = "./{project_name}/"', 'output_path = f"./{project_name}/"')
    nb["cells"][16]["source"] = source(code)

    code = "".join(nb["cells"][34]["source"])
    code = code.replace("if resample_data:\n", "if not testing_data and resample_data:\n")
    nb["cells"][34]["source"] = source(code)
    save(relative_path, nb)


def fix_rainfall_single_cell() -> None:
    relative_path = "notebooks/02_trigg_factors/infinite_slope_rainfall.ipynb"
    nb = load(relative_path)
    code = "".join(nb["cells"][6]["source"])
    code = code.replace(
        'subprocess.call(["chmod +x ./TRIGRS_1/Exe_TopoIndex"], shell=True)',
        'subprocess.run(["chmod", "+x", "./TRIGRS_1/Exe_TopoIndex"], check=True)',
    )
    code = code.replace(
        'subprocess.call([f"chmod +x {exe}"], shell=True)',
        'subprocess.run(["chmod", "+x", exe], check=True)',
    )
    code = code.replace(
        "[f'mpirun -np {trg_inputs[\"NP\"]} {exe}'], shell=True",
        '["mpirun", "-np", str(trg_inputs["NP"]), exe], check=True',
    )
    code = code.replace("subprocess.call([exe], shell=True)", "subprocess.run([exe], check=True)")
    code = code.replace("os.rename(", "os.replace(")
    nb["cells"][6]["source"] = source(code)
    save(relative_path, nb)


def translate_code_comments() -> None:
    replacements = {
        "# transform.e es negativo": "# transform.e is negative",
        "# Escribe con formato consistente: 4 decimales para floats": "# Use a consistent four-decimal format for floating-point values",
        "Construye una nueva grilla con celda más grande, conservando la misma extensión.": "Build a coarser grid while preserving the source extent.",
        "# e normalmente es negativo": "# e is normally negative",
        "Remuestrea un raster enmascarado (`np.ma.MaskedArray`) a una grilla destino.": "Resample a masked raster (`np.ma.MaskedArray`) to a destination grid.",
        "# Para variables continuas al pasar a celda más grande,": "# Average resampling is appropriate for continuous variables",
        "# average suele ser mejor que nearest.": "# when aggregating to a coarser grid.",
        "# uploaded = files.upload()  # sube el archivo": "# uploaded = files.upload()  # Upload one file",
    }
    from scripts.refactor_notebooks import NOTEBOOKS

    for relative_path in NOTEBOOKS:
        nb = load(relative_path)
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                continue
            code = "".join(cell["source"])
            for old, new in replacements.items():
                code = code.replace(old, new)
            cell["source"] = source(code)
        save(relative_path, nb)


def main() -> None:
    fix_landslide_susceptibility()
    fix_earthquake_notebooks()
    fix_probability_notebook()
    fix_mohr_defaults()
    fix_runout()
    fix_rainfall_spatial()
    fix_rainfall_single_cell()
    translate_code_comments()


if __name__ == "__main__":
    main()
