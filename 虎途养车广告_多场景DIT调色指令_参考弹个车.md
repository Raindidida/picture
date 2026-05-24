# 虎途养车广告 多场景 DIT 调色指令

参考视频：`弹个车：我们没有想卖车给你 [P4IIL2EygF4].mp4`

适配分镜源文件：`虎途养车广告_2分10秒_分镜头表_GPTImage2_MJ提示词.md`

## 参考片实测母版

- 统计范围：9 个叙事取样帧，共 `437,760 px`；裁除底部字幕区与片尾图文卡。
- 色彩管理参考：`BT.709 / TV range / 8-bit`。
- 阴影均值：`RGB(28,38,44)`，占比 `43.83%`。
- 中间调均值：`RGB(103,127,112)`，占比 `44.75%`。
- 高光均值：`RGB(193,222,202)`，占比 `11.42%`。
- Black Point：`3.35 / 255`；近黑剪切 `1.332%`。
- White Point：`242.17 / 255`；近白剪切 `0.207%`。
- 对比度目标：`14.45 : 1`；显示文件亮度跨度估算 `5.81 stops`。
- 母版关键色：`#22231A`、`#223F4C`、`#B4D0BE`、`#4E8A9F`、`#8A7A48`。
- 通用光学锁定：`natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening`。

> 以下各组参数是基于参考片实测母版、按本广告不同空间重新分配的目标调色值，用于 AI 生图/重绘控制，不是各未生成场景的实拍测量值。

## CG-01 地下停车场 / 车内冷光

适用镜头：`1-5`；适用底图：`MJ-S01`。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 阴影 RGB / 占比 | `RGB(22,35,44)` / `48-55%` |
| 中间调 RGB / 占比 | `RGB(83,112,113)` / `34-40%` |
| 高光 RGB / 占比 | `RGB(176,207,199)` / `8-12%` |
| Black Point / White Point | `3-5 / 255` / `232-242 / 255` |
| 对比度 / 亮度跨度 | `15:1-17:1` / `5.8-6.1 stops` |
| 主光 / 辅光 | `4:1`，约 `2 stops` |

### 核心 HEX 色板

- 主色调：`#16232C`
- 辅色调：`#536F71`
- 点缀色：`#B0CFC7`
- 阴影色：`#1D3442`
- 反差物体保留色：`#7D3B32`

### 调色指令(Color Grading)

```text
地下车库夜景，采用 BT.709 中低键冷色控制。将阴影压至 RGB(22,35,44)，阴影蓝通道高于红通道约 +22；中间调控制在 RGB(83,112,113)，保持青绿混合而非纯蓝；荧光灯照明高光限制在 RGB(176,207,199)，不出现纯白灯管大面积剪切。暗部占比 48-55%，高光不超过 12%。Black Point 设定 3-5/255，White Point 限制 232-242/255，对比度 15:1-17:1。红色物件只保留低饱和砖红 #7D3B32，避免抢夺暗冷主调。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
只使用顶部冷白荧光灯与车辆现场微弱反射作为可见光源；主光色温目标 4300-4800K，绿色偏移轻微增加；辅光来自湿地反射与车内弱环境光。主辅光比约 4:1。地面反射峰值不超过 225/255，灯管周边添加小范围 film halation，不增加轮廓灯。
```

### 负向指令(Negative Prompt)

```text
避免赛博霓虹蓝、过饱和青色、商业汽车棚拍亮边、纯白地面反射、灯管死白过曝、车漆镜面无灰尘、HDR 锐利边缘、数字锐化光晕、塑料皮肤、过强红色车漆、可读文字、水印、logo。
```

## CG-02 高档公寓门厅 / 暗金压迫

适用镜头：`6-7`；适用底图：`MJ-S02`。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 阴影 RGB / 占比 | `RGB(37,31,27)` / `42-48%` |
| 中间调 RGB / 占比 | `RGB(113,89,63)` / `40-46%` |
| 高光 RGB / 占比 | `RGB(214,186,131)` / `8-12%` |
| Black Point / White Point | `5-8 / 255` / `235-244 / 255` |
| 对比度 / 亮度跨度 | `13:1-15:1` / `5.5-5.9 stops` |
| 主光 / 辅光 | `3.5:1`，约 `1.8 stops` |

### 核心 HEX 色板

- 主色调：`#71593F`
- 辅色调：`#3A312B`
- 点缀色：`#D6BA83`
- 阴影色：`#251F1B`
- 过渡色：`#8A704F`

### 调色指令(Color Grading)

```text
室内门厅改为受控暗金色域，阴影 RGB(37,31,27)，保持红通道略高于蓝通道但不偏橙；中间调 RGB(113,89,63)，将木饰面与肤色归入同一低饱和暖调；壁灯与局部皮肤高光控制在 RGB(214,186,131)。暗部占比 42-48%，亮部低于 12%。Black Point 保留 5-8/255，防止黑色服装失去纹理；White Point 不超过 244/255。整体对比度 13:1-15:1，降低冷蓝填充，仅在门外或玻璃边缘保留极小面积冷色互补。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
主光来自暖色壁灯与门厅顶灯，目标 2800-3300K；人物背阴面用极弱环境反射补光，不增加美容柔光。主辅光比约 3.5:1。大理石高光形成窄面积暖色反射，局部峰值低于 240/255；暗木墙面保持纹理可读。
```

### 负向指令(Negative Prompt)

```text
避免金黄色过饱和、豪宅广告式均匀补光、肤色橙化、黑色西装压成纯黑块、灯具大面积白爆、泛蓝环境光、过度柔焦、蜡质皮肤、奢侈品海报质感、可读文字、水印、logo。
```

## CG-03 商务 MPV / 公司门口记者围堵

适用镜头：`8-10`；适用底图：`MJ-S03`。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 阴影 RGB / 占比 | `RGB(25,34,40)` / `38-44%` |
| 中间调 RGB / 占比 | `RGB(91,110,105)` / `38-44%` |
| 闪光高光 RGB / 占比 | `RGB(220,232,222)` / `14-18%` |
| Black Point / White Point | `3-5 / 255` / `245-250 / 255` |
| 对比度 / 亮度跨度 | `16:1-19:1` / `6.0-6.4 stops` |
| 环境主光 / 闪光峰值 | `1:5` 瞬态峰值 |

### 核心 HEX 色板

- 主色调：`#192228`
- 辅色调：`#5B6E69`
- 点缀色：`#DCE8DE`
- 阴影色：`#203743`
- 过渡色：`#728987`

### 调色指令(Color Grading)

```text
MPV 车内至记者围堵段保持母版青绿阴影，但允许闪光灯制造短暂高白峰值。阴影 RGB(25,34,40)，中间调 RGB(91,110,105)，相机闪光照亮的人脸与车身高光控制在 RGB(220,232,222)。Black Point 3-5/255；White Point 允许达到 245-250/255，但亮区剪切面积不得超过 0.8%。高光占比 14-18%，对比度提高至 16:1-19:1。闪光不改变整体冷绿中间调基准。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
车内使用车窗自然入光与屏幕弱反射；室外使用阴天天光作为环境底光，叠加记者相机瞬时闪光。环境主辅光约 3:1；闪光峰值相对填充可达约 5:1。闪光灯只在脸部、玻璃、车漆形成不连续高光斑，并产生克制的 halation，不把背景整体提亮。
```

### 负向指令(Negative Prompt)

```text
避免持续棚拍大平光、闪光导致全画面死白、玻璃幕墙纯蓝化、新闻画面数字锐利感、强 HDR、过分清晰毛孔、过饱和口红或肤色、大片面积纯白、可读麦标、字幕、水印、logo。
```

## CG-04 乡下父亲院子 / 情绪落地自然光

适用镜头：`11-13`；适用底图：`MJ-S04` 与父亲关键视觉。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 阴影 RGB / 占比 | `RGB(53,55,43)` / `28-35%` |
| 中间调 RGB / 占比 | `RGB(131,126,91)` / `48-55%` |
| 高光 RGB / 占比 | `RGB(220,208,158)` / `12-18%` |
| Black Point / White Point | `10-14 / 255` / `238-246 / 255` |
| 对比度 / 亮度跨度 | `8:1-10:1` / `4.9-5.4 stops` |
| 主光 / 辅光 | `2:1`，约 `1 stop` |

### 核心 HEX 色板

- 主色调：`#837E5B`
- 辅色调：`#6C754E`
- 点缀色：`#DCD09E`
- 阴影色：`#35372B`
- 过渡色：`#A89C70`

### 调色指令(Color Grading)

```text
乡下院子段主动释放前段压黑：阴影抬至 RGB(53,55,43)，中间调 RGB(131,126,91)，高光 RGB(220,208,158)。阴影不注入明显蓝色，转为低饱和中性绿褐。Black Point 抬到 10-14/255，保留旧墙、布料与皮肤纹理；White Point 238-246/255，允许阳光区域发亮但不剪切。暗部占比降至 28-35%，中间调占比提高到 48-55%，对比度降低至 8:1-10:1。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
使用傍晚自然侧光，目标色温 4800-5600K；主光为天空与斜入院子的阳光，辅光来自地面和旧墙漫反射。主辅光比约 2:1。面部与手部亮度过渡平缓，轮廓边缘不增加人工逆光。亮部只在布料、金属边缘和湿润眼部形成小面积柔和高光。
```

### 负向指令(Negative Prompt)

```text
避免夕阳橙滤镜、过度煽情金光、青蓝阴影残留、硬边阳光、死黑室内门洞、过曝天空、锐化皱纹、过度磨皮、油画化狗毛或皮肤、广告级洁净院落、可读文字、水印、logo。
```

## CG-05 交通变身蒙太奇 / 运动危险感

适用镜头：`13-17`；适用底图：`MJ-S05` 与 Fast Montage Key Visual。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 阴影 RGB / 占比 | `RGB(20,30,37)` / `40-50%` |
| 中间调 RGB / 占比 | `RGB(79,104,99)` / `34-42%` |
| 高光 RGB / 占比 | `RGB(188,211,190)` / `10-15%` |
| Black Point / White Point | `2-4 / 255` / `238-247 / 255` |
| 对比度 / 亮度跨度 | `16:1-18:1` / `6.0-6.3 stops` |
| 主光 / 辅光 | `4:1-5:1` |

### 核心 HEX 色板

- 主色调：`#141E25`
- 辅色调：`#4F6863`
- 点缀色：`#BCD3BE`
- 阴影色：`#233B48`
- 过渡色：`#778E72`

### 调色指令(Color Grading)

```text
交通快速蒙太奇以冷青阴影统一不同地点，使镜头切换保持综合色彩连续。阴影 RGB(20,30,37)，中间调 RGB(79,104,99)，高光 RGB(188,211,190)。Black Point 2-4/255，对比度 16:1-18:1，允许快速运动画面中的窄面积深黑与高亮交替，但 White Point 保持低于 247/255。降低暖色饱和度，将天空、玻璃、金属、车内暗部归入 #233B48 与 #4F6863 范围。运动模糊不影响黑位与色相稳定性。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
每个空间仅使用其真实可见光源：天空散射光、驾驶室窗外日光、车内环境反射、城市路面自然光。主辅光比控制在 4:1-5:1。高速切换段通过明暗方向与冷青暗部统一，而非用彩色特效光连接；高光边缘加入有限 halation，运动模糊保持光迹真实。
```

### 负向指令(Negative Prompt)

```text
避免科幻传送特效色、霓虹光轨、彩虹色复眼、过度鱼眼变形、视频游戏式运动模糊、纯黑吞细节、天空死白、车辆反射过亮、HDR 纹理、数字锐化、可读文字、水印、logo。
```

## CG-06 虎途门店 / 品牌收束实景光

适用镜头：`18`；适用底图：`MJ-S06` 与 Hero Key Visual。

### 目标参数

| 项目 | 目标值 |
|---|---:|
| 室外阴影 RGB / 占比 | `RGB(30,45,52)` / `24-32%` |
| 门店中间调 RGB / 占比 | `RGB(133,148,130)` / `44-52%` |
| 工位高光 RGB / 占比 | `RGB(222,229,206)` / `18-24%` |
| Black Point / White Point | `6-10 / 255` / `242-248 / 255` |
| 对比度 / 亮度跨度 | `10:1-12:1` / `5.3-5.7 stops` |
| 门店主光 / 室外填充 | `2.5:1-3:1` |

### 核心 HEX 色板

- 主色调：`#859482`
- 辅色调：`#1E2D34`
- 点缀色：`#DEE5CE`
- 阴影色：`#263E48`
- 过渡色：`#A3B29A`

### 调色指令(Color Grading)

```text
结尾门店段在保留冷色夜景外框的同时，提高工位曝光与中间调占比。室外阴影控制为 RGB(30,45,52)，门店中间调 RGB(133,148,130)，工位灯与车辆受光面高光 RGB(222,229,206)。Black Point 6-10/255，不回到前段死黑；White Point 242-248/255，高光占比允许达到 18-24%，但工具、轮胎、车辆材质必须保留层次。室外冷色与室内中性暖绿形成同一母版体系内的收束。natural lighting, soft optical lens quality, film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening.
```

### 布光指令(Lighting)

```text
门店内部使用真实工位灯和顶灯作为主光，色温目标 4000-4500K；街道夜色只作低亮度冷色填充。主辅光比约 2.5:1-3:1。车辆白色漆面保留 RGB(210-235) 的纹理区间，金属工具亮点控制在 248/255 以下；门玻璃只出现柔和反射，不生成硬质广告光带。
```

### 负向指令(Negative Prompt)

```text
避免电商白底棚拍质感、门店整体纯白过曝、过饱和品牌色、轮胎黑位无纹理、白色车漆剪切、人工蓝橙对撞、金属高光锐利爆点、过度降噪、过度锐化、廉价 LED 青白偏色、可读文字、水印、logo。
```

## 连贯性使用规则

| 段落 | 影调走向 | Black Point | 高光上限 | 色彩意图 |
|---|---|---:|---:|---|
| 镜头 1-5 | 冷、暗、压低 | `3-5` | `242` | 困顿现实 |
| 镜头 6-7 | 暗暖、压迫 | `5-8` | `244` | 权力诱惑与不安 |
| 镜头 8-10 | 冷绿、闪光冲击 | `3-5` | `250` | 暴露与失控 |
| 镜头 11-13 | 暖中性、抬黑 | `10-14` | `246` | 情绪落地 |
| 镜头 13-17 | 冷、快速、高反差 | `2-4` | `247` | 运动与危险 |
| 镜头 18 | 内亮外冷、放开中间调 | `6-10` | `248` | 现实收束 |

## 统一追加尾缀

将以下尾缀追加到任意场景生图或重绘提示词末尾：

```text
Color managed cinematic still, BT.709 display-referred target, natural lighting, soft optical lens quality, subtle film halation around highlights, Kodak Portra 400 grain, low contrast edges, analog photography style, realistic skin texture without over-sharpening, restrained saturation, preserve material detail, no HDR sharpness, no plastic skin, no text, no watermark.
```
