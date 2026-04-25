---
name: gpt-image2-prompts
description: "GPT-Image-2 全场景专业提示词库。以 EvoLinkAI/awesome-gpt-image-2-prompts（3.5k⭐）为主框架，融合 xianyu110/awesome-gptimage2（80+中文实战）、gpt-image2/awesome-gptimage2-prompts（1123条精选库）及专业视频分镜头表模板。当用户提到"gpt提示词"、"gpt图片"、"gpt-image"、"gptimage"、"GPT Image 2"、"chatgpt生图"、"gpt画图"、"gpt出图"、"gpt分镜"、"分镜提示词"时触发。"
source: "主框架: https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts | 融合: https://github.com/xianyu110/awesome-gptimage2 + https://github.com/gpt-image2/awesome-gptimage2-prompts"
date_added: "2026-04-25"
updated: "2026-04-25"
---

# GPT-Image-2 全场景提示词专家

> **主框架**：[EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) ⭐3.5k — 人像/海报/角色/UI/社区全覆盖
> **融合**：[xianyu110/awesome-gptimage2](https://github.com/xianyu110/awesome-gptimage2) × [gpt-image2/awesome-gptimage2-prompts](https://github.com/gpt-image2/awesome-gptimage2-prompts)（1123条）× 专业分镜头表模板

---

## 触发关键词

| 用户说 | 触发动作 |
|---|---|
| "gpt提示词" / "gpt图片" / "gpt出图" | 激活，询问需求或输出场景菜单 |
| "gpt画[内容]" / "chatgpt生图" | 直接匹配场景输出提示词 |
| "gpt-image" / "gptimage2" | 激活技能 |
| "gpt分镜" / "分镜提示词" | 进入分镜头表场景 |
| "推荐gpt提示词" | 输出场景菜单 |

---

## 提示词核心框架

```
[任务类型] + [主体描述] + [风格定义] + [技术参数] + [输出规格]
```

| 要素 | 说明 | 示例 |
|---|---|---|
| 任务类型 | 告诉模型做什么 | 人像摄影 / 海报设计 / 信息图 / UI截图 |
| 主体描述 | 画面核心内容 | 人物、产品、场景、信息结构 |
| 风格定义 | 视觉风格和调性 | 35mm胶片 / 新中式 / 赛博朋克 / 水彩 |
| 技术参数 | 光影、材质、构图 | 柔光打光 / 浅景深 / 电影级打光 |
| 输出规格 | 比例和分辨率 | 9:16 / 3:4 / 1:1 / 4K / 8K |

### 5条黄金原则
1. **具体 > 模糊**：描述越具体，输出越精准
2. **中文直接说**：不需要翻译成英文，中文效果一样好
3. **给出文字内容**：直接把图中需要的文字写进提示词
4. **photorealistic** 是万能关键词 → 主动规避塑料感
5. **指定比例**：9:16竖屏 / 16:9横屏 / 3:4海报 / 1:1方图

---

## 场景路由菜单

| # | 场景分类 | 触发关键词 |
|---|---|---|
| **1** | 📸 人像与摄影 | 人像、写真、胶片、摄影、肖像、idol、韩系 |
| **2** | 🎨 海报与插画 | 海报、插画、宣传图、城市海报、国潮 |
| **3** | 👤 角色设计 | 角色、人设、角色卡、设定图、二次元 |
| **4** | 📱 UI与社交媒体截图 | UI、界面、截图、直播间、App截图 |
| **5** | 🌐 社区创意与娱乐 | 整活、梗图、社交媒体整活、模型对比 |
| **6** | 🛒 电商与产品 | 电商、详情页、产品图、白底图 |
| **7** | 📊 信息图与科普 | 信息图、科普、百科、信息长图 |
| **8** | 🎬 分镜头表（Storyboard） | 分镜、storyboard、视频分镜 |

---

## 场景一：📸 人像与摄影

### 1.1 便利店霓虹人像（Case 1 by @BubbleBrain）
```
35mm film photography with harsh convenience store fluorescent lighting mixed with colorful neon signs from outside, authentic film grain, high contrast, slight color cast, cinematic street editorial style, intimate medium shot, early 20s sexy Chinese female idol with ultra-realistic delicate refined Chinese features, seductive almond-shaped fox eyes with natural double eyelids, high nose bridge, small sharp V-shaped jawline, flawless porcelain skin with cool ivory undertone and visible specular highlights from fluorescent light, subtle skin texture and micro pores, natural dewy makeup with soft flush on cheeks, glossy natural pink lips slightly parted, long dark brown hair in a messy high ponytail with many loose strands falling around face and neck, wearing an oversized white button-up shirt as the only top, unbuttoned at the top with deep cleavage and loosely tied at the waist, paired with a tiny black pleated mini skirt, barefoot in simple white slides, seductive casual leaning pose against the glass door of a 24-hour convenience store at late night, intensely seductive playful yet slightly vulnerable gaze straight at the viewer, authentic late-night convenience store atmosphere
```

### 1.2 电影极简人像（Case 2 by @iam_miharbi）
```
Generate a cinematic minimal portrait of a solitary man standing in an intense orange to red gradient environment, strong silhouette lighting, deep shadow contrast, reflective glossy floor, symmetrical composition, minimal
```

### 1.3 日式温泉旅馆人像（Case 3 by @BubbleBrain）
```
35mm film photography, warm vintage Japanese onsen ryokan aesthetic, soft ambient wooden lantern lighting mixed with gentle natural window light, subtle film grain, gentle color shift, intimate medium shot, early 20s beautiful Chinese female idol with ultra-realistic delicate refined Chinese features, seductive almond-shaped fox eyes with natural double eyelids, high nose bridge, small sharp V-shaped jawline, flawless porcelain skin with warm ivory undertone, visible subtle skin texture, soft natural makeup with dewy glow, long dark brown hair tied in a loose low bun with some messy strands, wearing a loose white yukata deliberately slipped off one shoulder, authentic vintage film color grading with warm tones, extremely sharp yet soft skin rendering, no watermark, no text, authentic 35mm film Japanese onsen ryokan atmosphere
```

### 1.4 35mm 闪光灯街拍人像（Case 4 by @BubbleBrain）
```
35mm color film photography with harsh direct on-camera flash, specular highlights on skin and clothing, strong catchlights in eyes, high contrast flash illumination, authentic film grain and color shift, high fashion fresh innocent basketball court editorial style, intimate first-person low-angle POV shot from below, early 20s sexy Chinese female idol, seductive almond-shaped fox eyes with natural double eyelids, flawless realistic porcelain skin with cool ivory undertone and visible flash specular highlights, wearing a loose white tank top and white high-waisted basketball shorts, white knee-high sports socks, seductive natural leaning pose against the basketball hoop pole on the outdoor court at dusk, high contrast film color grading with natural flash look --ar 9:16
```

### 1.5 镜子自拍卧室人像（Case 5 by @Shinning1010）
```
A stunning 18-year-old Chinese girl with a youthful, pure face and realistic skin texture, sitting on a cozy, slightly messy bed in her bedroom. She is taking a mirror selfie with a smartphone, capturing a natural and intimate moment. Wearing casual gray loungewear and neat white crew socks. Soft natural light (golden hour) streams in from a side window, creating a warm, moody, and cinematic atmosphere. 35mm lens, sharp focus on the subject in the mirror, depth of field with a beautifully blurred background (bokeh). Photorealistic, 8K, high resolution. Aspect Ratio: 3:4.
```

### 1.6 日系35mm空气感人像（Case 6 by @BubbleBrain）
```
Analog 35mm film photography, soft airy Japanese-style aesthetic, gentle diffused natural window light, slight overexposure, pastel tones, low contrast, soft highlights, minimal indoor setting near a window with white curtains, young East Asian woman, natural minimal makeup, soft realistic skin texture, long slightly messy dark hair, oversized white button-up shirt, light casual shorts, barefoot, standing naturally with relaxed posture, gentle soft smile, soft film grain, dreamy and understated atmosphere --ar 9:16
```

### 1.7 奢华美妆人像（Case 7 by @patrickassale）
```
Luxury Glam Beauty Portrait: Beautiful Black woman, youthful spirit, creamy vanilla, silk press, mahogany red, subtle confidence, textured fabric, sapphire blue, minimal jewelry, beachside breeze, lens flare effect, nostalgic, cinematic lens, symmetrical composition, soft focus, high fashion photography, monochromatic, dewy finish, mysterious tension, layered elements
```

### 1.8 韩系9格人像拼图（Case 11 by @BubbleBrain）
```
9:16 vertical, Korean idol portrait photoshoot, 3x3 grid (nine frames), same person in all images, consistent facial features and styling, soft black mist filter effect, lowered contrast, blooming highlights, subtle glow around light sources
```

### 1.9 CCD相机风韩系抓拍（Case 12 by @BubbleBrain）
```
mobile phone photo, old CCD camera aesthetic, harsh flash, grainy, dim messy indoor lighting, candid snapshot feeling, slight motion blur, young Korean female idol, soft innocent look
```

### 1.10 复古报纸头版设计（Case 19 by @Naiknelofar788）
```
Create the most realistic front page design of a vintage newspaper featuring the main character. The layout should be made in the style of a real printed newspaper with a cinematic black-and-white aesthetic.
The main photo should be prominently placed in the center. Create a bold, attention-grabbing headline at the top. Add realistic newspaper elements: columns of small text, fictitious publication name (e.g., "The Daily Prompts"), date, issue number, decorative lines, vintage typography. Style: black and white or slightly faded monochrome, fine paper texture, grain, and ink defects. Aspect ratio: 4:5 or 1:1. High-detail, ultra-realistic hybrid of editorial photography and print design.
```

### 1.11 超写实电影感DSLR人像（Case 25 by @harboriis）
```
Ultra-realistic cinematic DSLR photograph, [describe subject], shot from [angle], photorealistic, 8K, high resolution, zero AI look, natural skin rendering, realistic hair strands, fabric texture, shallow depth of field, cinematic premium color grading --ar 9:16
```

---

## 场景二：🎨 海报与插画

### 2.1 城市宣传海报（Spring 2026 波士顿风格）
```
A striking Spring 2026 city poster for [城市名] with an elegant celebratory mood and a bold contemporary design. On a clean off-white textured background with large areas of negative space, [标志性元素] flows in a dynamic calligraphic curve, gradually transforming into a dreamlike hand-painted panorama of [城市名]. Include iconic elements: [地标1]、[地标2]、[地标3]. Elegant typography: "SPRING 2026" with a vertical slogan "[宣传语]", 9:16
```

### 2.2 复古旅游海报（意大利海岸风格）
```
Modern pencil illustration of Vintage travel poster illustration of [目的地], panoramic coastal scene, classic 1960s car driving along a curved road, deep blue sea with small sailboats, colorful pastel hillside village, bright blue sky with soft clouds, bold vibrant colors, retro 1950s travel poster style, cinematic composition, high detail, screen print texture, graphic illustration
```

### 2.3 中国S型双重曝光城市海报
```
一张充满新春喜庆氛围但不失高雅格调的 2026 城市宣传海报。
双重曝光，构图延续了S型的流动感；
在纯白的纹理背景右下角，一个身穿中国传统服饰的微缩人物正在挥舞着一条长长的红色丝绸舞带，这条红绸在空中舞动，向左上方飘动的过程中，奇幻地变形成了一条壮丽的山脉河流。
在这条"河流"中，叠加了一个有山有海河的[城市]城市手绘图，国潮，景色尽在眼底。
[城市]的地标建筑（[地标1]，[地标2]，[地标3]）。
左下角排版着"SPRING 2026"和竖排的宣传语，尺寸9:16。
```

### 2.4 极简新中式S型美学海报（Case 4 by @liyue_ai）
```
极简新中式美学风格，画面以淡雅的灰白色为底，呈现出一种纸艺剪影般的立体感。
一条S形蜿蜒的裂痕状边缘将画面分割，仿佛撕开了一层纸面，露出内部色彩斑斓的东方山水景象。
裂口内，一条蜿蜒的河流自上而下贯穿整个构图，河水以深浅不一的蓝色渲染，层次分明。
河岸两侧点缀着青翠的山丘与梯田，色彩柔和，绿红交织。
画作边缘采用撕纸效果，营造出立体浮雕般的视觉体验。
下方题字"东方美学"，日期"2026/04/18"，整体氛围静谧深远。
```

### 2.5 科幻曼荼罗插画
```
曼荼羅の近未来SF版を描いて（科幻风格的曼陀罗，未来感，科技感）
```

### 2.6 剪纸艺术城市海报（Case 27 by @liyue_ai）
```
以[城市]现代都市景观为灵感的剪纸艺术，通过精巧的镂空手法在一整幅纸上，立体刻画[地标1]、[地标2]等地标建筑与繁华城景。
所有建筑与元素均以流畅的线条与结构相连，无孤立部分，构成一幅完整的都市画卷。
画面采用金属箔或光泽纸材质，表面带有细腻的明暗光泽，在光照下呈现柔和的高光与阴影。
作品中巧妙融入轻盈的蒲公英绒毛或星光般的动态光点，象征梦想与活力。整体呈现8K超高清视觉。
```

### 2.7 暗黑东方幻想城市海报（Case 42 by @liyue_ai）
```
平面插画,东方幻想风格高端城市海报设计,竖版9:16构图,整体采用对角线+S型流动构图。画面以深邃黑色为背景,自上而下渐变至浓烈暗红色,形成强烈冷暖对比。画面中央一条金色流动能量线条如火焰般蜿蜒贯穿，自底部向上延伸。

金色流光中逐层浮现[城市]地标建筑群：[地标1]为视觉核心,周围融合[地标2]等建筑元素。

画面底部为一位东方白发女性形象,长发飘逸如烟似雾,与金色流光自然衔接,怀抱一束多彩鲜花。色彩以黑与暗红为基底,高亮鎏金为主视觉强调。超高清8K。
```

### 2.8 超现实锦鲤星云插画（Case 11 by @liyue_ai）
```
一幅超现实主义数字插画风格，采用低角度仰拍视角。画面描绘了一条巨型彩色锦鲤遨游在梦幻般的星云中，四周环绕着色彩鲜艳的星云与气泡。画面中央还站着一个小人，背对观众，神情平静地仰望空中这条巨大的锦鲤，锦鲤头向下看着小人。整体画面呈现出强烈的大小对比，氛围空灵又梦幻。比例9:16
```

### 2.9 新中式水墨山水海报
```
新中式水墨山水海报，竖版9:16构图，东方极简美学风格，大面积留白，主题是[主题]。
```

### 2.10 科幻电影海报
```
Create a Science fiction movie poster
```

### 2.11 梦幻水彩编辑插画
```
Ilustración en acuarela de estilo onírico de [主题], con estética impresionista ligera, pinceladas sueltas y lavados translúcidos en tonos [color1] y [color2]. Difuminado suave sobre textura de papel prensado en frío, iluminación delicada, composición limpia, enfoque minimalista, alta calidad, estilo editorial.
```

### 2.12 极透视字体大桥（Case 28 by @xpg0970）
```
①场景 [主体物（如跨海大桥）]的侧面，dramatic cinematic angle。 巨型 bold sans-serif 文字「[文字内容]」painted onto the surface of [主体物], 从靠近镜头的前端开始，沿表面向远端 progressively foreshortens 逐渐透视压缩，letterforms conform to surface curvature 贴合物体曲面。Oversized bright yellow + sharp orange outline，extreme perspective distortion aligned to vanishing point。Cinematic lighting, motion blur, poster-grade dynamic integrated typography, modern advertising aesthetics。
```

---

## 场景三：👤 角色设计

### 3.1 Persona5风格角色设定卡
```
Persona5-style character reference card for [角色名]：full body front view, side view, and back view in a clean layout. Include character stats panel, color palette swatches, and personality notes. Bold graphic design with red/black/white color scheme, sharp linework, dynamic pose, anime aesthetic
```

### 3.2 GAL游戏角色介绍页（Case 3 by @09lyco）
```
Galgame character introduction page for [角色名], [性格描述], [外观描述]. Layout includes: character full illustration on the right, name in stylized font, stat bars (cute/smart/energetic), backstory text block, relationship chart, favorite items icons. Clean pastel UI design, visual novel aesthetic
```

### 3.3 官方设定图（JP风格，Case 5 by @Toshi_nyaruo_AI）
```
Official character sheet Japanese style for [角色名]: 3 poses (front/side/back), face expression sheet (6 emotions), color palette, height comparison chart, design notes. Clean white background, professional anime production quality
```

### 3.4 机甲少女海城关键视觉（Case 7 by @old_pgmrs_will）
```
Mecha girl key visual, sea city background, dramatic sunset lighting, detailed mechanical armor design with feminine silhouette, holographic HUD elements, [配色], dynamic pose overlooking futuristic coastal megacity, cinematic composition, 8K anime illustration quality
```

### 3.5 圣斗士星矢黄金圣斗士卡片网格（Case 8 by @songguoxiansen）
```
Saint Seiya Gold Saints character card grid, 3x4 layout, each card shows: character name in Chinese and Japanese, constellation, gold cloth armor illustration, power stats, dramatic background matching their constellation theme. Golden luxury card design, epic fantasy aesthetic
```

---

## 场景四：📱 UI与社交媒体截图

### 4.1 一句话生成UI设计（Case 1 by @austinit）
```
One prompt UI design: [描述你的产品或功能]. Generate a complete, polished mobile app interface with proper hierarchy, navigation, cards, and interactive elements. Modern design system, clean typography, coherent color palette
```

### 4.2 抖音/TikTok直播截图（Case 7 by @alanblogsooo）
```
生成一张抖音直播间截图，[主播名]正在进行[内容]直播，画面里要有主播头像、弹幕、商品卡片、点赞评论数据和平台UI。真实直播截图风格，中文弹幕，粉丝数[X]万，当前在线[X]人
```

### 4.3 手写笔记本照片（Case 3 by @patrickassale）
```
Handwritten notebook photo, real paper texture, pen ink on white lined paper, handwritten notes about [主题], casual authentic handwriting style, natural lighting from above, slight shadow of hand, photorealistic
```

### 4.4 宋代社交媒体信息流（Case 4 by @Panda20230902）
```
宋代风格的社交媒体信息流截图，仿照现代社交App的界面布局，但内容全部替换为宋代风格。包含：仿微博/小红书的帖子卡片、用户头像为宋代人物画像、发帖内容为文言文、点赞评论用古代数量词、顶部状态栏维持现代手机UI。整体极具视觉冲突感和幽默感。
```

### 4.5 赛博朋克霓虹UI设计系统（Case 38 by @AZLnfvp）
```
Cyberpunk neon UI design system: dark mode interface, neon glow accents (cyan/purple/orange), glassy panels with 40% opacity, holographic data visualizations, animated gradient borders, tech-noir typography, grid layout with status indicators, futuristic HUD elements
```

### 4.6 王者荣耀/原神式游戏状态界面（Case 27 by @Kashiko_AIart）
```
Japanese RPG status screen, character [角色名], stats panel showing HP/MP/ATK/DEF/SPD with animated progress bars, equipment grid, skill icons with cooldown rings, portrait on left, background [场景], pixel art meets modern UI hybrid style, [配色方案]
```

### 4.7 glassy玻璃态UI设计系统（Case 26 by @pfanis）
```
Glassy UI design system: frosted glass morphism panels, 60% backdrop blur, white borders with 20% opacity, layered depth hierarchy, floating cards with soft shadows, minimal color accent [颜色], clean typography, modern SaaS dashboard layout
```

### 4.8 博物馆风格汉服信息图（Case 25 by @MrLarus）
```
Museum-style infographic breakdown of [服饰/文物名称]: clinical white background, specimen label typography, detailed anatomical-style illustration with component callouts, historical timeline, material list, measurement specifications. Professional academic aesthetic mixed with modern graphic design
```

### 4.9 城市旅行指南信息图（Case 29 by @MrLarus）
```
City travel guide infographic for [城市名]: illustrated map style, recommended spots with icons, food highlights, local tips, transport guide, weather chart, packing list. Modern travel magazine aesthetic, [配色], 9:16 vertical layout
```

### 4.10 麻将/历史人物X主页（Case 31 by @Cryptohaifeng_）
```
[历史人物名]的 X/Twitter 个人主页截图：真实的X界面UI，头像为该人物的历史画像或AI写实版，简介用现代语言重写该人物生平，置顶推文符合人物性格，粉丝数和关注数用对应时代规模换算，整体极具创意和幽默感
```

---

## 场景五：🌐 社区创意与娱乐

### 5.1 名人整活生活照（Sam Altman系列）
```
"[名人名] on [活动] at [地点] with no people." [photorealistic, candid snapshot style, authentic setting]
```

### 5.2 微信朋友圈整活图
```
生成 [名人名] 在微信朋友圈用中文[内容描述]，底下[名人A]评论"[内容]"，[名人B]评论"[内容]"，图片比例为 16:9
```

### 5.3 2020年历史重大事件图
```
Generate an image of the most significant event of [年份]
```

### 5.4 游戏截图混搭（Case 30 by @yssrski）
```
[游戏A] × [游戏B] crossover screenshot mashup: combine [游戏A的视觉风格] with [游戏B的游戏机制UI], seamlessly blended, photorealistic game screenshot quality, [分辨率]
```

### 5.5 AI自我认知肖像（Case 18 by @80vul）
```
根据你对我的认知，给我生成一个"你认识的我"的图片
```

### 5.6 JSON Prompt 照片重建工作流（Case 21 by @pavellaslov）
```
analyze this photo and give me a detailed JSON prompt that recreates it. break down the color grading and every exact color in the photo

[使用Opus模型分析，然后将JSON粘贴到ChatGPT，上传产品图片说：]
using this JSON as reference, generate a person holding my product
```

---

## 场景六：🛒 电商与产品

### 6.1 草莓冰淇淋超写实产品摄影（Case 23 by @ZaraIrahh）
```
Ultra-realistic product photography of a rich strawberry soft-serve ice cream in a crispy waffle cone, styled with a clean, modern premium aesthetic. The soft serve is a vibrant natural pink, thick and creamy, sculpted into a smooth swirl with a softly curled peak.
The background is soft beige with natural sunlight casting subtle leaf shadows. Include softly blurred greenery in the foreground for depth.
On the left side, include modern English typography:
Main headline: Sweet Strawberry Bliss.
Supporting line: Made with real strawberries. Smooth. Creamy. Irresistible.
Small circular badge: $5.80
Lighting: soft natural daylight, warm highlights, shallow depth of field, high-end commercial food photography style.
```

### 6.2 绿茶胶片套装产品摄影（Case 22 by @ZaraIrahh）
```
[产品名] Film Kit displayed frontally, the open box shows [颜色] [包装描述], product placed centrally with clear branding [品牌文字], pastel [颜色] background with botanical graphic accents, three minimal icons floating around the product to emphasize benefits, photographic, hyper detailed, ultra realistic, lifelike, 8k, high detail, soft professional lighting.
```

### 6.3 笔记本上的超写实UI模型（Case 24 by @ZaraIrahh）
```
A hyper-realistic UI/UX mockup displayed on a slim modern laptop placed on a minimal wooden desk with soft natural daylight. The screen shows a clean SaaS dashboard with elegant typography, glassmorphism cards, smooth gradients, subtle drop shadows, and neatly spaced components. Visible charts, analytics panels, sidebar navigation, and micro-interactions. Realistic macOS-style window frame, soft reflections on the screen, shallow depth of field, cozy workspace atmosphere, shot in photorealistic product photography style, ultra-detailed.
```

### 6.4 护肤品电商首图（完整版）
```
高端护肤品电商首图海报，产品名为 [产品名]。整体风格干净、轻奢、科学护肤感强，画面中心是一瓶[产品描述]。

海报必须包含以下文案：
[品牌名] [产品名]
[功效1] [功效2] [功效3]
[核心卖点]
核心成分 [成分列表]
适合人群 [人群]
限时到手价 [价格] [促销信息]
```

### 6.5 电商产品套图批量生成
```
根据主产品视觉图，自动迁移生成：
1. 主图白底精修
2. 场景使用图
3. 成分卖点图
4. 品牌故事长图
5. 比较对照图

产品：[描述] 品牌风格：[风格]
```

---

## 场景七：📊 信息图与科普

### 7.1 科普百科图万能模板（EvoLinkAI Case 39 by @MrLarus）
```
请根据【[主题]】生成一张高质量竖版「科普百科图」。

这张图不是普通海报，而是兼具"图鉴感、百科感、信息结构感、收藏感"的模块化科普信息图。整体风格参考高级博物图鉴、现代百科书页、生活方式知识卡和社交媒体高传播信息图的结合。

请让画面包含：
- 一个清晰漂亮的主题主视觉
- 若干局部特征放大细节
- 多个圆角模块化信息分区
- 清楚的标题层级与重点标签
- 简洁但丰富的百科内容
- 可视化评分、要点总结或 Top 5 模块

内容栏目自动适配：基础档案、分类信息、外观特征、习性/生态、养护建议、风险注意、适合人群、优缺点对比、快速评分卡。

视觉要求：浅色干净背景，柔和配色，轻阴影，精致小图标，圆角信息框，信息密度高但不拥挤。
```

> 替换技巧：将【主题】替换为任何动物、植物、产品、技术概念等。

### 7.2 旅游杂志专题文章（Case 20 by @andis13）
```
Create image of Magazine feature article [travel] guide page, cute, information dense photo book style magazine feature article page. Add all necessary sections, tips, recommendations, information. Place the attached person at the precise location of [city, country]. Seamlessly blend the attached person as if they are sightseeing. Fully use the entire [9:16] page.
```

### 7.3 人物关系图海报
```
请根据【[主题/作品名]】生成一张高设计感的人物关系图海报。
```

### 7.4 手写药方图
```
生成一张手写中/西医药方图
```

### 7.5 博物学风格食物标本解剖图（Case 68 by @GeekCatX）
```
博物学风格食物标本解剖图，以博物馆藏品标注方式展示[食物名]的横截面。白色背景，标本标签式排版，详细解剖图示配文字标注，成分比例、层次结构、历史背景、营养信息。专业学术美学融合现代平面设计
```

### 7.6 个人档案信息图表
```
Personal profile infographic generator: name [姓名], profession [职业], skills radar chart, timeline of achievements, quote section, social stats, avatar placeholder. Modern clean design, [配色方案], professional yet approachable aesthetic
```

---

## 场景八：🎬 专业视频分镜头表（Storyboard）

### 反推参考：《天空之击》动漫院线分镜（可直接复用）

```
一份专业的动漫院线分镜头（16:9），标题为《天空之击》，副标题为"战士与圣石"。

布局结构：
干净的浅米色背景，圆角矩形面板排列成三列网格，共 9 个场景。每个场景面板显示：橙色"场景 XX"标签 + 时间码 + 场景标题 + 两个并排的画面（开始帧→结束帧，白色箭头连接）+ 注释（镜头/对白/特效/动作）

艺术风格：清晰的卡通渲染，新海诚 × 工作室吉卜力 × 进击的巨人——柔和画风光线、立体云朵、温暖金色阳光、电影广角镜头、动态动作姿势、浓郁天蓝翡翠绿调，黄铜铜色点缀。

9个场景：
场景01（00:00-00:03）开场镜头·飞艇：广角——蒸汽朋克飞艇，黄铜螺旋桨和飘扬的帆，在高空穿透积云海洋。镜头：无人机慢速推入
场景02（03:00-05:05）飞艇上的战士：低角度特写——女战士靴子和交叉的双腿悬挂在飞艇木制栏杆上，风中头发飘动。镜头：静态→微微向上倾斜
场景03（05:05-07:00）鸟瞰·世界之下：鸟瞰视角——翡翠山谷，蜿蜒河流和远处茅草屋顶的中世纪村庄。镜头：眩晕变焦
场景04（07:00-10:10）圣石：飞艇桥内部——海盗船长举着发着蓝光的圣石，脸上有耀眼的青色光。镜头：中→石头放大
场景05（10:10-13:13）发现入侵者·武器就绪：满脸胡渣的海盗举起黄铜左轮手枪对准她。镜头：双枪→跟着瞄准
场景06（13:00-16:00）子弹：极近距离，旋转穿过空中，运动模糊和烟雾轨迹。镜头：子弹时间追踪
场景07（16:00-20:20）栏杆·空的：什么都没有，子弹穿过空气。镜头：快速剪辑，杂音
场景08（20:20-24:00）月面翻身：女战士在空中优雅做月面翻身，头发和斗篷在动作中拖曳。镜头：慢动作，宽→近
场景09（24:00-30:00）着陆·对峙：她悄无声息地在射手身后降落，低蹲，手放在剑柄上。镜头：低角度→对峙

底部区域：
1. 关键角色行：4个角色肖像（女战士、海盗船长、射手海盗、船员）
2. 音调与方向：动态动作、风和云粒子，吉卜力奇观与武士情感
3. 音乐SFX时间线：0-5s 环境风→1-12s 开放天空惊奇→12-16s 鼓胀→16-20s 短促张力→20-30s 屏息落地对峙
4. 技术规格：30秒，16:9 1920×1080，24fps，全彩，mp4 H.264

布局：简洁信息图，细边框，粉彩色格，每帧内高度细致动漫关键视觉，专业制作文档美学。
```

---

### 万能分镜模板（替换占位符即用）

```
一份专业的[风格]分镜头（16:9），标题为《[项目名称]》，副标题为"[副标题]"。

布局结构：
[背景色]背景，圆角矩形面板排列成三列网格，共[X]个场景。每个场景面板显示：
[强调色]"场景 XX"标签 + 时间码 + 场景标题 + 开始帧→结束帧（白色箭头）+ 注释

艺术风格：[视觉风格描述]

场景列表：
场景01（[时间码]）[场景名]：[画面描述]。镜头：[镜头语言]
场景02（[时间码]）[场景名]：[画面描述]。镜头：[镜头语言]
...（继续填写）

底部区域：
1. 关键角色：[N]个角色肖像（[角色1]、[角色2]...）
2. 音调与方向：[情绪基调描述]
3. 音乐SFX时间线：[时间段] [音效]→...
4. 技术规格：[时长]，16:9 1920×1080，[帧率]，全彩，mp4 H.264

布局：简洁信息图，细边框，粉彩色格，专业制作文档美学。
```

---

### 六大视频风格分镜快速模板

#### 🌸 动漫院线（新海诚 × 吉卜力 × 进击的巨人）
- 浅米色背景，橙色场景标签，细黑边框
- 柔和体积光、立体积云、温暖金色阳光、电影广角构图、动态姿势
- 浓郁天蓝翡翠绿调色，黄铜铜色点缀，粒子光效

#### 🎬 好莱坞真人电影
- 深灰色背景，金色"SCENE XX"标签，专业制作文档风格
- 电影摄影写实主义，变形镜头影调，胶片颗粒，景深虚化，宽银幕构图
- 脱饱和青橙调 / 金色暖调 / 冷蓝现代感

#### 🕹️ 游戏CG过场
- 深黑色背景，青色/蓝色荧光标签，科幻HUD边框
- 虚幻引擎5级别写实渲染，次表面散射皮肤，PBR材质，体积雾
- 霓虹赛博朋克 / 奇幻史诗暖金 / 科幻冷蓝

#### 📱 短视频竖版（抖音/小红书/TikTok）
- 白色背景，6面板两列网格（适配竖版），红色/粉色标签
- 真实生活感vlog / 国风古装 / 都市轻奢 / 搞笑漫画

#### 🏮 国风武侠/古装
- 宣纸米白色背景，朱红色"第XX幕"标签，水墨边框
- 水墨晕染与写实3D融合，飘逸衣袂，剑气光效
- 水墨黑白 × 朱砂红 × 翠玉绿 × 金色光晕

#### 🌌 科幻/赛博朋克
- 黑色背景，霓虹蓝紫色标签，电路纹理边框
- 赛博朋克2077 × 银翼杀手美学，霓虹反射积水路面，大气体积雾

---

### 9大镜头语言速查

| 镜头类型 | 描述关键词 | 适用场景 |
|---|---|---|
| 建立镜头 | 广角/超广角，远景，无人机拉升 | 开场，交代环境 |
| 特写镜头 | 极近距离，焦点锐利，背景虚化 | 情绪表达，细节 |
| 低角度 | 仰拍，强调力量感，天空背景 | 英雄登场，威压感 |
| 鸟瞰/俯拍 | 正上方，世界尽收眼底 | 规模感，迷失感 |
| 子弹时间 | 360度环绕，时间冻结，运动模糊 | 动作高潮 |
| 慢动作 | 时间拉伸，细节毕现，情绪加深 | 关键动作，告别 |
| 跟随镜头 | 摄影机紧随角色，手持感，沉浸 | 追逐，行动 |
| 反应镜头 | 人物面部特写，情绪捕捉 | 对话，冲突 |
| 对峙镜头 | 双人构图，对称张力 | 高潮对决 |

---

## 高级技巧速查

### 技巧1：photorealistic 是万能钥匙
> OpenAI研究员 Alex 透露：最有效的关键词就是 `photorealistic`。模型会主动规避塑料感，复刻真实照片特征。

### 技巧2：给文字，不要描述文字

```
❌ 错误：生成一张有促销信息的奶茶海报
✅ 正确：生成一张奶茶海报，品牌名为"山川茶事"，新品名为"山柚观音冷泡系列"，价格"中杯16元 大杯19元"，活动"第二杯半价"
```

### 技巧3：JSON Prompt 工作流（保持角色一致性）
1. 用 Claude Opus 分析参考照片，获得详细 JSON（色彩分级、光影参数）
2. 将 JSON 粘贴到 ChatGPT，上传产品图
3. 说：`using this JSON as reference, generate a person holding my product`
4. 保存生成的角色作为参考，之后每次生成都附上

### 技巧4：Thinking 模式使用时机
- 需要联网信息（品牌知识、人物背景）→ 开启 Thinking
- 需要多张连贯图片（穿搭系列、多图连贯）→ 开启 Thinking
- 简单出图 → Instant 模式（约3秒/张）

### 技巧5：比例选择指南

| 比例 | 适用场景 |
|---|---|
| 1:1 | 社交媒体头像、产品主图 |
| 3:4 | 海报、信息图、插画 |
| 9:16 | 手机壁纸、故事/短视频封面 |
| 16:9 | 横版视频、分镜头表 |
| 21:9 | 公众号封面、电影感横幅 |
| 3:1 | 全景图、长卷 |
| 4:5 | Instagram、小红书最优比例 |

### 技巧6：信息图黄金公式
```
模块化分区 + 圆角信息框 + 层级分明的标题
+ 浅色干净背景 + 精致小图标 + 适当留白
```

---

## GPT-Image-2 模型快速参考

| 特性 | 详情 |
|---|---|
| 发布时间 | 2026年4月22日 |
| 知识截止 | 2025年12月 |
| 最大分辨率 | 2K（API Beta） |
| 宽高比 | 3:1 ~ 1:3 |
| 单次生成 | 最多8张连贯图（Thinking模式） |
| 生成速度 | 约3秒/张（Instant模式） |
| Arena排名 | 全球第一，领先第二名240+分 |

| API画质 | 分辨率 | 输出价格 |
|---|---|---|
| Low | 1024×1024 | $8.00/1M tokens |
| Medium | 1536×1536 | $16.00/1M tokens |
| High | 2048×2048 | $32.00/1M tokens |

---

## 分镜触发流程

当用户说"gpt分镜"或"分镜提示词"时，询问：
```
1. 项目名称/标题？
2. 故事类型？（动漫/真人电影/短视频/游戏CG/国风...）
3. 多少个场景？（推荐9个/6个）
4. 总时长？（默认30秒）
5. 主要角色有哪些？
6. 关键场景或故事梗概？
```
收到后，套用对应风格模板，输出可直接复制到 ChatGPT 的完整提示词。

---

**数据来源（三库融合）**：
- 🥇 主框架：[EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) ⭐3.5k — 人像/海报/角色/UI/社区 全覆盖
- 🥈 中文实战：[xianyu110/awesome-gptimage2](https://github.com/xianyu110/awesome-gptimage2) ⭐21 — 80+中文场景提示词与框架
- 🥉 精选库：[gpt-image2/awesome-gptimage2-prompts](https://github.com/gpt-image2/awesome-gptimage2-prompts) ⭐33 — 1123条结构化提示词
- 🎬 分镜模板：反推自《SKYBOUND STRIKE》动漫院线分镜参考图
