---
name: storyboard-prompt
description: Generate cinematic storyboard sketch prompts for GPT Image or similar image models from character references and optional scene references. Use when the user asks for storyboard prompts, storyboard sheets, cinematic panels, action previs, rough animation thumbnails, Chinese storyboard prompt requests, rough storyboard sketches, storyboardv2 prompts, or scene prompts when no scene reference is provided. Supports character-only inputs, character plus scene references, action/performance/sports/fantasy sequences, 16:9 multi-panel storyboard sheets, black-and-white line storyboard panels with colored production annotations, clean graphite-gray storyboardv2 modes, camera logic, motion progression, and panel-by-panel shot lists.
---

# Storyboard Prompt

Use this skill to turn a user's character and optional scene references into a production-style storyboard prompt. Output a prompt the user can paste into GPT Image or another image model.

## Core Decision

1. If the user provides both character and scene references, generate a complete storyboard prompt that explicitly uses both references.
2. If the user provides a character reference but no scene reference, first generate a concise scene prompt section, then include that scene inside the storyboard prompt.
3. If the user provides no references, write a self-contained storyboard prompt from the user's concept and ask for references only if identity consistency is essential.

## Required Output Shape

Default all storyboard prompts to Chinese unless the user explicitly asks for English or another language. Keep fixed tool-facing labels such as `GPT Image 2 Storyboard Prompt:` or `GPT Image 2 Prompt for storyboard:` in English if useful, but write the actual prompt body, shot descriptions, notes, constraints, and reference-use sentence in Chinese by default.

Default v1 storyboard output to the template-style structure below:

- `GPT Image 2 Storyboard Prompt:`
- 16:9 storyboard sheet
- 12 cinematic panels
- 3x4 grid
- black-and-white rough line storyboard drawings
- grayscale sketch panels on warm off-white or neutral storyboard paper
- colored handwritten production annotations are included by default
- panel drawings stay black-and-white; annotation marks may use color
- no timestamps, dialogue, logos, watermark, subtitles, or extra UI unless requested

Use the user's requested panel count, grid, aspect ratio, style, language, or tool target when specified.

## V1 Template Structure

Use this exact section order for normal v1 storyboard prompts:

```text
GPT Image 2 Storyboard Prompt:

[STORYBOARD]:
TITLE: [TITLE]
TYPE: [GENRE / SEQUENCE TYPE]
ASPECT RATIO: 16:9
PANEL COUNT: 12
GRID: 3x4

[LOOK]:
Create a rough cinematic storyboard focused entirely on planning, staging and motion readability rather than illustration quality.
Use loose hand-drawn pencil and ink strokes, quick construction lines, gesture drawing and simplified masses.
Characters and environments should be built from basic forms rather than finished drawings.
Keep characters semi-abstract with minimal facial information and simplified costumes.
Indicate environments rather than illustrating them.
Represent the scene space, floor plane, foreground/background layers, props, atmosphere and key interaction elements using only the minimum shapes required for orientation and interaction.
Allow rough unfinished strokes, broken lines, visible construction and sketch overlap.
Do not clean the drawing.
Prioritize timing, motion, staging and readability over appearance.
Avoid texture rendering, materials, lighting, clothing folds, decorative linework and production illustration quality.
The storyboard should feel like rough animation thumbnails, action planning boards, animatic preparation sketches and first-pass previs notes rather than concept art.
No timestamps.

[DETAIL LEVEL]:
low-to-medium detail
semi-mannequin characters
gesture-driven poses
strong silhouette readability

[PACE / MOTION LOGIC]:
[Fast-paced or genre-appropriate motion logic. Explain how the sequence escalates, what action system drives it, and how transitions stay active.]

[COLOR LOGIC]:
Keep the base storyboard grayscale.
All annotations must follow the color key below.

[ANNOTATION KEY]:
RED = camera / lens / framing / camera movement
BLUE = body movement / path / turn / jump / fall / pose flow
GREEN = key prop path / object movement / transformation flow
ORANGE = burst / snap / impact / vibration / visual accent / light accent
PURPLE = timing / acceleration / hold / speed change

[ARROW / MARK STYLE]:
Draw annotation arrows and marks as visible production notes over the storyboard.
Use thin hand-drawn arrows rather than clean vector graphics.
Use curved arrows for spins, arcs, turns, orbital motion and object flow.
Use straight arrows for direct movement and push-in direction.
Use dashed arrows for anticipated motion and trailing continuation.
Keep annotations readable and functional.
Do not cover face, hands or key silhouette reads.

[WORLD]:
[Concise scene and environment description. Keep the world minimal enough for action readability while preserving spatial continuity, scale, props, floor plane and background cues.]

[CAST]:
[Character identities, reference use, silhouettes, costume language, personality and motion language.]

[DIRECTORIAL LANGUAGE]:
[Cinematic framing, shot variety, camera movement, transitions and escalation logic.]

[OPENING / ENDING LOGIC]:
[Immediate opening hook and active ending requirement.]

[BOARD RULES]:
Use large readable panel numbers in the top-left corner.
Keep shot subtitles and notes readable.
Each panel must show one clear action beat.
Preserve spatial continuity.
Avoid repeated camera angles unless intentional.
Keep the sheet readable at a glance.
No dialogue, subtitles, logos, watermarks or decorative UI.

[SHOT NOTE RULES]:
Each panel includes a short note explaining purpose, transition value or visual idea.
Keep notes brief.

[SEQUENCE FORMAT]:
[NUMBER] - [SHOT NAME]
SHOT NOTE:
[Short cinematic note]
camera:
action:
focus:
------------------------------------------------

[SEQUENCE]:
1 - [SHOT NAME]
SHOT NOTE:
[Short cinematic note]
camera:
[Camera note]
action:
[One clear action beat]
focus:
[Primary read]
------------------------------------------------
```

For v1, always write the full `[SEQUENCE]` with 12 numbered panels unless the user asks for a different panel count.

## Storyboardv2 Mode

Use `storyboardv2` mode when the user explicitly asks for storyboardv2, provides a single dense GPT Image prompt as a template, asks for a premium rough-sketch storyboard sheet, or requests a clean storyboard sheet where technical information lives outside the panels.

Storyboardv2 defaults:

- Start with `GPT Image 2 Prompt for storyboard:`
- Write the storyboardv2 prompt body in Chinese by default unless the user explicitly requests English.
- Generate one compact paragraph prompt unless the user asks for a panel-by-panel list.
- Clean 16:9 premium rough-sketch storyboard sheet.
- Low-detail graphite-gray, black-and-white semi-mannequin planning sketches on warm off-white paper.
- Keep storyboard panels as gray line drawings only, not finished concept art.
- A compact artistic project card near the top.
- A continuity/style strip near the top with tiny final-video look swatches.
- A 10-panel storyboard grid unless the user requests another count.
- A bottom director strip for timing, camera, lens, technical notes, shot order, and continuity notes.
- No arrows, motion lines, captions, labels, dialogue, logos, watermarks, UI overlays, subtitles, or production notes inside the panel images.
- All timing, camera and technical information must be in the director strip only.
- If color is needed, limit it to tiny style swatches or VFX/color notes outside the panels, not within the storyboard panels.
- End the prompt with a short Chinese reference-use sentence when needed, for example: `仅将参考图用于视频分镜与视觉一致性。`

Storyboardv2 prompt structure:

```text
GPT Image 2 Prompt for storyboard:

Create a clean 16:9 premium rough-sketch storyboard sheet for [TITLE], a [DURATION] [GENRE / ACTION TYPE]: [CHARACTERS] in [SCENE], with [KEY PROPS / ENVIRONMENT DETAILS / PHYSICAL HAZARDS]. Use Image #1 for [reference role] and Image #2 for [reference role]; storyboard panels must stay low-detail graphite-gray black-and-white semi-mannequin planning sketches on warm off-white paper, while tiny style swatches near the top show the final-video look: [lighting, palette, shadow style, VFX/material cues]. Include a compact artistic project card, continuity/style strip, [PANEL COUNT]-panel storyboard grid and bottom director strip, keeping all timing, camera and technical info only in the director strip; no arrows, motion lines, captions, notes, labels, dialogue, logos, watermarks or overlays inside panel images. The sequence starts with [opening beat], then escalates through [middle action progression]; the final beat must be unmistakable: [ending image].

*Used only the storyboard reference for the video.*
```

When converting an existing panel-by-panel sequence to storyboardv2, compress the beats into a single cinematic escalation sentence while preserving the exact required story events and reference identities.

## Template Logic

For v1, prefer the V1 Template Structure above. Use the older compact section logic only when the user asks for a shorter prompt, a non-sheet prompt, or a format incompatible with the template.

Older compact section logic:

```text
[TYPE]:
[REFERENCE USE]:
[FORMAT]:
[LOOK]:
[STYLE / MOTION LANGUAGE]:
[CHARACTER]:
[SCENE]:
[SHOT LOGIC]:
[MOTION / CHOREOGRAPHY LOGIC]:
[CAMERA LOGIC]:
[VFX / ELEMENT / OBJECT LOGIC]:
[ANNOTATION KEY]:
[BOARD RULES]:
[SEQUENCE]:
```

Keep sections concise. Avoid explaining basic storyboard theory. The final artifact should be the prompt, not a lesson.

## Reference Use

When references are provided, state how to use them:

- Character reference: preserve identity, silhouette, costume language, hairstyle, proportions, and key visual motifs. Do not copy copyrighted named characters unless the user owns or explicitly asks for an original-safe reinterpretation.
- Scene reference: preserve spatial mood, architecture, lighting direction, scale cues, materials, and key props. Simplify details so action reads clearly.
- If scene reference is absent, create `[SCENE PROMPT]` before `[SCENE]`. Make it concrete, image-model-ready, and aligned with the action.

Scene prompt format:

```text
[SCENE PROMPT]:
A concise cinematic environment description with location, scale, lighting, atmosphere, key props, floor plane, foreground/background layers, and what must stay minimal for readability.
```

## Look Rules

Storyboard drawings should usually be:

- gray black-and-white line drawings only
- graphite, charcoal, pencil, or ink-like rough linework
- warm off-white or neutral storyboard paper when a sheet look is requested
- rough pencil, ink, or manga thumbnail lines
- unfinished, lightweight, gesture-driven
- readable silhouettes and clear body mechanics
- minimal facial details, costume folds, texture rendering, and decorative polish
- focused on staging, timing, motion, camera, and action readability
- not colorful finished concept art, not polished illustration, not cinematic key art

Use high illustration quality only when the user specifically requests finished concept art.

## Action Rules

Start directly in motion. Avoid calm setup shots unless the user explicitly asks for a slow intro.

Every panel should contain one clear action beat. For action, sports, dance, fantasy performance, fight choreography, transformation, or chase sequences:

- escalate every few panels
- avoid repeated camera angles
- keep key props or powers visible when they drive the sequence
- show body momentum, object paths, environmental reaction, and transition value
- end on an active climax rather than a calm resolution

## Camera Rules

Use varied cinematic framing:

- extreme low angle
- overhead or top-down views
- close-ups on hands, feet, face, props, or impact points
- orbiting camera moves
- whip-pan feeling
- long-lens side silhouette
- wide negative space
- foreground occlusion
- dutch angles
- aggressive push-ins
- parallax and near-lens passes

Match camera language to the genre: arthouse action, anime sports, fantasy music-video, horror, sci-fi, commercial product, or user-specified style.

## Annotation System

Always include a color key and colored handwritten production annotations in normal v1 storyboard output unless the user explicitly asks for clean boards. The panel artwork itself remains black-and-white / grayscale rough line drawing; only the annotation marks and production callouts use color. For storyboardv2, do not put annotations inside panel images.

Default v1 key:

- RED = camera / lens / framing / camera movement
- BLUE = body movement / path / turn / jump / fall / pose flow
- GREEN = key prop path / object movement / transformation flow
- ORANGE = burst / snap / impact / vibration / visual accent / light accent
- PURPLE = timing / acceleration / hold / speed change
- black text = panel labels, shot subtitles, lens notes, and short production notes

If the user's template gives a different color key, preserve that key exactly. If the user asks for clean gray black-and-white boards, omit the color key and state that panels are unannotated graphite-gray line drawings.

Annotation marks should look like rough handwritten production notes, not clean vector graphics. Use curved arrows for spins, arcs, orbital movement, ribbons, bat trails, or energy flow; straight arrows for push-ins and direct motion; dashed arrows for anticipated motion and trails.

Do not use arrows or motion lines inside panel images in storyboardv2 mode.

## Sequence Writing

For each panel, write:

```text
[NUMBER] - [SHOT NAME]
SHOT NOTE:
[Short purpose, transition value, or visual idea]
camera:
[Framing, lens, movement]
action:
[One clear action beat]
focus:
[What must read first]
```

Keep each panel compact. Make panel descriptions concrete enough for an image model to draw.

## Scene Generation Without Scene Reference

When inventing a scene:

1. Choose an environment that amplifies the character's action language.
2. Define scale, floor plane, props, light, atmosphere, and foreground/background layers.
3. Keep it minimal enough that motion reads.
4. Include interaction opportunities: dust, reflections, fabric, hanging objects, nets, debris, water ripples, shadows, particles, or architectural silhouettes.
5. Avoid overcrowding frames.

## Genre Adaptation

Use the user's concept to choose the action system:

- Kung fu / fight: explosive body mechanics, impact poses, low stances, sweeps, strikes, dust, shockwaves, martial silhouette clarity.
- Sports / batting / training: prop always visible, flawless rhythm, contact beats, footwork, slow-motion anticipation, impact bursts, net or equipment reactions.
- Ribbon / dance / fantasy performance: object-first choreography, shape formation, transformation flow, orbiting camera, near-lens wipes, elegant body control with aggressive object motion.
- Product / commercial: feature-focused panels, macro shots, assembly or reveal logic, material callouts, lighting arrows, practical VFX.
- Horror / suspense: readable threat geography, restrained motion, negative space, lens notes, shadow direction, escalation through proximity.

## Negative Constraints

Include clear negatives tailored to the request:

- no dialogue
- no singing
- no timestamps
- no extra characters unless requested
- no enemies unless requested
- no logos
- no watermark
- no polished final illustration look
- no colorful rendered panels unless explicitly requested
- no overcrowded frames
- no static standing poses for action boards

## Output Style

Write the final storyboard prompt in Chinese by default, regardless of the user's mixed-language input, unless the user explicitly asks for English or another language. Do not switch to English just because the target image model may understand English well. If the user requests English, output English only; if they requests bilingual output, provide Chinese first and English second.

Do not mention that this skill was used. Do not include implementation notes.
