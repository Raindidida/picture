---
name: character-identity-board-prompt
description: Generate GPT Image 2 prompts in a fixed long CHARACTER IDENTITY BOARD template where only four variables are filled: CHARACTER SEED, AGE / BODY TYPE, VISUAL MEDIUM, and STYLE. Use when the user asks for a character card prompt, character identity board prompt, character design board, OC character sheet prompt, GPT Image prompt for a character, or wants a reference image or seed idea converted into a 16:9 artistic character identity board prompt.
---

# Character Identity Board Prompt

## Overview

Generate a ready-to-paste GPT Image 2 prompt using the fixed long CHARACTER IDENTITY BOARD template. Only fill the four variable fields: `[CHARACTER SEED]`, `[AGE / BODY TYPE]`, `[VISUAL MEDIUM]`, and `[STYLE]`. Keep every rule section after the variables unchanged.

## Workflow

1. Extract or infer only these four fields from the user request:
   - `CHARACTER SEED`
   - `AGE / BODY TYPE`
   - `VISUAL MEDIUM`
   - `STYLE`
2. If the user provides extra details, fold them into one of the four fields instead of adding `[OTHER DETAILS - OPTIONAL]`.
3. If the user provides a reference image, use it only for broad mood, material, lighting, pose energy, styling cues, or palette. Do not copy the person, exact face, exact outfit, exact composition, logo, or any identifiable subject.
4. If a required field is missing, make a tasteful assumption and fill it directly into the field.
5. Return only one complete prompt in the fixed template unless the user asks for explanation.

## Required Output Template

Always use this exact structure. Fill only the four bracketed variable sections at the top. Do not include an `[OTHER DETAILS - OPTIONAL]` section in the generated output.

```text
Create a fully original, copyright-safe character and present them as an artistic CHARACTER IDENTITY BOARD.

[CHARACTER SEED]:
[Fill this with the core idea, identity hook, mood, outfit/body hints, props, colors, themes, personality hints, and any user-provided extra details.]

[AGE / BODY TYPE]:
[Fill this with age impression, body type, posture, physical presence, or creature anatomy.]

[VISUAL MEDIUM]:
[Fill this with the exact rendering medium.]

[STYLE]:
[Fill this with the aesthetic direction.]

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

Use concise but specific prose inside each filled field. Do not leave placeholder text in the final output.

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

## Important Constraints

- Do not add `[OTHER DETAILS - OPTIONAL]` in normal generated prompts.
- Do not rewrite or shorten the fixed rule sections after `[STYLE]`.
- Do not create a separate negative prompt unless the user asks.
- If the user asks for shorter output, make the four filled fields shorter while keeping the fixed long sections intact.
