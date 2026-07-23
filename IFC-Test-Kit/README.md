# IFC Viewer Test Kit

## Purpose

This folder contains the files used to test and compare IFC viewers.

## Files

- `duplex.ifc` — Main IFC model used for standard testing.
- `model_elements.csv` — List of IFC elements and their `GlobalId` values.
- `analytics_dataset_with_levels.csv` — Analytics data matched to the model using `GlobalId`.
- `large_test_model.ifc` — Larger IFC model used only for performance testing.

## Testing

1. Load `duplex.ifc`.
2. Connect the analytics CSV using `GlobalId`.
3. Test numeric and category colouring.
4. Display analytics values for selected elements.
5. Test totals or averages by level.
6. Open `large_test_model.ifc` and record loading speed, responsiveness and stability.
7. Record any scripts, conversions or preprocessing required.

Use `duplex.ifc` for the standard tests and `large_test_model.ifc` only for the performance test.