# Grazing Plan Project - Methodology and Workflow

This document provides a detailed overview of the technical process, parameters, assumptions, and logic used to develop the grazing plan, including a comprehensive explanation of the Excel calculation engine.

## 1. Project Summary
The objective was to subdivide a **4.21-hectare** farm into **3 grazing sections** (C1, C2, C3) and perform a comprehensive GIS analysis to feed an agronomic model that determines the carrying capacity and grazing schedule of the land.

## 2. Technical GIS Workflow

### Step 1: Boundary Reconstruction
- **Process:** Vertices were digitized from reference imagery and scaled to match the target area of **42,127 m²**.
- **CRS:** EPSG:25830.

### Step 2: Terrain and Hydrology
- **Slope:** Calculated from a 2m resampled Copernicus DEM to assess land accessibility.
- **Water Access:** Euclidean distance calculated from a proposed Western access point.

### Step 3: Vegetation Monitoring (NDVI)
- **NDVI Calculation:** `(NIR - Red) / (NIR + Red)` using Sentinel-2 L2A imagery.
- **Time-series:** 12 monthly scenes were processed to capture the full phenological cycle.

### Step 4: Land Cover Classification
- **Logic:** NDVI > 0.35 (Spring) = Trees/Shrubs; 0.05 < NDVI < 0.35 = Grass/Pasture.
- **Masking:** Only "Grass" pixels are used in the final production calculations.

## 3. Excel Calculation Logic (Agronomic Model)

The workbook transforms raw satellite data into grazing days through a multi-stage bio-physical model:

### Stage A: Biomass Estimation (Monteith Model)
1. **NDVI to fPAR:** The NDVI data from the GIS analysis is converted to the **Fraction of Photosynthetically Active Radiation (fPAR)**.
   - *Logic:* NDVI is a proxy for the greenness and density of the canopy, which directly correlates with how much light the plants can absorb.
2. **PAR Absorption:** Global solar radiation data (Rad) is multiplied by fPAR to determine the **Absorbed Photosynthetically Active Radiation (APAR)**.
3. **Dry Matter Production (kg MS/ha):** APAR is multiplied by a **Radiation Use Efficiency (RUE)** factor, adjusted by environmental stress factors (Temperature, Vapor Pressure Deficit).
   - *Formula:* `Production = APAR * RUE * Stress_Factors`.

### Stage B: Usability and Feed Supply
1. **Usable Forage:** Not all produced biomass is consumable. A **Harvest Index / Use Factor** is applied based on the slope and distance to water.
   - *Slope Factor:* Steep areas reduce the "Usability" of the grass.
   - *Distance Factor:* Forage further from water points has lower utilization rates.
2. **UFL Conversion:** Dry Matter (kg MS) is converted to **Unité Fourragère Laitière (UFL)**, the standard energy unit for livestock feed evaluation.

### Stage C: Animal Requirements and Grazing Plan
1. **Necesidades (Needs):** Animal energy requirements are calculated based on weight, gestation status, and activity.
2. **Pastoreo (Grazing):** The final sheet matches the daily supply (from the pasture) with the daily demand (from the herd).
   - *Rotational Logic:* The model tracks the depletion of energy in each section (C1, C2, C3) and determines when the herd must move to the next paddock.

## 4. Key Assumptions and Parameters

| Component | Logic / Parameter |
| :--- | :--- |
| **Spatial Scale** | **2m resolution** to capture micro-topography and precise paddock boundaries. |
| **Tree Masking** | Excludes non-forage biomass (trees) to avoid overestimating carrying capacity. |
| **RUE Factor** | Assumed standard for Mediterranean pastures, modified by monthly climate data. |
| **Water Influence** | Utilization decreases linearly as distance to the water point increases. |
| **Animal Unit** | Based on livestock assumptions embedded in the `Necesidades` sheet. |

## 5. Final Deliverables
- `/layers`: GeoPackage vector files (Boundary, Subdivisions, Water).
- `/rasters`: 2m GeoTIFFs (Slope, NDVI series, Distance, Masks).
- `Plan de pastoreo.xlsx`: The complete agronomic calculation engine.
- `METHODOLOGY.md`: This technical guide.
