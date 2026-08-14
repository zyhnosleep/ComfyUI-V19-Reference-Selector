# V19 Reference Selector

Transparent reference-image selection for the distilled V19 short-drama workflow.

## Inputs

- `asset_images`: character and key-prop images in one batch.
- `asset_indexes`: exactly four comma-separated, zero-based indexes, such as `6,3,0,1`.
- `scene_images`: scene reference images in one batch.
- `scene_index`: one zero-based scene index, such as `0`.

## Outputs

- `selected_assets`: four images in requested shot order. Duplicate indexes are preserved.
- `selected_scene`: one selected scene image.
- `selection_summary`: the resolved indexes for inspection.

Invalid counts, non-integers, negative values, and out-of-range indexes stop execution with a Chinese error. The node never changes an invalid index automatically.
