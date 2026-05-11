# Screenwriter Skill — 中文快速开始

通用中文编剧 skill。适合电影、短剧、剧集、分集大纲、人物弧光、对白、结构审阅和时长删减。默认输出中文剧本；只有用户明确要求时才输出双语或外语版本。

---

## 里面有什么

- **`SKILL.md`** — skill 主入口，定义中文输出和工作方式。
- **`methodology.md`** — 麦基 + 坎贝尔 + 亚里士多德方法论。
- **`style-rules.md`** — 中文剧本写作规则和 Hollywood 格式变体。
- **`workflow.md`** — 和用户协作、改稿、审阅、删减的流程。
- **`timing-and-cutting.md`** — 估算屏幕时间和删减长度。
- **`templates/`** — 梗概、人物、世界观、分集大纲模板。
- **`tools/`** — `.docx` 生成器：剧本、双语剧本、分集大纲。

---

## 怎么开始

### 第 1 步：安装

把 `screenwriter/` 文件夹放进项目的 `.cursor/skills/` 或全局 skills 目录。

### 第 2 步：唤起 skill

> “使用 screenwriter skill，我们开始写中文剧本。”

助手会读取 `SKILL.md`、方法论、写作规则和 workflow。

### 第 3 步：给材料

任选一种：

**A. 已有梗概 / 分集大纲 / 场景草稿。**
直接发文件，助手会读完后问从哪里开始。

**B. 只有一个想法。**
用一两段说明，助手会先帮你打磨一句话故事，再到梗概、分集大纲、场景。

**C. 只有片名和类型。**
先填 `templates/synopsis.template.md` 和 `templates/characters.template.md`，再迭代。

### 第 4 步：按场景工作

标准循环：
1. 你指定要写哪一场。
2. 助手给一个中文版本 + 一个创作理由。
3. 你提出修改。
4. 助手只改你要求的部分。
5. 场景定稿后，用 `tools/build_screenplay.js` 导出 `.docx`。

---

## ИНСТРУМЕНТЫ ВЫГРУЗКИ

### 中文剧本（Hollywood 变体格式）
```bash
cp tools/build_screenplay.js my_scene.js
# открой my_scene.js, заполни массив `screenplay` через slug/action/character/dial/trans
NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node my_scene.js
# 生成 screenplay.docx
```

### 双语剧本（仅在明确需要时）
```bash
cp tools/build_bilingual.js my_bilingual.js
# заполни через ...dialB("Main lang", "Translation")
node my_bilingual.js
# 生成 screenplay-bilingual.docx
```

### 分集大纲 / 场景大纲
```bash
cp tools/build_treatment.js my_treatment.js
# заполни через scene("Title", "Body", "[опц.] audit-tag")
node my_treatment.js
# 生成 treatment.docx
```

---

## ТИПОВЫЕ ЗАПРОСЫ К СКИЛЛУ

| Запрос | Что делает Клод |
|---|---|
| “写第5场” | 读取分集大纲 → 给一个中文版本 + 一个理由 |
| “这不对” | 只问一个窄问题 → 再给一个新版本 |
| “做双语版” | 使用 `tools/build_bilingual.js`，默认中文为主语言 |
| “审一下因果链” | 按分集大纲逐场标记问题 |
| “大概多少分钟？” | 按场景类型估算屏幕时间 |
| “压到 X 分钟” | 给具体删减计划 |
| “让角色Y的说话方式区别于X” | 对比对白，做人物声口调整 |

---

## ТРИ ВЕЩИ, КОТОРЫЕ КЛОД НЕ ДЕЛАЕТ

1. **Не пишет 5 вариантов** — даёт ОДИН + аргумент.
2. **Не «улучшает» соседние реплики** — меняет только то, что просили.
3. **Не описывает эмоции** — только глаголы действия.

Если клод нарушает — скажи: «Один вариант, не пять» или «Меняй только Х».

---

## ПЕРСОНАЛИЗАЦИЯ СКИЛЛА

Если ты пишешь много фильмов в одном жанре — можешь форкнуть этот скилл и добавить:

- **`reference-films.md`** — список референс-фильмов с разбором сцен.
- **`my-style.md`** — твои личные предпочтения по стилю (напр. «не люблю флешбеки», «всегда кончать на тишине»).
- **`recurring-tropes.md`** — твои повторяющиеся приёмы.

Скилл становится твоим, не общим.
