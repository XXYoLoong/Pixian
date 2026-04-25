from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .markov import MarkovStyleModel
from .reader import read_novel

SURNAMES = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹"
GIVEN = "玄微照临星阙云舟霜月烬渊澜昼衡珩青禾长陵昭明孤鸿听雪观棋无咎折枝归尘望舒九思曜灵怀瑾扶光知微兰若惊蛰"
SECT_SUFFIX = ["宗", "门", "宫", "阁", "盟", "书院", "剑庐", "天府", "灵台", "观", "城", "山庄"]
PREFIX = ["太玄", "归墟", "无量", "星河", "苍梧", "玉京", "扶摇", "九曜", "玄霜", "赤明", "寒渊", "青冥", "烛龙", "云梦", "天机", "墨麟", "长生", "逐鹿", "听雪", "万象"]
REALMS = ["凡骨", "启灵", "纳气", "筑台", "金丹", "元婴", "化神", "洞虚", "合道", "问鼎", "渡劫", "飞升"]


@dataclass
class Character:
    name: str
    faction: str
    role: str
    realm: str
    motive: str
    secret: str
    first_seen: int


@dataclass
class Faction:
    name: str
    alignment: str
    power: int
    territory: str
    doctrine: str
    rivals: list[str] = field(default_factory=list)


@dataclass
class World:
    name: str
    core_law: str
    realms: list[str]
    factions: list[Faction]
    characters: list[Character]
    buildings: list[str]
    map_tiles: list[list[str]]


class PixianEngine:
    def __init__(self, style_source: str | None = None, order: int = 3) -> None:
        self.style = MarkovStyleModel(order=order)
        if style_source:
            self.style.fit(read_novel(style_source))
        self.world: World | None = None
        self.outline: list[dict[str, str]] = []
        self.chapter_directions: dict[int, str] = {}
        self.chapters: list[str] = []

    def _name(self) -> str:
        return random.choice(SURNAMES) + "".join(random.choice(GIVEN) for _ in range(random.choice([1, 2])))

    def build_world(self, faction_count: int = 120, character_count: int = 60) -> World:
        factions: list[Faction] = []
        for _ in range(faction_count):
            name = random.choice(PREFIX) + random.choice(SECT_SUFFIX)
            if any(f.name == name for f in factions):
                name += random.choice("天地玄黄")
            factions.append(Faction(
                name=name,
                alignment=random.choice(["正道", "魔道", "中立", "隐世", "皇朝", "商盟"]),
                power=random.randint(18, 99),
                territory=random.choice(PREFIX) + random.choice(["原", "海", "洲", "岭", "城", "荒", "泽"]),
                doctrine=random.choice(["以剑问天", "万物皆可成书", "灵脉即国脉", "不问出身，只问道心", "献祭旧神，重开天门"]),
            ))
        for faction in factions:
            faction.rivals = random.sample([f.name for f in factions if f.name != faction.name], k=3)

        characters: list[Character] = []
        for i in range(character_count):
            faction = random.choice(factions).name
            characters.append(Character(
                name=self._name(),
                faction=faction,
                role=random.choice(["主角", "宿敌", "宗主", "长老", "剑侍", "阵师", "密探", "遗孤", "书灵"]),
                realm=random.choice(REALMS),
                motive=random.choice(["寻找失落天书", "复兴旧族", "掩盖身世", "阻止飞升骗局", "夺回被篡改的命运"]),
                secret=random.choice(["体内藏有第二枚金丹", "真实身份来自敌对宗门", "曾被天道除名", "记忆被封在一座旧城", "与世界核心同源"]),
                first_seen=random.randint(1, 12),
            ))

        buildings = [random.choice(PREFIX) + random.choice(["殿", "楼", "塔", "台", "宫", "阙", "陵", "渡", "关", "藏书阁"]) for _ in range(80)]
        tiles = [[random.choice(["山", "泽", "城", "宗", "林", "荒", "海", "塔"]) for _ in range(14)] for _ in range(9)]
        self.world = World(
            name=random.choice(PREFIX) + "界",
            core_law="凡被写入天书者，命运会沿文字生长；凡被删去名字者，将从众生记忆中消失。",
            realms=REALMS,
            factions=factions,
            characters=characters,
            buildings=buildings,
            map_tiles=tiles,
        )
        return self.world

    def plan_outline(self, chapters: int = 24, goal: str = "主角从末法时代重启仙路") -> list[dict[str, str]]:
        events = [
            "天书残页现世", "主角被宗门除名", "旧城秘境开启", "敌对势力围猎", "战力体系第一次反转", "命盘被人篡改",
            "卧底进入敌宗", "主角发现世界法则漏洞", "百宗会盟", "反派请出旧神", "伏笔集中回收", "飞升真相揭露",
        ]
        self.outline = []
        for i in range(chapters):
            event = events[i % len(events)]
            self.outline.append({
                "chapter": str(i + 1),
                "title": f"第{i + 1}章 · {event}",
                "goal": goal,
                "beat": event,
                "conflict": random.choice(["战力压制", "身份暴露", "盟友背叛", "天道审判", "秘境坍塌", "势力谈判"]),
            })
        return self.outline

    def set_direction(self, chapter_index: int, direction: str) -> None:
        self.chapter_directions[chapter_index] = direction

    def generate_chapter(self, chapter_index: int, target_chars: int = 3500) -> str:
        if not self.world:
            self.build_world()
        if not self.outline:
            self.plan_outline()
        chapter = self.outline[chapter_index]
        direction = self.chapter_directions.get(chapter_index, "")
        head = [chapter["title"], "", f"【本章目标】{chapter['beat']}；核心冲突：{chapter['conflict']}。"]
        if direction:
            head.append(f"【方向修正】{direction}。")
        head.append("")
        if self.style.chain:
            body = self.style.generate(target_chars)
        else:
            body = self._template_body(chapter, target_chars)
        text = "\n".join(head) + body
        while len(self.chapters) <= chapter_index:
            self.chapters.append("")
        self.chapters[chapter_index] = text
        return text

    def _template_body(self, chapter: dict[str, str], target_chars: int) -> str:
        assert self.world is not None
        chars = random.sample(self.world.characters, k=min(4, len(self.world.characters)))
        factions = random.sample(self.world.factions, k=min(3, len(self.world.factions)))
        fragments = []
        while sum(map(len, fragments)) < target_chars:
            c = random.choice(chars)
            f = random.choice(factions)
            place = random.choice(self.world.buildings)
            fragments.append(
                f"{place}外，{c.name}听见风里传来断续的钟声。{chapter['beat']}并非偶然，{f.name}早在三日前便封锁了通往灵脉的道路。"
                f"他记得自己的境界仍停在{c.realm}，但命盘上的字迹却忽然加深，像有一只看不见的手正在替他补完余生。"
                f"{f.doctrine}，这是{f.name}刻在山门上的古训。可今夜它更像一句诅咒，逼迫所有人承认：这片天地的法则已经开始松动。"
            )
        return "".join(fragments)[:target_chars]

    def export(self, outdir: str | Path) -> None:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        if self.world:
            (outdir / "world.json").write_text(json.dumps(asdict(self.world), ensure_ascii=False, indent=2), encoding="utf-8")
        (outdir / "outline.json").write_text(json.dumps(self.outline, ensure_ascii=False, indent=2), encoding="utf-8")
        chapters_dir = outdir / "chapters"
        chapters_dir.mkdir(exist_ok=True)
        for i, text in enumerate(self.chapters):
            (chapters_dir / f"chapter_{i + 1:03d}.txt").write_text(text, encoding="utf-8")
