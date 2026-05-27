# Grazing Plan Project - Methodology and Workflow

This document provides a detailed overview of the technical process, parameters, assumptions, and logic used to develop the grazing plan, including in-depth explanations of the water infrastructure theory, paddock design logic, and the Excel calculation engine.

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

## 3. In-Depth Analysis: Water Infrastructure Logic and Theory

The placement of the proposed water point at **(429250, 4221800)** on the Western boundary is based on a combination of logistical common sense and established grazing ecology theories.

### A. Theoretical Framework: The Piosphere and Grazing Gradients
In grazing management, the area around a water source is known as a **Piosphere**. This concept describes a "grazing gradient" where the intensity of land use by livestock is highest near the water and decreases as distance increases. Livestock naturally centralize their activity around water, creating a zone of high impact near the source.

### B. The "Metabolic Cost of Walking" Assumption
A critical assumption in this model is that the **utilization rate of forage is inversely proportional to the distance from water**.
- **The 500m Rule:** In intensive systems, it is generally accepted that for every 100 meters further from water, the effective grazing capacity drops. Beyond 500-800 meters, large portions of forage may remain untouched because the metabolic cost of walking exceeds the animal's energy budget.
- **Application:** By calculating the **Euclidean distance** at a 2m resolution, the Excel model can apply a "Distance Discount Factor" to each pixel.

### C. Logic for Western Boundary Placement
1. **Accessibility:** Infrastructure (roads/pipes) typically follows boundary lines.
2. **Infrastructure Cost:** Placing the point near a potential entrance minimizes piping requirements.
3. **Rotational Efficiency:** Allows for a "Front-access" grazing design where animals have a short path back to water from any section.

## 4. Detailed Analysis: Paddock Subdivision Logic and Design

The design of the 3 paddocks (**C1, C2, C3**) follows strict geometric and agronomic principles to optimize rotational grazing management.

### A. Equal-Area Partitioning Logic
The farm was divided into three sections of exactly **1.404 hectares (14,042 m²) each**.
1. **Standardized Stocking Rates:** By keeping the areas identical, the manager can use a constant stocking rate (number of animals) across all paddocks without needing to perform complex math for each rotation.
2. **Simplified Rotation Management:** A 3-paddock system allows for a simple "one-third" rotation rule. For example, if the total forage lasts 30 days, each paddock is grazed for 10 days, providing a predictable schedule for both the manager and the ecosystem recovery.
3. **Geometric Precision:** The split points were determined using a **binary search algorithm** on the Easting coordinates, ensuring that the intersection of the division planes with the farm boundary resulted in three polygons of mathematically equal area.

### B. Vertical (East-West) Splitting Logic
The choice of vertical slices (running North-South, splitting along the E-W axis) was intentional based on the Western water point:
1. **Radial Access Pattern:** By splitting the farm vertically, every paddock (C1, C2, C3) has a "frontage" that is relatively accessible from the Western water point.
2. **Path Distance Minimization:** This layout prevents "bottlenecking." In many paddock designs, animals have to walk through one paddock to get to another (serial access), which leads to over-grazing of the "transit" paddock. The E-W split minimizes the distance livestock must travel to reach the furthest corner of any section while maintaining a logical flow.
3. **Logistical Flow:** Livestock movement is simplified; animals can be moved from the water-access side into any of the three sections with minimal stress and labor.

## 5. Excel Calculation Logic (Agronomic Model)

### Stage A: Biomass Estimation (Monteith Model)
1. **NDVI to fPAR:** NDVI is converted to the **Fraction of Photosynthetically Active Radiation (fPAR)**.
2. **PAR Absorption:** Solar radiation data is multiplied by fPAR to determine **APAR**.
3. **Dry Matter Production:** APAR is multiplied by **Radiation Use Efficiency (RUE)**, adjusted by Temperature and Vapor Pressure stress factors.

### Stage B: Usability and Feed Supply
1. **Usable Forage:** Production is modified by a **Use Factor** derived from the **Water Distance Logic** and the **Slope Analysis**.
2. **UFL Conversion:** Consumable Dry Matter is converted to **UFL (Feed Units)**.

## 6. Technical Parameters Summary

- **Primary CRS:** EPSG:25830
- **Reporting Resolution:** 2.0 meters
- **Vegetation Index:** NDVI
- **Subdivisions:** 3 Equal-Area Paddocks (1.404 ha each)
- **Water Point:** 429250, 4221800 (EPSG:25830)

## 7. Final Deliverables
- `/layers`: Vector files (finca, subdivisions, water point).
- `/rasters`: 2m GeoTIFFs (Slope, NDVI series, Distance, Masks).
- `Plan de pastoreo.xlsx`: The updated calculation engine.
- `METHODOLOGY.md`: This comprehensive guide.
