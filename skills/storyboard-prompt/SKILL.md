---
name: storyboard-prompt
description: Generate cinematic storyboard sketch prompts for GPT Image or similar image models from character references and optional scene references. Use when the user asks for storyboard prompts, storyboard sheets, cinematic panels, action previs, rough animation thumbnails, Chinese storyboard prompt requests, rough storyboard sketches, or scene prompts when no scene reference is provided. Supports character-only inputs, character plus scene references, action/performance/sports/fantasy sequences, 16:9 multi-panel storyboard sheets, annotation color systems, camera logic, motion progression, and panel-by-panel shot lists.
---

# Storyboard Prompt

Use this skill to turn a user's character and optional scene references into a production-style storyboard prompt. Output a prompt the user can paste into GPT Image or another image model.

## Core Decision

1. If the user provides both character and scene references, generate a complete storyboard prompt that explicitly uses both references.
2. If the user provides a character reference but no scene reference, first generate a concise scene prompt section, then include that scene inside the storyboard prompt.
3. If the user provides no references, write a self-contained storyboard prompt from the user's concept and ask for references only if identity consistency is essential.

## Required Output Shape

Default to:

- `Storyboard Prompt for GPT Image 2:`
- 16:9 storyboard sheet
- 12 cinematic panels
- 3x4 grid
- rough grayscale storyboard drawings
- colored handwritten annotations
- no timestamps, dialogue, logos, watermark, subtitles, or extra UI unless requested

Use the user's requested panel count, grid, aspect ratio, style, language, or tool target when specified.

## Template Logic

Include these sections when useful:

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

- black and white or grayscale base
- rough pencil, ink, or manga thumbnail lines
- unfinished, lightweight, gesture-driven
- readable silhouettes and clear body mechanics
- minimal facial details, costume folds, texture rendering, and decorative polish
- focused on staging, timing, motion, camera, and action readability

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

Always include a color key unless the user asks for clean boards.

Default key:

- red = body movement or action path
- blue = camera movement
- green = framing, composition, object path, or transformation flow
- orange = lighting, impact, burst, vibration, or accent
- yellow = VFX, elemental energy, rhythm effects, or special effects
- purple = timing, acceleration, hold, or speed change
- black text = panel labels, lens notes, and short production notes

If the user's template gives a different color key, preserve that key exactly.

Annotation marks should look like rough handwritten production notes, not clean vector graphics. Use curved arrows for spins, arcs, orbital movement, ribbons, bat trails, or energy flow; straight arrows for push-ins and direct motion; dashed arrows for anticipated motion and trails.

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
- no overcrowded frames
- no static standing poses for action boards

## Output Style

Write in the user's language unless they ask for English. If the target image model prompt is likely better in English, provide the final prompt in English and optionally add a short Chinese note above it.

Do not mention that this skill was used. Do not include implementation notes.
