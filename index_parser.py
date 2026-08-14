def _parse_integer(token, label, position):
    value = token.strip()
    if not value:
        raise ValueError(f"V19参考图选择失败：第{position}个{label}索引为空。")
    try:
        parsed = int(value, 10)
    except ValueError as exc:
        raise ValueError(
            f"V19参考图选择失败：第{position}个{label}索引“{value}”不是整数。"
        ) from exc
    if parsed < 0:
        raise ValueError(
            f"V19参考图选择失败：第{position}个{label}索引不能为负数，当前值为{parsed}。"
        )
    return parsed


def _validate_bound(index, label, position, image_count):
    if image_count < 1:
        raise ValueError(f"V19参考图选择失败：没有加载{label}图片。")
    if index >= image_count:
        raise ValueError(
            f"V19参考图选择失败：第{position}个{label}索引{index}越界；"
            f"已加载{image_count}张{label}图片，有效索引为0～{image_count - 1}。"
        )


def parse_asset_indexes(raw, image_count):
    tokens = str(raw).split(",")
    if len(tokens) != 4:
        raise ValueError(
            f"V19参考图选择失败：主体索引必须恰好包含4个整数，当前得到{len(tokens)}个。"
        )
    indexes = []
    for position, token in enumerate(tokens, start=1):
        index = _parse_integer(token, "主体", position)
        _validate_bound(index, "角色/道具", position, image_count)
        indexes.append(index)
    return indexes


def parse_scene_index(raw, image_count):
    tokens = str(raw).split(",")
    if len(tokens) != 1:
        raise ValueError("V19参考图选择失败：场景索引只能包含1个整数。")
    index = _parse_integer(tokens[0], "场景", 1)
    _validate_bound(index, "场景", 1, image_count)
    return index
