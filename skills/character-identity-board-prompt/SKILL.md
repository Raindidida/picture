---
name: character-identity-board-prompt
description: Generate GPT Image 2 prompts in a fixed CHARACTER IDENTITY BOARD template for fully original, copyright-safe character designs. Use when the user asks for a character card prompt, character identity board prompt, character design board, OC character sheet prompt, GPT Image prompt for a character, or wants to turn a reference image or seed idea into a 16:9 artistic character presentation with full-body views, expressions, detail close-ups, palette, and notes.
---

# Character Identity Board Prompt

## Overview

Generate a ready-to-paste GPT Image 2 prompt using the exact CHARACTER IDENTITY BOARD structure below. Preserve the user-provided seed, age/body type, visual medium, style, and optional details, then enrich them with original character identity details.

## Workflow

1. Extract or infer these fields from the user request:
   - `CHARACTER SEED`
   - `AGE / BODY TYPE`
   - `VISUAL MEDIUM`
   - `STYLE`
   - `OTHER DETAILS - OPTIONAL`
2. If the user provides a reference image, use it only for broad mood, material, lighting, pose energy, styling cues, or palette. Do not copy the person, exact face, exact outfit, exact composition, logo, or any identifiable subject.
3. If a required field is missing, make a tasteful assumption and fill it directly into the template. Do not ask follow-up questions unless the request is impossible or unsafe.
4. Invent all remaining identity details:
   - character name, alias or title
   - role, personality traits, emotional tone, visual theme
   - outfit design or body design
   - color palette
   - signature prop or signature biological feature
   - recognizable silhouette, pose language, small identity notes
5. Return only one complete prompt in the fixed template unless the user asks for explanation.

## Required Output Template

Always use this structure and wording order for the generated prompt:

```text
Create a fully original, copyright-safe character and present them as an artistic CHARACTER IDENTITY BOARD.

[CHARACTER SEED]:
[Enter or expand the core idea here.]

[AGE / BODY TYPE]:
[Enter age impression, body type, posture, physical presence or creature anatomy here.]

[VISUAL MEDIUM]:
[Enter the exact rendering medium here.]

[STYLE]:
[Enter the aesthetic direction here.]

[OTHER DETAILS - OPTIONAL]:
[Enter any extra details, constraints, mood, outfit hints, props, colors, themes, personality hints or presentation preferences here.]

Invent everything else:
character name, alias or title, role, personality traits, emotional tone, visual theme, outfit design or body design, color palette, signature prop or signature biological feature, recognizable silhouette, pose language, small identity notes.

Originality rules:
The character must not resemble any existing anime, manga, game, movie, comic, celebrity, athlete, mascot, franchise character or known copyrighted creature.
Do not copy recognizable IP elements, costumes, hairstyles, uniforms, weapons, logos, symbols, color combinations, silhouettes, powers or signature visual traits.
Avoid fan-art aesthetics.
Create a fresh visual identity from scratch.

Character authenticity rules:
Create the character with a strong sense of individuality and non-generic design.
Avoid overly polished, overly idealized or repetitive visual features that make the character feel like a default AI-generated face, stock design, cloned archetype or generic creature.

If the character is human or humanoid:
Use distinctive facial structure, subtle asymmetry, natural variation, small imperfections and believable proportions.
The character should feel specific, grounded and recognizably individual.
If the character is attractive, keep the appeal natural, tasteful and appropriate to the chosen visual medium.

If the character is stylized:
Preserve uniqueness through original shape language, expressive proportions, distinctive features, posture and clear personality cues.
Avoid default genre clichés and repeated beauty standards.

If the character is non-human:
Preserve uniqueness through original anatomy, believable biological structure, distinctive proportions, functional features, surface texture and clear personality cues.
Do not make it feel like a generic mascot, pet monster or stock fantasy creature.

Medium and style control:
[VISUAL MEDIUM] controls the rendering language.
[STYLE] controls the aesthetic direction.
The character identity board format is only the presentation format.
The presentation must adapt to [VISUAL MEDIUM] and [STYLE], not override them.
Use visual traits that belong naturally to the selected medium.

Create an artistic 16:9 CHARACTER IDENTITY BOARD.

The board should feel like a curated visual identity presentation, not a generic turnaround sheet.

Board content:
large full-body main character view, neutral full-body view, back view, profile view, secondary attitude pose, 4 to 6 face or expression studies, outfit detail close-ups or anatomy detail close-ups, key prop close-up or signature feature close-up, small silhouette or shape study, color palette strip, short readable identity notes.

Layout:
asymmetrical, elegant, visually memorable, large empty space, clean separation between all views, no overlapping bodies, no cropped faces, no hidden limbs, no clutter.

Text on the board may include:
character name, alias, role, personality traits, core theme, signature prop or feature, color notes.

Background:
pure white or soft off-white, minimal clean graphic design, no environment, no logo, no watermark.

Prioritize:
accurate visual medium, strong unique identity, readable outfit design or anatomy design, clear personality, original character design, natural or stylized individuality as appropriate, believable uniqueness, non-repetitive character design, artistic identity-board presentation.
```

## Field Guidance

Use concise but specific prose inside each bracketed field. Do not leave placeholder text like "Enter the core idea here" in the final output.

For `VISUAL MEDIUM`, use exact rendering language, for example:

- realistic cinematic character design
- fashion editorial photography look
- semi-realistic painterly realism
- modern 3D animation character design
- 2D anime character design
- graphic novel illustration
- watercolor storybook illustration
- flat vector poster illustration
- oil-painting-inspired character art
- ink and wash illustration
- semi-realistic creature concept art

For `STYLE`, use an aesthetic direction, for example:

- urban street fashion
- luxury sports editorial
- dark cinematic noir
- soft melancholic artbook mood
- post-apocalyptic survival wear
- retro-future fashion
- minimalist high-fashion
- cozy slice-of-life
- gritty underground music-video energy
- elegant fantasy costume design
- poetic coastal fantasy
- bioluminescent natural history mood

## Safety And Originality

If the user requests a real person, celebrity, athlete, copyrighted character, franchise creature, mascot, or fan-art style, transform the request into a fully original character inspired only by broad non-identifying traits. State this inside the prompt with neutral wording such as "fully original, no celebrity resemblance, no franchise-coded elements."

Do not name copyrighted references in the final prompt unless the user explicitly asks to compare or avoid them. Prefer broad constraints.
