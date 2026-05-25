# Grazing Plan Project - Methodology and Workflow

This document provides a detailed overview of the technical process, parameters, assumptions, and logic used to develop the grazing plan.

## 1. Project Summary
The objective was to subdivide a **4.21-hectare** farm into **3 grazing sections** (C1, C2, C3) and perform a comprehensive GIS analysis including terrain, vegetation dynamics, and water accessibility to support professional grazing calculations.

## 2. Technical Workflow

### Step 1: Boundary Reconstruction
- **Source:** Reference image `farm_boundary_current.png`.
- **Process:** Vertices were digitized and the resulting geometry was scaled to match the client's specified area of **42,127 m²**.
- **Coordinate Reference System (CRS):** EPSG:25830 (UTM Zone 30N).

### Step 2: Terrain Analysis
- **Data Source:** Copernicus GLO-30 DEM.
- **Processing:** Reprojected to EPSG:25830 and resampled to **2-meter resolution**.
- **Outputs:** Slope (degrees) and Hillshade layers were generated to evaluate land suitability.

### Step 3: Vegetation Monitoring (Sentinel-2 NDVI)
- **Data Source:** Sentinel-2 L2A (Level-2A Bottom-of-Atmosphere reflectance).
- **Dates:** 12 specific dates from Sept 2024 to Aug 2025 were analyzed to capture seasonality.
- **NDVI Calculation:** `(NIR - Red) / (NIR + Red)`.
- **Resolution:** Resampled to **2m** for high-density reporting.

### Step 4: Land Cover Classification
- **Tree Identification:** An NDVI threshold of **> 0.35** during the spring peak (April 2025) was used to identify woody vegetation.
- **Grass Layer:** A "Grass Pixel Layer" was created by masking out trees and non-vegetated areas (NDVI < 0.05).

### Step 5: Water Access Analysis
- **Water Point Logic:** A logical water infrastructure point was proposed at the Western boundary (Coordinates: 429250, 4221800) based on typical farm access patterns.
- **Analysis:** A Euclidean distance raster was generated from this point across the entire farm.

### Step 6: Paddock Subdivision Design
- **Subdivision Logic:** The farm was partitioned into 3 sections of exactly equal area (**1.404 ha each**).
- **Partitioning:** Vertical (East-West) splitting was used to provide balanced access to the proposed water source and simplify livestock movement.

### Step 7: Excel Data Integration
- **Data Population:** Pixel-level data (approx. 10,000 points at 2m resolution) was extracted.
- **Fields:** Section ID, area (0.0004 ha), slope, distance-to-water, and 12-month NDVI time-series.
- **File:** `Plan de pastoreo.xlsx`.

## 3. Assumptions and Logic

| Component | Assumption / Logic |
| :--- | :--- |
| **Area Precision** | The total area was fixed at **42,127 m²** as per the client brief. Boundary geometry was adjusted to maintain this exact footprint. |
| **Spatial Resolution** | Analysis was performed at **2m resolution** (resampled from 10m). This was done to provide ~2,500 data points per hectare, ensuring the high-density data required for professional grazing spreadsheets. |
| **Tree Classification** | NDVI values above **0.35** in peak spring are assumed to represent perennial trees/shrubs. These areas are excluded from "usable grass" calculations. |
| **Usable Pasture** | NDVI values between **0.05 and 0.35** are assumed to be usable grass/pasture. Values below 0.05 are treated as bare soil, rocks, or roads. |
| **Water Location** | In the absence of a client-provided water layer, the point was placed at the **Western boundary**. This assumes the most likely location for main water lines or road-side access. |
| **Subdivision Equality** | Subdivisions were designed for **equal area** rather than equal forage. This provides a stable baseline for rotational grazing management. |
| **Slope Impact** | Slope is calculated at the pixel level to allow the client to apply "usability" reduction factors for steep terrain within the Excel workbook. |

## 4. Technical Parameters Summary

- **Primary CRS:** EPSG:25830
- **Reporting Resolution:** 2.0 meters
- **Vegetation Index:** NDVI (Normalized Difference Vegetation Index)
- **Subdivisions:** 3 Paddocks (C1, C2, C3)
- **Total Area:** 4.2127 Hectares

## 5. Final Deliverables
- `/layers`: Vector files (finca, subdivisions, water point) in GeoPackage format.
- `/rasters`: Slope, NDVI (12 dates), Masks, and Distance-to-water in GeoTIFF format.
- `Plan de pastoreo.xlsx`: Updated calculation workbook.
- `METHODOLOGY.md`: Technical documentation.
