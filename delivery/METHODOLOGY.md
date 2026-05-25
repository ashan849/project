# Proyecto de Plan de Pastoreo - Metodología y Flujo de Trabajo

Este documento detalla el proceso técnico, los parámetros y la metodología utilizados para el desarrollo del plan de pastoreo.

## 1. Resumen del Proyecto
El objetivo es subdividir una finca de **4.21 hectáreas** en **3 secciones de pastoreo** (C1, C2, C3), realizando un análisis geoespacial completo que incluya topografía, vegetación y accesibilidad al agua.

## 2. Flujo de Trabajo (Workflow)

### Paso 1: Reconstrucción del Límite de la Finca
- **Fuente:** Imagen de referencia `farm_boundary_current.png`.
- **Proceso:** Se digitalizaron los vértices y se ajustó la geometría para obtener una superficie exacta de **42,127 m²**.
- **Sistema de Coordenadas:** EPSG:25830 (UTM Zona 30N).

### Paso 2: Análisis de Terreno (DEM y Pendiente)
- **Fuente de Datos:** Copernicus GLO-30 DEM (vía Microsoft Planetary Computer).
- **Procesamiento:**
  - Reproyección a EPSG:25830.
  - Remuestreo a resolución de **2 metros**.
  - Cálculo de pendiente (Slope) en grados utilizando algoritmos de gradiente.

### Paso 3: Análisis de Vegetación (Sentinel-2 NDVI)
- **Fuente de Datos:** Sentinel-2 L2A (Multiespectral).
- **Fechas Analizadas:** 12 fechas desde Septiembre 2024 hasta Agosto 2025 (según estructura de Excel).
- **Cálculo de NDVI:** `(NIR - Red) / (NIR + Red)`.
- **Resolución:** Procesado originalmente a 10m y remuestreado a **2m** para consistencia.

### Paso 4: Clasificación de Cobertura
- **Identificación de Árboles:** Se aplicó un umbral (threshold) de NDVI > 0.35 en la primavera (Abril 2025) para identificar áreas boscosas o de matorral denso.
- **Capa de Pasto:** Se generó una máscara excluyendo árboles y suelo desnudo (NDVI < 0.05).

### Paso 5: Acceso al Agua
- **Punto de Agua Propuesto:** Localizado lógicamente en la zona de acceso oeste (Coordenadas: 429250, 4221800).
- **Análisis:** Se generó un ráster de distancia euclidiana desde este punto a toda la finca.

### Paso 6: Diseño de Subdivisiones (Paddock Design)
- **Criterio:** División de la finca en 3 secciones de área idéntica (**1.404 ha cada una**).
- **Orientación:** E-O (Este-Oeste) para facilitar el acceso radial al punto de agua propuesto.

### Paso 7: Integración en Excel
- **Proceso:** Se extrajeron los datos de cada píxel de 2m x 2m (aprox. 10,000 puntos).
- **Datos por Píxel:** ID de sección, área (0.0004 ha), pendiente, distancia al agua y los 12 valores de NDVI.
- **Archivo Final:** `Plan de pastoreo.xlsx`.

## 3. Parámetros Técnicos

| Parámetro | Valor |
| :--- | :--- |
| Sistema de Referencia (CRS) | EPSG:25830 (ETRS89 / UTM zone 30N) |
| Resolución de Análisis | 2.0 metros / píxel |
| Umbral de Árboles (NDVI) | > 0.35 (Abril) |
| Umbral de Pasto (NDVI) | 0.05 - 0.35 |
| Número de Subdivisiones | 3 (C1, C2, C3) |

## 4. Archivos Entregables
- `/layers`: Capas vectoriales (finca, subdivisiones, punto de agua) en formato GeoPackage.
- `/rasters`: Mapas de pendiente, NDVI, máscaras y distancias en formato GeoTIFF.
- `Plan de pastoreo.xlsx`: Libro de cálculos actualizado con datos GIS.
- `METHODOLOGY.md`: Este documento.

---
*Nota: Todos los procesos se automatizaron mediante scripts de Python para asegurar la trazabilidad y precisión de los cálculos.*
