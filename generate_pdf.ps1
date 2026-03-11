
# 生成 Nano Banana Pro 7 Tips PDF 文档
$outputPath = "d:\desktop\picture prompt\Nano_Banana_Pro_7Tips.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()
$selection = $word.Selection

# 设置页面边距
$doc.PageSetup.TopMargin = $word.InchesToPoints(1)
$doc.PageSetup.BottomMargin = $word.InchesToPoints(1)
$doc.PageSetup.LeftMargin = $word.InchesToPoints(1.2)
$doc.PageSetup.RightMargin = $word.InchesToPoints(1.2)

# 辅助函数：写入带样式的段落
function Write-Heading1 {
    param([string]$text)
    $selection.Style = $doc.Styles["Heading 1"]
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Write-Heading2 {
    param([string]$text)
    $selection.Style = $doc.Styles["Heading 2"]
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Write-Heading3 {
    param([string]$text)
    $selection.Style = $doc.Styles["Heading 3"]
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Write-Normal {
    param([string]$text)
    $selection.Style = $doc.Styles["Normal"]
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Write-Bullet {
    param([string]$text)
    $selection.Style = $doc.Styles["List Bullet"]
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Write-BlankLine {
    $selection.Style = $doc.Styles["Normal"]
    $selection.TypeParagraph()
}

# ============================================================
# 标题页
# ============================================================
Write-Heading1 "7 Tips to Get the Most Out of Nano Banana Pro"
Write-Normal "来源：Google Keyword Blog | 作者：Bea Alessio，Google DeepMind 集团产品经理"
Write-Normal "发布日期：2025 年 11 月 20 日 | 整理日期：2026 年 2 月 27 日"
Write-BlankLine

Write-Normal "Nano Banana Pro（即 Gemini 3 Pro Image）是 Google 基于 Gemini 3 构建的最先进图像生成模型，支持多语言文字渲染、多达 14 张图像的混合合成、专业级控制编辑等能力，可在 Gemini 应用、AI Studio、Vertex 等平台中使用。本文档将官方 7 大提示技巧进行系统整理，帮助您快速掌握高质量出图的方法。"
Write-BlankLine

# ============================================================
# 第一部分：构建核心视觉要素
# ============================================================
Write-Heading2 "第一部分：构建核心视觉要素——故事、主体与风格"
Write-Normal "要获得最佳效果并拥有更精细的创作控制，提示词（Prompt）应包含以下六大要素："
Write-BlankLine

Write-Bullet "主体（Subject）：图像中有谁或什么？要具体描述。例如：'一个眼睛发出蓝光的冷静机器人咖啡师'；'戴着小巫师帽的蓬松玳瑁猫'。"
Write-Bullet "构图（Composition）：镜头如何取景？例如：极端特写、广角镜头、低角度拍摄、人像构图。"
Write-Bullet "动作（Action）：画面中发生了什么？例如：正在冲泡咖啡、施展魔法咒语、在原野上奔跑。"
Write-Bullet "场景/位置（Location）：场景发生在哪里？例如：火星上的未来主义咖啡馆、杂乱的炼金术士图书馆、黄金时刻阳光明媚的草地。"
Write-Bullet "风格（Style）：整体美学风格是什么？例如：3D 动画、黑色电影、水彩画、照片写实、1990 年代产品摄影。"
Write-Bullet "编辑指令（Editing Instructions）：修改现有图像时，要直接且具体。例如：'把男士领带改成绿色'；'去掉背景中的汽车'。"
Write-BlankLine

# ============================================================
# 第二部分：精细化细节
# ============================================================
Write-Heading2 "第二部分：精细化细节——相机、灯光与格式"
Write-Normal "简单的提示词仍然有效，但要达到专业级效果，需要更具体的指令。在撰写提示词时，请考虑以下进阶要素："
Write-BlankLine

Write-Bullet "构图与画面比例（Composition & Aspect Ratio）：定义画布。例如：'9:16 竖版海报'；'21:9 宽幅电影镜头'。"
Write-Bullet "相机与灯光细节（Camera & Lighting）：像电影摄影师一样执导拍摄。例如：'低角度拍摄，浅景深（f/1.8）'；'黄金时刻的逆光，投射出长长的阴影'；'带有低调青色调的电影级色彩分级'。"
Write-Bullet "特定文字整合（Text Integration）：清晰说明文字应出现的位置和样式。例如：'顶部以粗体、白色、无衬线字体显示标题 URBAN EXPLORER'。"
Write-Bullet "事实约束（Factual Constraints）：对于图表类内容，指定准确性需求并确保输入本身是事实性的。例如：'科学准确的横截面图示'；'确保维多利亚时代的历史准确性'。"
Write-Bullet "参考输入（Reference Inputs）：上传图像时，明确定义每张图的作用。例如：'使用图像 A 提供角色姿势，图像 B 提供艺术风格，图像 C 提供背景环境'。"
Write-BlankLine

# ============================================================
# 七大技巧详解
# ============================================================
Write-Heading2 "第三部分：七大技巧详解与示例"
Write-BlankLine

# Tip 1
Write-Heading3 "技巧 1：生成带有出色文字渲染的图像"
Write-Normal "Nano Banana Pro 支持清晰、可读的文字嵌入，助您创作震撼人心的海报、精密的图表，甚至是详细的产品模型。"
Write-Normal "适用场景：品牌海报、信息图、产品包装设计、活动宣传图。"
Write-Bullet "提示示例：'创建一张信息图，展示如何制作 elaichi chai（豆蔻奶茶）'"
Write-Bullet "提示示例：'创建一张图，用木头拼出短语 How much wood would a woodchuck chuck...，由土拨鼠来制作'"
Write-BlankLine

# Tip 2
Write-Heading3 "技巧 2：运用真实世界知识创作"
Write-Normal "Nano Banana Pro 基于 Gemini 3 Pro 构建，能够调用 Gemini 3 的真实世界知识和深度推理能力，生成精确、细腻、信息丰富的图像结果。"
Write-Normal "适用场景：科普示意图、历史场景还原、技术架构图、事实性图示。"
Write-Bullet "优势：无需提供额外参考资料，模型本身具备广博知识储备"
Write-Bullet "建议：对于数据驱动的可视化，始终验证事实准确性"
Write-BlankLine

# Tip 3
Write-Heading3 "技巧 3：翻译与本地化您的创意"
Write-Normal "生成本地化文字，或翻译图像中的文字内容。预览产品在多语言市场中的外观，为不同地区创建海报和信息图。"
Write-Normal "适用场景：多语言营销材料、国际化产品包装、跨区域广告素材。"
Write-Bullet "提示示例：'将三个黄蓝相间的易拉罐上的所有英文翻译成韩文，其他内容保持不变'"
Write-Bullet "注意：多语言文字生成可能出现语法错误或遗漏特定文化语境"
Write-BlankLine

# Tip 4
Write-Heading3 "技巧 4：使用影视级专业控制编辑"
Write-Normal "获得广泛的专业级控制，直接影响灯光和相机设置，包括角度、焦点、色彩分级等。"
Write-Normal "适用场景：产品渲染、广告图片、社交媒体内容、品牌视觉物料。"
Write-Bullet "提示示例：'将这个场景改为夜晚'"
Write-Bullet "提示示例：'聚焦在花朵上'"
Write-Bullet "可控参数：光线方向与强度、镜头焦距与景深、色彩分级与滤镜、场景时间与天气"
Write-BlankLine

# Tip 5
Write-Heading3 "技巧 5：精准调整尺寸与分辨率"
Write-Normal "试验不同的画面比例，在各种产品上以 1K、2K 或 4K 分辨率生成清晰的视觉效果。"
Write-Normal "适用场景：多平台内容适配、印刷品、高清大图展示。"
Write-Bullet "支持分辨率：1K / 2K / 4K"
Write-Bullet "灵活调整比例，通过改变画面比例适配不同平台（如 1:1 方图、16:9 横图、9:16 竖图）"
Write-Bullet "提示示例：'将这张图调整为 9:16 格式并提升至 4K 分辨率'"
Write-BlankLine

# Tip 6
Write-Heading3 "技巧 6：多图融合，保持多角色一致性"
Write-Normal "保持多个角色的一致性与形象，即使他们一同出现在群像中。可以将多达 6-14 张（根据平台不同而异）完全不相关的图像融合，创作出新的作品。"
Write-Normal "适用场景：角色一致性维护、多图合成创作、品牌形象统一。"
Write-Bullet "输入图像数量：最多 6-14 张（不同平台有所差异）"
Write-Bullet "提示示例：'将这些图像合并为一张 16:9 格式的合适电影感图像，并将人台架上的连衣裙换成图像中的那件'"
Write-Bullet "技巧：明确说明每张参考图的用途（角色姿势、风格参考、背景素材）"
Write-BlankLine

# Tip 7
Write-Heading3 "技巧 7：打造并维护您的品牌视觉形象"
Write-Normal "以一致的品牌风格渲染和应用设计，轻松将概念可视化。将图案、Logo 和艺术作品无缝附着到服装、包装等 3D 物体和表面上，同时保持自然的光线和纹理效果。"
Write-Normal "适用场景：品牌识别系统、产品包装设计、品牌周边物料、广告 Mockup。"
Write-Bullet "能力亮点：将 Logo/图案映射到真实 3D 产品表面"
Write-Bullet "保持品牌色彩、字体、风格的跨图一致性"
Write-Bullet "提示示例（两步流程）："
Write-Bullet "  第一步：'创建一个基于草图风格的光滑 Logo，采用 1960-70 年代迷幻复古风格排版，单词 WAVE 排列成波浪轮廓，浅蓝色背景配深蓝色 Logo...'"
Write-Bullet "  第二步：'现在逐一创建品牌识别系统，用 10 张高质量 Mockup，包含各种相关产品、广告、广告牌、公交站等，每次生成一张，每张 16:9'"
Write-BlankLine

# ============================================================
# 当前限制
# ============================================================
Write-Heading2 "第四部分：当前已知局限性"
Write-Normal "Google 团队正在持续改进模型，目前仍有以下方面需要注意："
Write-BlankLine

Write-Bullet "视觉与文字保真度：渲染小字、精细细节，以及生成准确拼写可能不完美。"
Write-Bullet "数据与事实准确性：始终验证图表、信息图等数据驱动型可视化内容的事实准确性。"
Write-Bullet "翻译与本地化：多语言文字生成可能出现语法错误或遗漏特定文化语境。"
Write-Bullet "复杂编辑与图像融合：高级编辑任务（如融合或灯光变化）有时会产生不自然的伪影。"
Write-Bullet "角色特征一致性：虽然通常可靠，但跨编辑的角色一致性可能存在差异。"
Write-BlankLine

# ============================================================
# 快速参考总览
# ============================================================
Write-Heading2 "第五部分：7 大技巧快速参考总览"
Write-BlankLine

Write-Bullet "技巧 1 - 文字渲染：生成包含清晰文字的图像，适用于海报、图表、产品 Mockup"
Write-Bullet "技巧 2 - 真实知识：利用 Gemini 3 知识库生成精准信息图和事实性图示"
Write-Bullet "技巧 3 - 翻译本地化：翻译图像内文字，生成多语言版本营销素材"
Write-Bullet "技巧 4 - 专业控制：调整灯光、角度、色彩分级等，达到影视级专业效果"
Write-Bullet "技巧 5 - 尺寸精控：支持 1K/2K/4K 分辨率，灵活调整多平台画面比例"
Write-Bullet "技巧 6 - 多图融合：最多 14 张图合成，多角色同框保持形象一致性"
Write-Bullet "技巧 7 - 品牌形象：统一品牌风格，将 Logo 映射到 3D 产品表面"
Write-BlankLine

Write-Normal "---"
Write-Normal "原文来源：https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/"
Write-Normal "文档整理：AI Assistant | 整理日期：2026 年 2 月 27 日"

# 保存为 PDF
$doc.SaveAs([ref]$outputPath, [ref]17)  # 17 = wdFormatPDF
$doc.Close()
$word.Quit()

Write-Host "PDF 已生成：$outputPath"
