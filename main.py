from __future__ import annotations

import argparse
from pixian_core import PixianEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Pixian 笔仙：中文长篇小说自动创作机器")
    parser.add_argument("--input", help="可选：用于模仿创作的 txt/epub 文件")
    parser.add_argument("--goal", default="主角从末法时代重启仙路", help="小说创作目标")
    parser.add_argument("--chapters", type=int, default=8, help="生成章节数")
    parser.add_argument("--chars", type=int, default=3500, help="每章目标中文字符数")
    parser.add_argument("--factions", type=int, default=120, help="势力数量")
    parser.add_argument("--out", default="output", help="输出目录")
    parser.add_argument("--direction", action="append", default=[], help="章节方向修正，格式：17:让主角卧底敌宗")
    args = parser.parse_args()

    engine = PixianEngine(style_source=args.input)
    engine.build_world(faction_count=args.factions)
    engine.plan_outline(chapters=args.chapters, goal=args.goal)

    for item in args.direction:
        idx, text = item.split(":", 1)
        engine.set_direction(int(idx) - 1, text)

    for i in range(args.chapters):
        engine.generate_chapter(i, target_chars=args.chars)

    engine.export(args.out)
    print(f"Pixian finished. Output: {args.out}")


if __name__ == "__main__":
    main()
