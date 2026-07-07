---
name: portrait-prompt-architecture
description: "Build compact, modular AI portrait image prompts from reusable slots: shooting style, subject archetype, fashion style, composition, body silhouette, pose, and expression. Use when the user asks for human/portrait/K-pop/fashion/editorial photo prompts, short image prompt frameworks, prompt element libraries, style-combination prompts, or wants to turn artist/designer/literary references into concise visual language for AI image generation."
---

# Portrait Prompt Architecture

## Overview

Use this skill to create short portrait prompts with swappable high-density elements instead of long pose, lens, wardrobe, and mood descriptions. The core move is to build a stable prompt architecture, collect reference names or style traits for each slot, then recombine them into multiple concise variants.

The method is adapted from the Vibe Shot Club post "人像提示词构架思路：让你少写99%的姿势镜头服装，就能组合出片" by 迪丽热翼: https://vibeshot.club/forum/d6f2b4e3-15e1-4484-82ac-aa21a462eb6e

## Workflow

### 1. Define the prompt architecture

Start from these slots. Keep the order stable unless the user's target model responds better to another order.

```text
[shooting style / finished image effect],
[subject archetype],
[fashion or wardrobe style],
[optional composition or framing],
[body silhouette or side profile details],
[pose and expression modifiers]
```

For safety and clarity, make subjects adults when using glamorous, sensual, idol, fashion, boudoir, or body-focused language. Do not imply minors or school-age subjects in sexualized contexts.

### 2. Collect high-density reference elements

Use names, movements, media traits, or compact style phrases that carry many visual instructions at once. When a model or policy should not use a living artist/designer/style directly, translate the reference into neutral visual traits instead.

Shooting style:
- Use photographers, film stocks, camera eras, documentary modes, editorial genres, or platform-native aesthetics.
- Convert references into traits such as candid flash, private snapshot intimacy, CCD texture, direct gaze, soft grain, harsh on-camera flash, magazine editorial polish, or backstage reportage.

Fashion style:
- Use designers, fashion eras, garment construction, silhouette logic, and runway references.
- Useful axes: sculptural upper body, exaggerated shoulder line, corseted waist, hard metallic glamour, deconstructed tailoring, couture volume, asymmetry, feathering, transparent overlays, armor-like bodice, or black runway minimalism.

Composition and literary atmosphere:
- Convert writers or literary moods into visual camera language.
- Examples of translation: shadow and negative space, obsessive close observation, dreamlike softness, restrained emptiness, golden luxury, intimate interior framing, or quiet off-center composition.

Body, pose, and expression:
- Describe silhouette and posture as visual design, not anatomy fixation.
- Prefer performance cues: chin angle, shoulder tension, weight shift, hand placement, micro-smile, direct stare, half-turned torso, runway stillness, candid interruption, or playful eye contact.

### 3. Build short combinations

Combine one or two strong references per prompt. Avoid stacking too many famous names; it can muddy the result. Prefer 3-6 comma-separated clauses.

Template:

```text
[shooting style], adult [subject archetype], [fashion style], [composition/atmosphere], [pose/expression]
```

Example pattern:

```text
candid CCD flash fashion portrait, adult K-pop editorial model, sculptural couture upper-body silhouette, intimate off-center framing with deep shadow, direct gaze and relaxed half-smile
```

### 4. Produce variants

When the user asks for prompts, output:

- A slot breakdown if they are still exploring.
- 6-12 compact prompt variants if they want usable prompts.
- A small "element bank" if they want to keep remixing.
- A stricter final prompt if they need one polished image direction.

## Output Format

For most requests, answer in Chinese unless the user asks otherwise.

Use this compact structure:

```markdown
## 架构
拍摄风格 / 人物 / 服装 / 构图 / 身材侧写 / 动作表情

## 元素库
- 拍摄风格：
- 服装风格：
- 构图气质：
- 动作表情：

## 组合提示词
1. ...
2. ...
3. ...
```

If the target is GPT Image or another natural-language model, keep prompts readable and phrase-like. Do not force JSON unless the user asks for it.
