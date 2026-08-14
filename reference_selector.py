import torch

try:
    from .index_parser import parse_asset_indexes, parse_scene_index
except ImportError:
    from index_parser import parse_asset_indexes, parse_scene_index


class V19ReferenceSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "asset_images": ("IMAGE",),
                "asset_indexes": ("STRING", {"default": "0,0,0,0"}),
                "scene_images": ("IMAGE",),
                "scene_index": ("STRING", {"default": "0"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "STRING")
    RETURN_NAMES = ("selected_assets", "selected_scene", "selection_summary")
    FUNCTION = "select"
    CATEGORY = "V19 Short Drama"

    @staticmethod
    def _validate_image_batch(images, label):
        if not isinstance(images, torch.Tensor) or images.ndim != 4:
            raise ValueError(f"V19参考图选择失败：{label}必须是4维IMAGE批次。")
        if images.shape[0] < 1:
            raise ValueError(f"V19参考图选择失败：没有加载{label}。")

    def select(self, asset_images, asset_indexes, scene_images, scene_index):
        self._validate_image_batch(asset_images, "角色/道具图片")
        self._validate_image_batch(scene_images, "场景图片")

        selected_asset_indexes = parse_asset_indexes(
            asset_indexes, int(asset_images.shape[0])
        )
        selected_scene_index = parse_scene_index(
            scene_index, int(scene_images.shape[0])
        )

        index_tensor = torch.tensor(
            selected_asset_indexes, device=asset_images.device, dtype=torch.long
        )
        selected_assets = asset_images.index_select(0, index_tensor)
        selected_scene = scene_images[selected_scene_index:selected_scene_index + 1]
        summary = (
            f"主体索引：{','.join(str(value) for value in selected_asset_indexes)}\n"
            f"主体图片数：{selected_assets.shape[0]}\n"
            f"场景索引：{selected_scene_index}"
        )
        return selected_assets, selected_scene, summary
