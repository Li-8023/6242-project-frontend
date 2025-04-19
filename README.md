## Usage Guide

## Installation

```bash
npm install
```

## Run
```bash
npm run dev
```
---

## Display Adaptation Settings

If the interface does not display in full screen after launching, you can manually adjust the layout.

### How to Enable Auto Adaptation:

1. Locate the **Settings** button at the **top-right corner** of the screen.
2. Click the button to open the settings menu.
3. Under **Global Settings**, toggle **Enable Auto Adaptation** to `Yes`.  
   > This will automatically adjust the resolution to the default (1920×1080) or fit your screen.

---

## Module Descriptions (`src/views/index`)

### `left-top.vue` – Car Segmentation (Top Left)
Displays a scatter plot that segments vehicles based on price and mileage, using clustering.  
Each point represents a car, and colors indicate cluster types:  
- 🟦 High mileage, low price  
- 🟥 Low mileage, high price  
- 🟩 Low mileage, low price

### `right-top.vue` – Dealer Region Aggregation (Top Right)
Shows a U.S. map with pie charts representing the distribution of car body types (SUV, Sedan, Truck, Other) across different regions.  
Great for spatial analysis of dealership sales.

### `left-bottom.vue` – Sales Forecasting (Bottom Left)
Implements a Holt-Winters Forecasting Chart, visualizing time-series trends in car sales.  
Includes projected future sales with smooth trend curves and confidence intervals.

### `right-bottom.vue` – Car Price Prediction (Bottom Right)
Enables interactive car price prediction based on user-selected features (e.g., make, trim).  
Displays:
- Predicted price
- Confidence interval slider
- Model reliability score (e.g., Random Forest)

---

## Project Overview

This frontend project implements a Real-Time Automotive Sales Analytics Dashboard.  
It features four modular panels powered by ECharts and machine learning models, enabling users to:

- Explore car price/mileage clusters
- Analyze regional sales distributions
- Forecast future sales trends
- Predict vehicle prices with confidence intervals
