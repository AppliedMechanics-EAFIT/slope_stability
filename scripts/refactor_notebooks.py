"""Apply the editorial and compatibility standard to the published notebooks.

Run from the repository root. The script intentionally targets only notebooks
listed in ``myst.yml``; archived and case-study notebooks remain untouched.
Running it clears notebook outputs, so re-execute notebooks before publishing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NOTEBOOKS = {
    "notebooks/01_cond_factors/landslide_susceptibility.ipynb": (
        r"""# Susceptibilidad a movimientos en masa

© 2024 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/01_cond_factors/landslide_susceptibility.ipynb)

La herramienta estima la susceptibilidad mediante el método del **valor informativo** y agrega las unidades computacionales del terreno (TCU) en unidades de zonificación (TZU), siguiendo a {cite:t}`Ciurleo_etal_2016_SusceptibilityZoningShallow`. Los datos de demostración proceden del material docente de la escuela [LARAM 2023](https://www.laram.unisa.it/).""",
        r"""## Fundamentos

El valor informativo compara la densidad de movimientos en cada clase de un factor condicionante con la densidad media del inventario. Un peso positivo indica una asociación mayor que la media; el índice de susceptibilidad es la suma de los pesos de las clases presentes en cada celda. El índice expresa propensión espacial relativa, no probabilidad temporal de falla.

## Cómo usar la herramienta

1. Use `testing_data = True` para reproducir el ejemplo remoto o `False` para cargar rasters propios.
2. Identifique cuáles capas son continuas y cuáles son categóricas.
3. Compruebe CRS, extensión, origen, resolución y máscara común antes de combinar celdas.
4. Interprete el AUC junto con la cobertura espacial y valide con datos independientes cuando estén disponibles.

:::{warning}
La zonificación es un resultado dependiente del inventario, de la clasificación y de la escala. No sustituye un análisis de amenaza ni una evaluación geotécnica del sitio.
:::

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/01_cond_factors/mohr_circles_and_stress_paths.ipynb": (
        r"""# Círculos de Mohr y trayectorias de esfuerzos

© 2022 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/01_cond_factors/mohr_circles_and_stress_paths.ipynb)""",
        r"""## Fundamentos

Para un estado plano, el círculo de Mohr tiene centro $c=(\sigma_{xx}+\sigma_{yy})/2$ y radio $r=\sqrt{[(\sigma_{xx}-\sigma_{yy})/2]^2+\tau_{xy}^2}$. Sus intersecciones con el eje normal son los esfuerzos principales. Las variables $(s,t)$ y $(p,q)$ permiten representar la evolución del estado mediante trayectorias de esfuerzos.

## Cómo usar la herramienta

1. Modifique las componentes del tensor y la convención de signos de forma consistente.
2. Active el polo, el plano inclinado o la envolvente de resistencia según el objetivo.
3. Compare varios estados con las herramientas de círculos y trayectorias.
4. Verifique unidades y recuerde que el ángulo sobre el círculo es el doble del giro físico.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/01_cond_factors/mohr_circles_for_strains.ipynb": (
        r"""# Círculo de Mohr para deformaciones

© 2022 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/01_cond_factors/mohr_circles_for_strains.ipynb)

La formulación sigue el capítulo 1 de *Mohr Circles, Stress Paths and Geotechnics* de {cite:t}`Parry2014_MohrCircles`.""",
        r"""## Fundamentos

El círculo de deformaciones representa deformación normal en el eje horizontal y la mitad de la deformación cortante ingenieril en el vertical. El centro corresponde a la mitad de la deformación volumétrica bidimensional y el radio a $\gamma_{max}/2$. Las líneas de cero extensión ayudan a interpretar orientaciones potenciales de bandas de corte.

## Cómo usar la herramienta

1. Ingrese deformaciones con una única convención de signos.
2. Active el polo y el plano para transformar el estado a otra orientación.
3. Use incrementos de deformación para estudiar líneas de cero extensión.
4. Evite interpretar la construcción cuando todas las deformaciones son iguales, pues el radio es nulo.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/01_cond_factors/spt_processing.ipynb": (
        r"""# Procesamiento del ensayo SPT

© 2023 Daniel F. Ruiz, Exneyder A. Montoya-Araque y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/01_cond_factors/spt_processing.ipynb)

La herramienta aplica el procedimiento de {cite:t}`Gonzalez1999_ParametrosSPT` para estimar parámetros de resistencia a partir del ensayo de penetración estándar ([documento en español](https://www.scg.org.co/wp-content/uploads/2021/08/ESTIMATIVOS-DE-PARAMETROS-DE-RESISTENCIA-CON-SPT-1.pdf)).""",
        r"""## Fundamentos

El número de golpes medido debe corregirse por energía, diámetro de perforación, longitud de varillas, muestreador y nivel de esfuerzo efectivo. Las correlaciones posteriores son empíricas y su dispersión puede ser significativa; el perfil estratigráfico y la posición del nivel freático controlan la corrección por sobrecarga.

## Cómo usar la herramienta

1. Use los datos de prueba o cargue una hoja de cálculo con las columnas del ejemplo.
2. Defina profundidades de estratos, pesos unitarios, nivel freático, diámetro y energía de campo.
3. Ejecute el procesamiento y revise primero la tabla completada.
4. Contraste las correlaciones con el tipo de suelo y con información local.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/01_cond_factors/strength_envelopes.ipynb": (
        r"""# Envolventes de resistencia al corte

© 2022 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/01_cond_factors/strength_envelopes.ipynb)

La implementación sigue el análisis de fallas superficiales en taludes de suelo presentado por {cite:t}`Lade_2010_MechanicsSurficialFailure`.""",
        r"""## Fundamentos

La envolvente de Mohr–Coulomb aproxima la resistencia mediante $\tau_f=c'+\sigma'_n\tan\phi'$. En materiales no lineales, una única pareja $(c',\phi')$ depende del intervalo de esfuerzos usado para ajustar la recta; por ello conviene comparar la envolvente curva y sus aproximaciones secantes o tangentes.

## Cómo usar la herramienta

1. Defina los parámetros del modelo y el intervalo de esfuerzo normal pertinente.
2. Compare la envolvente no lineal con los ajustes lineales mostrados.
3. Use parámetros efectivos o totales de manera consistente con el problema.
4. No extrapole la envolvente fuera del intervalo calibrado.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/02_trigg_factors/infinite_slope_earthquake.ipynb": (
        r"""# Sismo como factor detonante de un talud infinito

© 2024 Daniel F. Ruiz, Exneyder A. Montoya-Araque y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/02_trigg_factors/infinite_slope_earthquake.ipynb)

La herramienta usa `pyNewmarkDisp`, desarrollado por {cite:t}`Montoya-Araque_etal_2024_OpensourceApplicationSoftware`, y el método clásico del bloque rígido deslizante de {cite:t}`Newmark_1965_EffectsEarthquakesDams`.""",
        r"""## Fundamentos

El mecanismo de talud infinito permite obtener el factor de seguridad estático y el coeficiente sísmico crítico $k_y$. En el método de Newmark el bloque acumula desplazamiento permanente cuando la aceleración que actúa en la dirección desfavorable supera la aceleración de fluencia $k_y g$.

## Cómo usar la herramienta

1. Defina geometría, nivel freático y parámetros resistentes con unidades consistentes.
2. Use el registro de prueba o cargue un archivo de dos columnas: tiempo y aceleración.
3. Indique correctamente si la aceleración está en $g$, m/s² o cm/s².
4. Compare el análisis estático, pseudoestático y el desplazamiento de Newmark.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/02_trigg_factors/infinite_slope_earthquake_spatial.ipynb": (
        r"""# Sismo como factor detonante en un dominio espacial

© 2024 Daniel F. Ruiz, Exneyder A. Montoya-Araque y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/02_trigg_factors/infinite_slope_earthquake_spatial.ipynb)

Se aplica `pyNewmarkDisp` ({cite:t}`Montoya-Araque_etal_2024_OpensourceApplicationSoftware`) a cada celda de un dominio, con base en el método de {cite:t}`Newmark_1965_EffectsEarthquakesDams`.""",
        r"""## Fundamentos

Cada celda se modela como un talud infinito con propiedades asignadas por zona. El resultado espacial solo es válido si elevación, pendiente, profundidad, nivel freático y zonas representan exactamente la misma malla. Las celdas sin datos se excluyen de todos los cálculos mediante una máscara común.

## Cómo usar la herramienta

1. Reproduzca primero el ejemplo con los rasters ASCII remotos.
2. Para otro caso, alinee CRS, extensión, origen y resolución antes de ejecutar el modelo.
3. Defina una tupla $(\phi',c',\gamma)$ para cada identificador de zona.
4. Verifique una celda con la integración temporal antes de interpretar los mapas.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/02_trigg_factors/infinite_slope_rainfall.ipynb": (
        r"""# Lluvia como factor detonante de un talud infinito

© 2024 Daniel F. Ruiz, Exneyder A. Montoya-Araque y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/02_trigg_factors/infinite_slope_rainfall.ipynb)

El notebook ejecuta `TRIGRS` (*Transient Rainfall Infiltration and Grid-Based Regional Slope-Stability Analysis*), desarrollado por {cite:t}`Baum_etal_2002_TRIGRSFortranProgram` y {cite:t}`Baum_etal_2008_TRIGRSFortranProgram`, y paralelizado por {cite:t}`Alvioli_Baum_2016_ParallelizationTRIGRSModel`.""",
        r"""## Fundamentos

La infiltración transitoria modifica la presión de poros y, con ella, el esfuerzo efectivo. TRIGRS aproxima esta respuesta mediante soluciones de difusión vertical para condiciones saturadas o no saturadas y evalúa el factor de seguridad con un mecanismo de talud infinito.

## Cómo usar la herramienta

1. Edite intensidad y duración de lluvia, profundidad, nivel freático, pendiente y parámetros de la zona.
2. No cambie los campos marcados con 🛇 salvo que conozca el formato de entrada de TRIGRS.
3. Ejecute TopoIndex y TRIGRS y revise el registro antes de interpretar los perfiles.
4. Confirme unidades, condiciones iniciales y parámetros hidráulicos con información del sitio.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/02_trigg_factors/infinite_slope_rainfall_spatial.ipynb": (
        r"""# Lluvia como factor detonante en un dominio espacial

© 2024 Daniel F. Ruiz, Exneyder A. Montoya-Araque y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/02_trigg_factors/infinite_slope_rainfall_spatial.ipynb)

El notebook ejecuta `TRIGRS`, desarrollado por {cite:t}`Baum_etal_2002_TRIGRSFortranProgram` y {cite:t}`Baum_etal_2008_TRIGRSFortranProgram`, y paralelizado por {cite:t}`Alvioli_Baum_2016_ParallelizationTRIGRSModel`.""",
        r"""## Fundamentos

TRIGRS resuelve la infiltración vertical transitoria y el factor de seguridad para cada celda. La consistencia de la malla es parte del modelo: elevación, pendiente, dirección de flujo, zonas y profundidades deben compartir CRS, extensión, origen, resolución y `nodata`. Las variables continuas pueden remuestrearse; las categorías y direcciones requieren vecino más cercano o recálculo.

## Cómo usar la herramienta

1. Use `testing_data = True` para reproducir el caso remoto.
2. Para datos propios, cargue el DEM y las capas solicitadas; el DEM define la malla objetivo.
3. Revise la máscara común y los mapas de entrada antes de ejecutar TopoIndex.
4. Compruebe el registro de TRIGRS y contraste una celda de los mapas con su perfil vertical.

:::{warning}
El remuestreo no corrige errores de datum, unidades ni calidad del DEM. La dirección de flujo debe derivarse de la elevación ya acondicionada sobre la malla final.
:::

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/03_rupture/global_equilibrium_method.ipynb": (
        r"""# Método de equilibrio global

© 2022 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/03_rupture/global_equilibrium_method.ipynb)""",
        r"""## Fundamentos

La geometría de una masa potencialmente inestable puede describirse mediante la intersección del terreno con una superficie circular. El área, el centroide y la longitud del arco son cantidades básicas para formular balances globales de fuerzas y momentos.

## Cómo usar la herramienta

1. Defina altura e inclinación del talud.
2. Ubique el centro y el radio de la superficie circular.
3. Verifique que la superficie intercepte el perfil y produzca una masa físicamente válida.
4. Use la figura interactiva para estudiar la sensibilidad geométrica.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/03_rupture/limit_equilibrium_method.ipynb": (
        r"""# Método de equilibrio límite

© 2022 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/03_rupture/limit_equilibrium_method.ipynb)

La herramienta ejecuta `pyCSS`, asociado con {cite:t}`SuarezBurgoa_MontoyaAraque_2016_pyCSS`. También están disponibles la [versión original](https://github.com/eamontoyaa/pyCSS/tree/v0.0.9) y el [manual en español](https://github.com/eamontoyaa/pyCSS/tree/master/other_files).

![Variables geométricas del talud](https://raw.githubusercontent.com/eamontoyaa/pyCSS/master/other_files/figures/slope_geometry.svg)""",
        r"""## Fundamentos

Los métodos de dovelas satisfacen el equilibrio de una masa delimitada por el terreno y una superficie de falla. El factor de seguridad moviliza la resistencia al corte disponible; una búsqueda sobre múltiples círculos aproxima el mínimo dentro del espacio explorado, no necesariamente el mínimo global.

## Cómo usar la herramienta

1. Defina geometría, nivel freático y materiales con unidades coherentes.
2. Evalúe primero una superficie y revise su geometría.
3. Configure densidad y límites de búsqueda antes del análisis múltiple.
4. Compruebe convergencia y amplíe el dominio de búsqueda si el mínimo queda en un borde.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/03_rupture/prob_failure_infinite_slope.ipynb": (
        r"""# Probabilidad de falla mediante Monte Carlo para un talud infinito

© 2024 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/03_rupture/prob_failure_infinite_slope.ipynb)""",
        r"""## Fundamentos

La simulación de Monte Carlo propaga distribuciones de las variables de entrada a una muestra del factor de seguridad. La probabilidad de falla se estima como la fracción de realizaciones con $FS<1$. La estabilidad de la media y de la desviación estándar no garantiza por sí sola la convergencia de una probabilidad de cola.

## Cómo usar la herramienta

1. Defina valores medios, intervalos o coeficientes de variación con soporte físico.
2. Seleccione distribuciones compatibles con cada variable y conserve semillas para reproducibilidad.
3. Aumente el tamaño de muestra y revise la convergencia de $FS$ y $P_f$.
4. Evalúe correlaciones entre variables cuando el caso real no permita tratarlas como independientes.

## Módulos requeridos y configuración de figuras""",
    ),
    "notebooks/04_propagation/runout_semiempirical.ipynb": (
        r"""# Simulación semiempírica de propagación de movimientos en masa

© 2026 Exneyder A. Montoya-Araque, Daniel F. Ruiz y Universidad EAFIT.

Este notebook puede ejecutarse en línea → [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AppliedMechanics-EAFIT/slope_stability/blob/main/notebooks/04_propagation/runout_semiempirical.ipynb)

La herramienta aplica `Flow-Py v1.0`, propuesto por {cite:t}`DAmboise_etal_2022_FlowPyV10Customizable`, para estimar alcance e intensidad geométrica de flujos gravitacionales.""",
        r"""## Fundamentos

Flow-Py propaga masa desde celdas fuente sobre un DEM mediante reglas semiempíricas de alcance y divergencia. El ángulo de alcance controla la distancia máxima, el exponente controla la dispersión lateral y $Z_\delta$ representa una altura cinética geométrica. Los parámetros requieren calibración para el tipo de proceso y el sitio.

## Cómo usar la herramienta

1. Use el DEM de prueba o cargue un GeoTIFF proyectado con unidades horizontales y verticales compatibles.
2. Defina fuentes dentro de la extensión y confirme visualmente las celdas activadas.
3. Ejecute varios valores de ángulo, exponente y umbral de flujo.
4. Exporte el resultado conservando exactamente CRS, transformación, resolución y máscara del DEM.

## Módulos requeridos y configuración de figuras""",
    ),
}


STYLE = """# Figure style shared by every chapter
plt.style.use("default")
AXIS_LINEWIDTH = 1.25
PLOT_LINEWIDTH = 1.75
mpl.rcParams.update(
    {
        # Some teaching libraries still call ``Figure.tight_layout()`` after
        # creating a colorbar. Matplotlib 3.10 cannot switch from constrained
        # layout at that point, so keep one compatible layout engine globally.
        "figure.constrained_layout.use": False,
        "figure.figsize": (6.4, 4.2),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.family": "DejaVu Serif",
        "font.serif": ["DejaVu Serif"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.linewidth": AXIS_LINEWIDTH,
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "lines.linewidth": PLOT_LINEWIDTH,
        "lines.markersize": 6,
        "grid.color": "0.75",
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "legend.frameon": False,
        "mathtext.fontset": "dejavuserif",
        "xtick.major.width": AXIS_LINEWIDTH,
        "ytick.major.width": AXIS_LINEWIDTH,
        "text.usetex": False,
    }
)
"""


MARKDOWN_REPLACEMENTS = {
    "## Reading the input data": "## Lectura de datos de entrada",
    "### Loading testing data": "### Carga de datos de prueba",
    "### Uploading the raster files of conditioning factors": "### Carga de rasters de factores condicionantes",
    "### Uploading the raster files of landslides": "### Carga del raster del inventario",
    "## Percentile class for each independent variable": "## Clase percentil de cada variable independiente",
    "The independent variables are classified according to a quantile criterion employing 8 classes": "Las variables independientes continuas se clasifican por cuantiles en ocho clases.",
    "TCUs belonging to the class $j$ of the independent variable $V_i$": "TCU pertenecientes a la clase $j$ de la variable independiente $V_i$",
    "Number of TCUs with landslides belonging to the class $j$ of the independent variable $V_i$": "Número de TCU con movimientos en masa en la clase $j$ de la variable independiente $V_i$",
    "Number of TCUs without landslides belonging to the class $j$ of the independent variable $V_i$": "Número de TCU sin movimientos en masa en la clase $j$ de la variable independiente $V_i$",
    "Weight of the class $j$ of the independent variable $V_i$": "Peso de la clase $j$ de la variable independiente $V_i$",
    "Density of landslides within class $j$ of the independent variable $V_i$": "Densidad de movimientos en la clase $j$ de la variable independiente $V_i$",
    "Average density of landslides within the test area": "Densidad media de movimientos en el área de estudio",
    "statistical indicator to assess the discriminant capability": "indicador estadístico de la capacidad discriminante",
    "## Visualize the spatial distribution of the susceptibility index": "## Distribución espacial del índice de susceptibilidad",
    "### Raw results for terrain computational units (TCU)": "### Resultado por unidades computacionales del terreno (TCU)",
    "### Processed results for larger terrain zoning unit (TZU)": "### Resultado agregado por unidades de zonificación del terreno (TZU)",
    "The focal statistics used here is a 2D Gaussian filter with standard deviation $\\sigma$ used to control the degree of smoothness.": "La estadística focal usa un filtro gaussiano bidimensional cuya desviación estándar $\\sigma$ controla el grado de suavizado.",
    "To visualize the landslide boundaries over the map, uncomment the code in the following cell.": "Para superponer los límites del inventario, active el código comentado en la celda siguiente.",
    "### Export results to raster file": "### Exportación de resultados a raster",
    "To save the susceptibility index map to a raster file, set the ``want2save`` variable in the next cell as `True`.": "Active la exportación en la celda siguiente para guardar el índice de susceptibilidad como raster.",
    "## Performance validation of the susceptibility model": "## Evaluación del desempeño del modelo",
    "## Landslide susceptibility zonation": "## Zonificación de la susceptibilidad",
    "## Functions": "## Funciones",
    "## Basic example": "## Ejemplo básico",
    "# Basic example of the Mohr's circle": "## Ejemplo básico del círculo de Mohr",
    "# Ejemplo básico del Circulo de Mohr": "## Ejemplo básico del círculo de Mohr",
    "# Tool 01": "## Herramienta 1",
    "# Tool 02": "## Herramienta 2",
    "# Tool 03": "## Herramienta 3",
    "Stresses state for the same stage at different points.": "Estados de esfuerzo de una misma etapa en distintos puntos.",
    "Stresses state for at a point during different stages.": "Estados de esfuerzo de un punto durante distintas etapas.",
    "Stress path": "Trayectoria de esfuerzos",
    "# Lineas de cero extensión en el círculo de Mohr": "## Líneas de cero extensión en el círculo de Mohr",
    "## Example": "## Ejemplo",
    "### Reading the input data": "### Lectura de datos de entrada",
    "### Processing the data and completing the table": "### Procesamiento y terminación de la tabla",
    "## Plotting the processed data": "## Visualización de los datos procesados",
    "## Creating directories": "## Creación de directorios",
    "## Loading executables and input files": "## Descarga de ejecutables y archivos de entrada",
    "## Running a case": "## Ejecución de un caso",
    "## Running the TRIGRS model for a one-cell spatial domain": "## Ejecución de TRIGRS en un dominio de una celda",
    "## Running the TRIGRS model in a spatial domain": "## Ejecución de TRIGRS en un dominio espacial",
    "### General inputs": "### Entradas generales",
    "### Units conversion": "### Conversión de unidades",
    "### TRIGRS inputs": "### Entradas de TRIGRS",
    "### Creating `.asc` files": "### Creación de archivos `.asc`",
    "### Runnig TopoIndex and TRIGRS": "### Ejecución de TopoIndex y TRIGRS",
    "## Output to dataframe": "## Organización de resultados en un `DataFrame`",
    "## Verification of FS and head pressure at a point": "## Verificación de FS y presión de poros en un punto",
    "## Plotting results at a point": "## Visualización de resultados en un punto",
    "## Loading spatial files and creating `.asc` files": "## Carga de archivos espaciales y creación de `.asc`",
    "## Visualizing spatial inputs (conditioning factors)": "## Revisión visual de las entradas espaciales",
    "### Visualizing spatial outputs of *FS*": "### Distribución espacial de *FS*",
    "### Visualizing spatial outputs of $\\psi$": "### Distribución espacial de $\\psi$",
    "### Inputs (conditioning factors)": "### Entradas: factores condicionantes",
    "### Inputs (triggering factor - Earthquake record)": "### Entrada detonante: registro sísmico",
    "### Static factor of safety": "### Factor de seguridad estático",
    "### Critical seismic coefficient": "### Coeficiente sísmico crítico",
    "### Pseudo-static factor of safety": "### Factor de seguridad pseudoestático",
    ", when $k_\\mathrm{s}$ is 70% of $k_\\mathrm{y}$": ", para $k_\\mathrm{s}=0.7k_\\mathrm{y}$",
    ", when $k_\\mathrm{s}$ is 50% of PGA": ", para $k_\\mathrm{s}=0.5\\,PGA$",
    "### Calculating and plotting the spatial distribution of $\\mathrm{FS}_\\mathrm{static}$": "### Distribución espacial de $\\mathrm{FS}_\\mathrm{static}$",
    "### Calculating and plotting the spatial distribution of $k_\\mathrm{y}$": "### Distribución espacial de $k_\\mathrm{y}$",
    "### Calculating and plotting the spatial distribution of $\\mathrm{FS}_\\mathrm{pseudostatic}$ when $k_\\mathrm{s}$ is 40% of $k_\\mathrm{y}$": "### Distribución espacial de $\\mathrm{FS}_\\mathrm{pseudostatic}$ para $k_\\mathrm{s}=0.4k_\\mathrm{y}$",
    "### Calculating and plotting the spatial distribution of $u_\\mathrm{p}$": "### Distribución espacial de $u_\\mathrm{p}$",
    "### Cálculo y visualización the spatial distribution of $\\mathrm{FS}_\\mathrm{static}$": "### Distribución espacial de $\\mathrm{FS}_\\mathrm{static}$",
    "### Cálculo y visualización the spatial distribution of $k_\\mathrm{y}$": "### Distribución espacial de $k_\\mathrm{y}$",
    "### Cálculo y visualización the spatial distribution of $\\mathrm{FS}_\\mathrm{pseudostatic}$ when $k_\\mathrm{s}$ is 40% of $k_\\mathrm{y}$": "### Distribución espacial de $\\mathrm{FS}_\\mathrm{pseudostatic}$ para $k_\\mathrm{s}=0.4k_\\mathrm{y}$",
    "### Cálculo y visualización the spatial distribution of $u_\\mathrm{p}$": "### Distribución espacial de $u_\\mathrm{p}$",
    "### Loading earthquake record and spatial data": "### Carga del registro sísmico y de los datos espaciales",
    "### Non-spatial inputs": "### Entradas no espaciales",
    "### Plotting the Newmark method at a specific location": "### Verificación del método de Newmark en una ubicación",
    "## Comparing three signals with $a_\\mathrm{max} = 5.5 \\pm 0.1$ $\\mathrm{m/s}^2$": "## Comparación de tres señales con $a_\\mathrm{max}=5.5 \\pm 0.1$ $\\mathrm{m/s}^2$",
    "## Comparación de tres señales with $a_\\mathrm{max} = 5.5 \\pm 0.1$ $\\mathrm{m/s}^2$": "## Comparación de tres señales con $a_\\mathrm{max}=5.5 \\pm 0.1$ $\\mathrm{m/s}^2$",
    "## Area and centroid of a mass sliding along a circular surface": "## Área y centroide de una masa sobre una superficie circular",
    "### Funtions": "### Funciones",
    "### Static figure": "### Figura estática",
    "### Interactive figure": "### Figura interactiva",
    "## Inputs for analyzing one circular failure surface": "## Entradas para una superficie circular",
    "### Poject data": "### Datos del proyecto",
    "### Slope geometry": "### Geometría del talud",
    "### Watertable": "### Nivel freático",
    "### Materials properties": "### Propiedades de los materiales",
    "### Advanced inputs": "### Entradas avanzadas",
    "## Assessment of a single potential circular failure surface": "## Evaluación de una superficie circular",
    "### Geomoetry of the circular failure surface": "### Geometría de la superficie circular",
    "### Running stability analysis": "### Ejecución del análisis de estabilidad",
    "## Assessment of a multiple potential circular failure surface for getting the minimum": "## Búsqueda del factor de seguridad mínimo entre múltiples superficies circulares",
    "### Additional inputs to control how multiple surfaces are generated and evaluated": "### Entradas adicionales para generar y evaluar superficies",
    "### Inputs": "### Entradas",
    "### Generating random samples": "### Generación de muestras aleatorias",
    "### Samples for the probabilistic analysis": "### Muestras del análisis probabilista",
    "### Calculating FS for all the realizations": "### Cálculo de FS para todas las realizaciones",
    "### Plotting results": "### Visualización de resultados",
    "## Input data": "## Datos de entrada",
    "### Digital elevation model": "### Modelo digital de elevación",
    "### Release areas and visualization": "### Áreas fuente y visualización",
    "### Saving the release areas into a tif file": "### Exportación de las áreas fuente a GeoTIFF",
    "## Runing a case": "## Ejecución de un caso",
    "### Saving the Zmax output into a tif file": "### Exportación de $Z_\\delta$ a GeoTIFF",
}


def replace_style(source: str) -> str:
    standardized = re.compile(
        r"(?ms)^# Figure style shared by every chapter\n.*?^\)\n?"
    )
    if standardized.search(source):
        return standardized.sub(STYLE, source, count=1)

    pattern = re.compile(
        r"(?ms)(?:# Figures setup\n)?# %matplotlib widget\n"
        r"\s*(?:%matplotlib inline\n)?(?:plt\.style\.use\([^\n]+\)\n)?"
        r"mpl\.rcParams\.update\(\{.*?^\}\)\n?"
    )
    updated, count = pattern.subn(STYLE, source, count=1)
    if count == 0:
        raise RuntimeError("Figure style block not found.")
    return updated


def translate_markdown(source: str) -> str:
    for old, new in MARKDOWN_REPLACEMENTS.items():
        source = source.replace(old, new)
    source = source.replace(
        "Do not edit those parameters with the → 🛇 ← symbol.",
        "No edite los parámetros marcados con el símbolo → 🛇 ←.",
    )
    source = source.replace(
        "If working on Google Colab, set the `testing_data` variable in the following cell as `False`. Then you will be asked to upload your own raster files.",
        "En Google Colab, use `testing_data = False` para cargar sus propios archivos raster con el selector que aparecerá.",
    )
    source = re.sub(r"(?m)^#+ Funciones$", "## Funciones", source)
    source = source.replace("Susceptibility index", "Índice de susceptibilidad")
    source = source.replace(" of $W_i$", " de $W_i$")
    return source


def update_code(source: str) -> str:
    # Colab already includes rasterio. Install only optional course packages,
    # using the notebook kernel interpreter and the project's tested versions.
    source = source.replace("    run('pip install rasterio', shell=True);\n", "")
    for package, version in {
        "geotoolbox": "0.1.0",
        "pycss-lem": "0.1.0",
        "pynewmarkdisp": "0.1.0",
        "pysheds": "0.5",
    }.items():
        for runner in ("run", "subprocess.run"):
            source = source.replace(
                f"{runner}('pip install {package}', shell=True);",
                f'{runner}([sys.executable, "-m", "pip", "install", "{package}=={version}"], check=True)',
            )
    if "sys.executable" in source and "import sys\n" not in source:
        source = "import sys\n" + source
    source = source.replace("%matplotlib inline\n", "")
    source = source.replace("np.trapz(", "np.trapezoid(")
    source = source.replace("random_rample_normal", "random_sample_normal")
    source = source.replace(".set_linewidth(1.5)", ".set_linewidth(AXIS_LINEWIDTH)")
    source = source.replace(".set_linewidth(1.25)", ".set_linewidth(AXIS_LINEWIDTH)")
    source = source.replace("tick_params(width=1.5)", "tick_params(width=AXIS_LINEWIDTH)")
    source = source.replace("Running on CoLab.", "Running in Google Colab.")
    source = source.replace("Running on CoLab", "Running in Google Colab")
    source = source.replace("i < len(y_coord) and y_coord[i+1]", "i + 1 < len(y_coord) and y_coord[i+1]")
    source = source.replace("wt_depth >= mat_depths[-1] or wt_depth is None", "wt_depth is None or wt_depth >= mat_depths[-1]")
    # Escape backslashes that Python treats as invalid string escapes in LaTeX
    # labels and regular expressions, while preserving valid escapes such as \n.
    source = re.sub(
        r"(?<!\\)\\([^\\abfnrtv'\"01234567xuUN\n])",
        r"\\\\\1",
        source,
    )
    return source


def refactor(path: Path, header: str, introduction: str) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"][0]["source"] = header.splitlines(keepends=True)
    notebook["cells"][1]["source"] = introduction.splitlines(keepends=True)

    style_applied = False
    for cell in notebook["cells"]:
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "markdown":
            source = translate_markdown(source)
        elif cell["cell_type"] == "code":
            source = update_code(source)
            if not style_applied and "mpl.rcParams.update" in source:
                if "# Figure style shared by every chapter" not in source:
                    source = replace_style(source)
                style_applied = True
            cell["execution_count"] = None
            cell["outputs"] = []
        cell["source"] = source.splitlines(keepends=True)

    if not style_applied:
        raise RuntimeError(f"No style block updated in {path}")
    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for relative_path, (header, introduction) in NOTEBOOKS.items():
        refactor(ROOT / relative_path, header, introduction)
        print(f"Updated {relative_path}")


if __name__ == "__main__":
    main()
