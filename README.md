# 笔仙 Pixian

**请笔落纸，万象成书。**

Pixian 是一个面向中文长篇小说的自动创作机器。它不是简单的“生成一段文本”，而是把小说拆成世界观、战力体系、势力网络、人物谱系、建筑地图、大纲命盘、章节正文和一致性巡检等可持续更新的模块。

## 能力

- 随机生成或按目标生成小说项目。
- 读取 `.txt` 与 `.epub` 文件，抽取文本风格用于模仿创作。
- 自动生成世界观、十二阶战力体系、百级势力、人物资料、建筑名和地图。
- 自动生成章节大纲，并保持章节前后文一致性。
- 支持从任意章节开始写入指定剧情方向。
- 每章目标输出约 3500 中文字符，可通过参数调整。
- 附带高完成度可视化 Web UI 原型：`web/index.html`。

## 快速运行

```bash
python main.py --chapters 8 --chars 3500 --factions 120 --out output
```

使用 txt/epub 模仿创作：

```bash
python main.py --input sample.txt --chapters 12 --goal "写一部东方玄幻长篇，主角从末法时代重启仙路" --out output
```

从指定章节写入剧情方向：

```bash
python main.py --chapters 24 --direction "17:让主角加入敌对宗门卧底" --out output
```

## 可视化 UI

直接打开：

```bash
web/index.html
```

或用本地静态服务器：

```bash
python -m http.server 5173 -d web
```

然后访问：

```text
http://127.0.0.1:5173
```

## 工程结构

```text
Pixian/
├─ pixian_core/
│  ├─ engine.py        # 世界观、大纲、章节生成核心
│  ├─ markov.py        # 风格模仿模型
│  └─ reader.py        # txt/epub 读取
├─ web/
│  ├─ index.html       # 可视化创作驾驶舱
│  ├─ styles.css       # 东方玄幻 + AI 工具感 UI
│  └─ app.js           # mock 交互与动效
├─ docs/
│  └─ UIUX.md          # 产品与视觉设计说明
├─ scripts/
│  └─ push-to-github.ps1
└─ main.py             # CLI 入口
```

## 设计方向

Pixian 的产品形态是一张“故事命盘”，而不是传统表单后台。左侧是导航，中央是创作画布，右侧是记忆与一致性巡检。章节、大纲、势力、人物和地图不孤立存在，而是互相连接、互相校验。

## GitHub

目标仓库：`XXYoLoong/Pixian`
