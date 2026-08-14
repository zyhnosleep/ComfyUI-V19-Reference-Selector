import pathlib
import sys
import unittest


PACKAGE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from index_parser import parse_asset_indexes, parse_scene_index


class IndexParserTests(unittest.TestCase):
    def test_asset_order_and_duplicates_are_preserved(self):
        self.assertEqual(parse_asset_indexes("6,3,0,1", 7), [6, 3, 0, 1])
        self.assertEqual(parse_asset_indexes("0, 0, 1, 0", 2), [0, 0, 1, 0])

    def test_asset_count_must_be_exactly_four(self):
        with self.assertRaisesRegex(ValueError, "恰好包含4个整数"):
            parse_asset_indexes("0,1,2", 3)
        with self.assertRaisesRegex(ValueError, "恰好包含4个整数"):
            parse_asset_indexes("0,1,2,3,4", 5)

    def test_empty_and_non_integer_asset_tokens_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "第2个主体索引为空"):
            parse_asset_indexes("0,,1,2", 3)
        with self.assertRaisesRegex(ValueError, "不是整数"):
            parse_asset_indexes("0,角色A,1,2", 3)

    def test_negative_and_out_of_range_asset_indexes_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "不能为负数"):
            parse_asset_indexes("0,-1,1,2", 3)
        with self.assertRaisesRegex(ValueError, "索引8越界"):
            parse_asset_indexes("0,1,2,8", 7)

    def test_scene_index_is_one_valid_integer(self):
        self.assertEqual(parse_scene_index(" 1 ", 2), 1)
        with self.assertRaisesRegex(ValueError, "只能包含1个整数"):
            parse_scene_index("0,1", 2)
        with self.assertRaisesRegex(ValueError, "不是整数"):
            parse_scene_index("江边", 2)
        with self.assertRaisesRegex(ValueError, "不能为负数"):
            parse_scene_index("-1", 2)
        with self.assertRaisesRegex(ValueError, "索引2越界"):
            parse_scene_index("2", 2)


if __name__ == "__main__":
    unittest.main()
