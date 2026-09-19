# Estabilidad de taludes

Libro digital y herramientas reproducibles para el curso de posgrado de
**Estabilidad de Taludes** de la Universidad EAFIT.

[![Jupyter Book](https://img.shields.io/badge/Jupyter_Book-ver_sitio-F37726?style=for-the-badge&logo=jupyter&logoColor=white)](https://appliedmechanics-eafit.github.io/slope_stability/)

## Uso local

El entorno del proyecto está alineado con las versiones científicas del runtime
de Google Colab, verificado el 18 de septiembre de 2026:

```bash
UV_PROJECT_ENVIRONMENT=/home/eamontoyaa/.venvs/eafit-env uv sync
source /home/eamontoyaa/.venvs/eafit-env/bin/activate
jupyter book build --html --strict
```

Para validar la estructura y el código de los notebooks sin ejecutar los
modelos: `python scripts/validate_notebooks.py`.

El sitio se genera en `_build/html`. Cada capítulo incluye un enlace a Colab y
mantiene dos rutas de entrada: datos públicos de demostración o carga de archivos
propios. Los rasters propios deben tener CRS definido; los notebooks comprueban o
alinean extensión, origen, resolución, tamaño y valores `nodata` antes de operar.

## Contenido

### Dominio espacial (análisis territorial)

Herramientas que trabajan con inventarios y rasters sobre un área de estudio.

#### Factores condicionantes

1. [Susceptibilidad a movimientos en masa](./notebooks/01_spatial_domain/01_conditioning_factors/landslide_susceptibility.ipynb)

#### Factores detonantes

1. [Sismo en un dominio espacial](./notebooks/01_spatial_domain/02_triggering_factors/infinite_slope_earthquake_spatial.ipynb)
1. [Lluvia en un dominio espacial](./notebooks/01_spatial_domain/02_triggering_factors/infinite_slope_rainfall_spatial.ipynb)

#### Propagación

1. [Simulación semiempírica de propagación](./notebooks/01_spatial_domain/04_propagation/runout_semiempirical.ipynb)

### Dominio talud (análisis local)

Herramientas para caracterizar y analizar un talud o sección representativa.

#### Factores condicionantes

1. [Círculos de Mohr y trayectorias de esfuerzos](./notebooks/02_slope_domain/01_conditioning_factors/mohr_circles_and_stress_paths.ipynb)
1. [Círculo de Mohr para deformaciones](./notebooks/02_slope_domain/01_conditioning_factors/mohr_circles_for_strains.ipynb)
1. [Procesamiento del ensayo SPT](./notebooks/02_slope_domain/01_conditioning_factors/spt_processing.ipynb)
1. [Envolventes de resistencia al corte](./notebooks/02_slope_domain/01_conditioning_factors/strength_envelopes.ipynb)

#### Factores detonantes

1. [Sismo en un talud infinito](./notebooks/02_slope_domain/02_triggering_factors/infinite_slope_earthquake.ipynb)
1. [Lluvia en un talud infinito](./notebooks/02_slope_domain/02_triggering_factors/infinite_slope_rainfall.ipynb)

#### Rotura

1. [Método de equilibrio global](./notebooks/02_slope_domain/03_rupture/global_equilibrium_method.ipynb)
1. [Método de equilibrio límite](./notebooks/02_slope_domain/03_rupture/limit_equilibrium_method.ipynb)
1. [Probabilidad de falla](./notebooks/02_slope_domain/03_rupture/prob_failure_infinite_slope.ipynb)

## Respaldo

Antes de la reimplementación se creó
`notebook_backups/notebooks_2026-09-11_before_refactor.tar.gz`, que contiene los
46 notebooks encontrados en el repositorio. Su SHA-256 es
`5d9dfddea2aab25905b00c471632f5165f50b01b56150cfc7787c2c157a18fa5`.

© 2022–2026 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.
