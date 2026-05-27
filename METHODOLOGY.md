# Grazing Plan Project - Methodology and Workflow

This document provides a detailed overview of the technical process, parameters, assumptions, and logic used to develop the grazing plan, including an in-depth explanation of the water infrastructure theory and the Excel calculation engine.

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
In grazing management, the area around a water source is known as a **Piosphere**. This concept describes a "grazing gradient" where the intensity of land use by livestock is highest near the water and decreases as distance increases.
1. **The Piosphere Effect:** Livestock naturally centralize their activity around water. This creates a zone of high impact (trampling and heavy grazing) near the source, which transitions into zones of lower utilization further away.
2. **Optimal Foraging Theory (OFT):** Livestock are "energy-minimizers." They aim to maximize nutrient intake while minimizing the energy expended in movement. As the distance to water increases, the net energy gain from grazing decreases because of the "travel cost."

### B. The "Metabolic Cost of Walking" Assumption
A critical assumption in this model is that the **utilization rate of forage is inversely proportional to the distance from water**.
- **The 500m Rule:** In intensive systems, it is generally accepted that for every 100 meters further from water, the effective grazing capacity drops. Beyond 500-800 meters, large portions of forage may remain untouched or "wasted" because the metabolic cost of walking to that forage exceeds the animal's willingness or energy budget.
- **Application in the Project:** By calculating the **Euclidean distance** at a 2m resolution, the Excel model can apply a "Distance Discount Factor" to each pixel, ensuring that the final "Usable Forage" (kg MS) reflects real-world animal behavior.

### C. Logic for Western Boundary Placement
The decision to propose the water point at **429250, 4221800** (West side) follows three logical pillars:
1. **Accessibility and Logistics:** On most Mediterranean farms, infrastructure (roads and main water lines) follows the boundary lines. The Western side shows the most consistent access to potential off-site connection points.
2. **Infrastructure Cost Minimization:** Placing the water point on the boundary near a potential entrance minimizes the length of piping required to bring water into the system.
3. **Rotational Efficiency:** The farm is subdivided East-to-West. Placing the water source on the Western edge allows for a "Radial" or "Front-access" grazing design. This ensures that even as the herd moves through sections C1, C2, and C3, they maintain the shortest possible path back to the central water source, reducing the formation of "cow paths" and minimizing soil erosion.

### D. Euclidean Distance vs. Least-Cost Path
While the analysis uses **Euclidean (straight-line) distance**, it assumes the land is relatively traversable. Since the terrain analysis (Slope) is also provided, the model can combine these: steep slopes effectively "increase" the perceived distance for the animal.

## 4. Excel Calculation Logic (Agronomic Model)

### Stage A: Biomass Estimation (Monteith Model)
1. **NDVI to fPAR:** NDVI is converted to the **Fraction of Photosynthetically Active Radiation (fPAR)**.
2. **PAR Absorption:** Solar radiation data is multiplied by fPAR to determine **APAR**.
3. **Dry Matter Production:** APAR is multiplied by **Radiation Use Efficiency (RUE)**, adjusted by Temperature and Vapor Pressure stress factors.

### Stage B: Usability and Feed Supply
1. **Usable Forage:** Production is modified by a **Use Factor** derived from the **Water Distance Logic** explained above and the **Slope Analysis**.
2. **UFL Conversion:** Consumable Dry Matter is converted to **UFL (Feed Units)**.

### Stage C: Balancing
The model matches the **UFL Supply** (from grass) with the **UFL Demand** (animal requirements) to calculate the number of grazing days per section.

## 5. Technical Parameters Summary

- **Primary CRS:** EPSG:25830
- **Reporting Resolution:** 2.0 meters
- **Vegetation Index:** NDVI
- **Tree Masking:** NDVI > 0.35 (to exclude non-grazable biomass)
- **Water Point:** 429250, 4221800 (EPSG:25830)

## 6. Final Deliverables
- `/layers`: Vector files (finca, subdivisions, water point).
- `/rasters`: 2m GeoTIFFs (Slope, NDVI series, Distance, Masks).
- `Plan de pastoreo.xlsx`: The updated calculation engine.
- `METHODOLOGY.md`: This comprehensive guide.
