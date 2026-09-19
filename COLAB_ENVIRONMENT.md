# Entorno de referencia de Google Colab

Fecha de verificación: **18 de septiembre de 2026**.

Las dependencias científicas del proyecto se alinearon con el archivo público
[`pip-freeze.txt`](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt)
del repositorio oficial `googlecolab/backend-info`. Google advierte que este
inventario corresponde a la extracción más reciente del contenedor de pruebas y
puede adelantarse o retrasarse con respecto al runtime de producción.

| Paquete | Versión de referencia |
|---|---:|
| Python | 3.12 |
| affine | 3.0.1 |
| geopandas | 1.1.4 |
| ipykernel | 6.17.1 |
| ipywidgets | 7.7.1 |
| matplotlib | 3.10.0 |
| numba | 0.61.2 |
| numpy | 2.1.3 |
| openpyxl | 3.1.5 |
| pandas | 2.2.3 |
| rasterio | 1.5.1 |
| rasterstats | 0.21.0 |
| requests | 2.32.4 |
| scikit-learn | 1.6.1 |
| scipy | 1.16.3 |
| seaborn | 0.13.2 |
| shapely | 2.1.2 |

Los paquetes que no vienen preinstalados en Colab (`geotoolbox`, `gstools`,
`ipympl`, `jupyter-book`, `pycss-lem`, `pynewmarkdisp`, `pysheds`,
`scikit-gstat` y `tol-colors`) se fijan a versiones compatibles en
`pyproject.toml` y `requirements.txt`.
