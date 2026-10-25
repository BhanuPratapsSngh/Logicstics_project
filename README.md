# FedEx Logistics Performance Analysis — SCMS Delivery History (EDA)

## What the notebook does
- **Cleaning:** repairs the BOM in the first column and the mojibake in "Côte d'Ivoire", parses two different date formats explicitly, keeps business sentinels (`Pre-PQ Process`, `N/A - From RDC`, `Weight Captured Separately`, `Freight Included in Commodity Cost`, …) as status columns, flags outliers instead of deleting them, and exports a 10,324-row cleaned file.
- **Features:** `delivery_delay_days`, `delivery_performance`, `is_late`, `po_to_scheduled_days`, `po_to_delivered_days`, `recording_lag_days`, `order_year`, plus `scheduled_year` (used for trends because `order_year` is empty for RDC rows).
- **EDA:** 26 charts — 9 univariate (incl. missing data), 6 numerical-vs-categorical, 4 numerical-vs-numerical, 3 categorical-vs-categorical, 4 multivariate. Every chart is followed by *Why this chart / Insight / Business impact*, with the numbers printed under the chart.

## Key findings
- 61.3% of line items arrive on schedule, 27.3% early, 11.5% late (1,186 items, $259.0 M).
- Fulfilment route matters most: RDC is late 17.2% vs 5.3% for direct-from-vendor, and produces 78.2% of late items (matching the direct rate would cut late items by about 54%).
- Three vendors (Aurobindo, Cipla, Orgenics) cause 83.0% of late direct deliveries; trucks to Mozambique, Zambia, Tanzania and Rwanda cause 22.7% of all late items.
- Late rate jumped from 2.4% (2007–2009) to 15.2% (2010–2015), mostly on the RDC route.
- Order size, weight and value barely correlate with delay (|ρ| ≤ 0.05).
- Freight is 12.6% of value on regular Air vs 3.5% on Ocean; $10.02/kg by Air vs $2.50 by Truck.

## Assumptions
- Delay = delivered date − scheduled date; "late" means delay > 0.
- "SCMS from RDC" in the Vendor column is an internal warehouse label, so vendor charts use external vendors only and RDC is analysed as a fulfilment route.
- Rows with no shipment mode (360) are excluded from mode-based charts only.
- Cells with fewer than 10 shipments (heatmap) or 20 shipments (yearly trend) are hidden to avoid noisy rates.
- Team names and the GitHub URL are placeholders to be filled in.
