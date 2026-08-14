import pathlib
import sys
import unittest

import torch


PACKAGE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from reference_selector import V19ReferenceSelector


class ReferenceSelectorTests(unittest.TestCase):
    def setUp(self):
        self.node = V19ReferenceSelector()
        self.assets = torch.stack(
            [torch.full((2, 3, 3), float(index)) for index in range(7)]
        )
        self.scenes = torch.stack(
            [torch.full((2, 3, 3), float(index + 10)) for index in range(2)]
        )

    def test_selects_order_duplicates_scene_and_summary(self):
        assets, scene, summary = self.node.select(
            self.assets, "6,3,0,3", self.scenes, "1"
        )
        self.assertEqual(tuple(assets.shape), (4, 2, 3, 3))
        self.assertEqual(tuple(scene.shape), (1, 2, 3, 3))
        self.assertEqual(assets[:, 0, 0, 0].tolist(), [6.0, 3.0, 0.0, 3.0])
        self.assertEqual(scene[0, 0, 0, 0].item(), 11.0)
        self.assertIn("主体索引：6,3,0,3", summary)
        self.assertIn("场景索引：1", summary)

    def test_invalid_tensor_rank_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "必须是4维IMAGE批次"):
            self.node.select(self.assets[0], "0,0,0,0", self.scenes, "0")

    def test_empty_batch_is_rejected(self):
        empty = torch.empty((0, 2, 3, 3))
        with self.assertRaisesRegex(ValueError, "没有加载角色/道具图片"):
            self.node.select(empty, "0,0,0,0", self.scenes, "0")


if __name__ == "__main__":
    unittest.main()
