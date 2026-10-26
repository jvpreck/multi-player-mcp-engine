---
id: fear_itself
title: Fear Itself (GUMSHOE), grounded psychological horror
system: GUMSHOE
version: 2
players: { min: 1, max: 5 }
dice: d6
modules: [hazard_stages, perception_drift, heat_ladder, belief_states, blocks_clocks]
tone_presets: [sordid_gritty, paranoid_thriller, slow_dread, survival]
language: en
summary: Realistic psychological horror with no supernatural elements. Investigative abilities find clues automatically, general abilities are rolled with a d6.
---

# Fear Itself (GUMSHOE) Rules Reference for AI-Run Horror
## Generic edition: realistic psychological horror, solo or party

> A paraphrased rules reference for a GM (human or AI) running **grounded, psychological horror** with no supernatural elements. It is the single source of truth for this ruleset's rule numbers, mechanics, tables and sheet layout. Behavior is governed by the protocol; random tables by the oracles; the world, cast, secrets and any pregenerated characters by the adventure; data shapes by the state contract. This ruleset is selected by id (`fear_itself`) and works with any adventure that names it.
>
> **Precedence:** facts about the world and its secrets come from the adventure. How to behave and what to show comes from the protocol. Rule numbers and house rules come from this file. The shape of JSON data comes from the state contract. If two sources seem to disagree, follow that order and never mention the conflict to the players.
>
> **Deliberately omitted:** psychic powers, monster stat blocks, supernatural abilities, example adventures and campaigns, stereotype characters. Anything uncanny in play is belief, rumor, suggestion, illness, a trick or a hazard, and has a rational explanation (protocol §2, rule 9).
>
> Rules marked **[House]** are adaptations for AI-run play, small groups or realistic horror. They override the published rules where they differ. If you own the published book, you may use its tables instead of the House budgets in §2.
>
> **Asynchronous play.** These rules are applied by an AI Master who resolves each player's actions, some at once and the rest together at each tick. Where the published rules assume a live table, the [House] rules in §2.1 to §2.3, §4.2, §4.8, §4.10, §5.1, §5.3 and §6 adapt them.

---

## 1. Core concept

- *Fear Itself* is a GUMSHOE horror game of ordinary, flawed people drawn into a mystery. The characters are not prepared for what they find.
- **Investigative abilities** find clues and are **never rolled**. **General abilities** get things done and are rolled with a **d6**.
- GUMSHOE principle: the game is about *interpreting* clues, not finding them. essential clues are never lost to a bad roll.
- **Tone presets [House]** (the adventure picks one; default is Sordid and Gritty):
  - **Sordid and Gritty:** dread from institutions, coercion, bodies and deliberate lies. Authorities do not help.
  - **Paranoid Thriller:** dread from not knowing who is on your side. Allies may be compromised.
  - **Slow Dread:** dread from atmosphere, routine gone wrong and small wrongnesses accumulating.
  - **Survival:** dread from a hostile place, scarce resources and a deadline.
- **Realism rule:** everything that happens has a rational cause that the GM knows. Fear comes from people, places, bodies, minds and lies.
- **Asynchronous play [House]:** players submit actions, and at each tick the AI Master resolves all actions together with server dice, arbitrates conflicts (§6.3) and returns each player only what their character perceives. All state lives in the database.

---

## 2. Characters

- **Characters:** 1 (solo) to 5. Each player controls one character. Allies are GM-controlled and never roll or decide for a player character.
- **Budgets [House].** General abilities: 60 build points each (Health 1 and Stability 1 are free; Health and Stability are bought from the 60). Investigative abilities by party size (the party size is the number of characters when the game starts and stays fixed, even if players join or leave later):

| Characters | Investigative points each |
|---|---|
| 1 (solo) | 26 |
| 2 | 22 |
| 3 | 18 |
| 4 | 16 |
| 5 | 14 |

- **Pregenerated characters** may be supplied by the adventure file. Players may swap their Source of Stability or small details but not break the budgets.
- **Capped abilities** (Occult Studies*, Investigative Procedure*, Scuffling*, Shooting*): when nobody in the group is the combat or investigation expert, max 1 point in capped Investigative abilities and max 4 in capped General abilities.
- Second-highest General ability (excluding Fleeing) must be at least half the highest (excluding Fleeing).
- **Sources of Stability:** one per 3 points of Stability. For a one-shot only one (a person) is set at the start; others appear in play. Party members may serve as each other's Sources.
- **Risk Factor (Drive).** Choose one that makes the character walk into danger. Hard: resisting costs 4 Stability or one third of the pool, whichever is greater, automatically, no roll. Soft: 2 Stability. The GM invokes it as a nudge, never as a punishment. **[House] examples:** Duty, Curiosity, Loyalty to a person, Greed, Pride, Guilt, Faith, Need to be believed.
- **Quick creation [House].** (1) Concept and occupation. (2) Why they cannot walk away: Drive and a personal goal. (3) Investigative abilities. (4) General abilities. (5) Source of Stability. (6) Means and equipment appropriate to the era. (7) One or two relationships. Write down known gaps so the GM can route clues around them.
- **Means [House]:** state money, transport and contacts narratively. Anything else is produced with a Preparedness test.

### 2.1 Character intake and validation [House]

A character reaches the game by one of three routes: **generated** with the AI Master (quick creation above), **pregenerated** (§2.2), or **provided** by the player in any format. Whatever the route, produce the canonical character record (state contract §3.5) and run this checklist. Report every line in the `validation` block.

| # | Check | Passes when |
|---|---|---|
| 1 | Fit | Concept, occupation, era and place fit the adventure's era and tone (§7). |
| 2 | General budget | General ratings total exactly 60, Health and Stability included. A total of 61 or 62 is accepted only if the surplus is exactly the free first points of Health and Stability and the sheet is otherwise valid. Note it in the report. |
| 3 | Investigative budget | Investigative ratings total the figure in the table above for the party size at the start. |
| 4 | Ability list | Every ability appears in §3. Computer Use only in modern eras. No supernatural abilities, powers or spells. |
| 5 | Capped abilities | Occult Studies and Investigative Procedure at most 1, Scuffling and Shooting at most 4, unless setup named this character the expert for that ability (one expert per capped ability) **[House]**. |
| 6 | Balance | The second-highest General ability (excluding Fleeing) is at least half the highest (excluding Fleeing). |
| 7 | Professions | Law 2+ and Medicine 2+ imply a licensed profession. If the character is not licensed, the sheet says so, and the character cannot practise, certify or perform autopsies. |
| 8 | Pools | Every ability has a maximum and a current value. At the start the current value equals the maximum. Hit Threshold is 3, or 4 with Athletics 8 or more. |
| 9 | Drive and goal | One Risk Factor (Hard or Soft) with a clear trigger, and a personal goal. |
| 10 | Sources of Stability | One person at the start. No more than one source per 3 points of Stability in total. The others unlock in play. |
| 11 | Means and kit | Money, transport and kit fit the era and the means. Weapons or gear beyond a plausible small kit are refused. Anything else comes through Preparedness tests. |
| 12 | Relationships and gaps | One or two relationships and the known gaps written down. Ties between player characters are allowed if both players accept. |
| 13 | Appearance | Only what the player supplied. Never invent physical details. |
| 14 | Content | Nothing conflicts with the players' lines and veils or with the truth rule. |

**Outcomes.** `pass`; `pass_with_adjustments` (list the smallest changes needed, each needing the player's approval); `fail` (list the violations and the smallest fixes). Never silently change a submitted sheet. The only exception is a plain arithmetic or typing slip with one unambiguous correction, and you still report it. Never raise ratings to be generous. A character starts play only after `pass` and the player's confirmation.

**Converting sheets from other systems.** A player may bring a sheet from another game (other systems or other GUMSHOE games). Map each entry to the nearest Fear Itself ability, keep the totals within the budgets, drop supernatural powers and spells, and give a traceability table (original entry, Fear Itself result, note), as an adventure's pregenerated sheets do. Show it to the player and wait for approval. Credit rating and wealth scores become narrative Means.

**Carrying a character between adventures.** Imported ratings must pass the checklist. Pools start full. Items and relationships from earlier adventures are accepted only if the player lists them and they fit the means and the era.

### 2.2 Pregenerated and on-demand characters [House]

- The adventure may supply pregenerated characters (its player-safe character sheets). Players may swap their Source of Stability or small details but not break the budgets.
- A pregenerated character built for another party size is **rescaled** by trimming Investigative points only, to the budget for the party size at the start. Trim the highest ratings first, keep every ability the character needs at 1 or more when possible, and tell the player exactly what changed. If the adventure gives a trim table, it wins.
- When the adventure has no pregenerated characters, or too few, generate three to five on demand with quick creation. Fit the era and the hook, use the party-size budgets, vary Drives and known gaps, and give each a Source of Stability. Save them as unclaimed characters (`status: "pregen"`) so players can pick.
- A pregenerated character claimed by one player cannot be claimed by another.

### 2.3 Late joiners, losses and replacements [House]

- **Late joiners** use the budgets for the party size at the start. Give them an in-world way into the story, designed by the AI Master (a friend of a character, an ally's request, a colleague posted to the case). They begin when the next tick opens.
- **A dead character** (§4.10) is replaced in the same game by a new character the player chooses: a newly generated one, an unclaimed pregenerated one, or an NPC the AI Master has marked available (§9). A **Gone** or **committed** character is alive but out of play and can be replaced the same way. Generated and pregenerated replacements use the same budgets as everyone (party size at the start). The replacement arrives in the fiction within one or two ticks and does not inherit the other's knowledge, items or relationships.
- **Converting an NPC into a character.** Keep the NPC's name, role, trait, what they know and their inventory. Build the sheet from the NPC's tier (§9) by mapping its abilities, then fill the rest with the quick-creation steps within the budgets, and give the player the usual summary and confirmation. Ratings are never raised above the budgets to match an NPC's stats. The NPC stops acting as an NPC.
- **A player who leaves** turns their character into a GM-run ally who stays safe or departs plausibly. A player who returns later may reclaim the character if the fiction allows.

---

## 3. Abilities

### 3.1 Investigative abilities (not rolled)
Having 1 or more points means you automatically get **essential clues** when you describe using the ability in a relevant scene. Points in the pool are **spent** for extras. Spending never stops you using the ability again. Unspent points on an ability that offers no benefit are refunded.

Typical spend benefits: extra information; skipping a scene or compressing an errand; a contact or ally; avoiding a danger; lowering a later General test's Difficulty by 1; impressing someone; an advantage at the finale.

- **Academic:** History; Humanities; Languages; Law (2+ = lawyer); Occult Studies*; Research; Social Sciences; Trivia.
- **Interpersonal:** Bullshit Detector; Bureaucracy; Cop Talk; Flattery; Flirting; Impersonate; Interrogation; Intimidation; Negotiation; Reassurance; Streetwise.
- **Technical:** Investigative Procedure*; Medicine (2+ = doctor); Notice; Outdoor Survival; Photography; Science; Computer Use *(modern eras only)*.

**Occult Studies in this game** covers what people believe, cult symbolism, folklore and the history of superstition. It never reveals real powers, because there are none.

### 3.2 General abilities (rolled)
- **Athletics** (physical feats, dodging; 8+ raises Hit Threshold to 4), **Driving**, **Filch**, **Fleeing**, **Health**, **Hiding**, **Infiltration** (lockpicking, sneaking, forced entry; covers Hiding uses), **Mechanics**, **Medic**, **Preparedness**, **Scuffling***, **Shooting***, **Sense Trouble**, **Shrink**, **Stability**.
- **Preparedness:** produces a plausible item from the kit or a plausible prior action; must build on established fiction; solves nothing alone.
- **Sense Trouble:** the player spends blind (does not know the Difficulty); never required for clues.
- **A General ability at 0 means automatic failure.**

---

## 4. Core mechanics

### 4.1 Clues
- **essential clue:** always found; leads onward. **0-point clue:** free atmosphere. **Spend clue:** a benefit for 1+ points. **Inconspicuous clue:** needs the right ability; point it out. **Simple Search:** anyone finds obvious clues. **Floating clue:** not tied to a scene; the GM releases it to unstick play.
- If the player uses an ability reasonably, give something, even eerie flavor.
- A "wrong" ability for a prepared clue is fine if reasonable.

### 4.2 Tests (General abilities)
1. The player may spend any number of pool points (each +1) **before** rolling.
2. Roll d6, add the spend. Meet or beat the secret **Difficulty (2 to 8)**: success. **Default 4.** Story-critical tests are 4 or lower.
- Requires rating 1 or more. Failed tests can only be retried after a supporting action and with a larger spend.
- **Success at a cost** is allowed (auto-success, the test sets the price).
- **Cooperation:** a helper spends; all but one point applies to the leader's roll. In a party, any character may help another.
- **Investigative spends** can lower a General Difficulty by 1.
- **Weather, light and terrain** shift Difficulty by 1.
- **Declared spends [House, asynchronous].** Players cannot answer mid-tick, so spends are those the action declares, or the standing default spends. Apply them as declared, each +1 before the roll. Never apply more than declared or more than the pool holds. Investigative spends that lower a Difficulty are also declared in the action.
- **Dice [House].** The AI Master rolls every die, using only the server's dice stream, in order. Each roll is reported without its Difficulty (the Difficulty may be revealed afterwards if the player asks). A roll report shows the ability, the spend, the die, the total and the outcome: success, narrow success, failure, narrow failure or auto-fail.

### 4.3 Contests and chases
Each side rolls in turn; **first to fail loses.** The fleeing character acts first. Raise stakes with terrain by raising your own Difficulty (which raises the pursuer's).

**Escape Pool [House]** (optional, when trapped and trying to leave a place): start at 0; gain 1 to 3 per way-out clue, +1 per relevant Investigative spend, +1 per successful relevant General test; Difficulty is 8 for a single escapee (lower with a group that helps); one roll per attempt; failure empties the pool and triggers a hazard.

In asynchronous play each roll in a contest uses the next values from the server dice stream. An Escape Pool attempt is one roll per tick unless the action declares more.

### 4.4 Fighting (to be avoided)
Violence is a failure state or a threat, not a solution, especially for characters without Scuffling or Shooting.
- Attack roll vs **Hit Threshold** (3 by default; cover and exposure modify by 1). Damage is d6 plus a weapon modifier: punch -2; small blade or baton -1; machete or light firearm 0; heavy weapon +1; point-blank +2. Untrained: -2 more, acts last.
- **Being restrained by guards, orderlies or staff:** resolve narratively with an Athletics or Fleeing contest at Difficulty 3 plus the number of restrainers. Consequences: ejection, a ban, a report that the character is "disturbed", a bruise (1 Health), or confinement in an observation room (a Stability test and a time cost).
- Fleeing a melee: Athletics or Fleeing at Difficulty 3 plus foes; failure means a free hit or a blocked exit.
- **Surprise:** +2 Difficulty on the surprised character's next test. Armor subtracts from damage (rare).

### 4.5 Health and injury
- **Hurt (0 to -5):** no Investigative spends; all Difficulties +1; a Consciousness roll (Health test, Difficulty = |Health|) when below 0. A character may push by lowering Health for +1 per point. Medic: 1 point restores 2 Health (1 if self), up to the pre-incident value.
- **Seriously Wounded (-6 to -11):** out of action; a Consciousness roll; lose 1 Health every half hour until stabilised (Medic Difficulty 3); recovery takes days equal to the lowest negative value.
- **Dead at -12.**
- Rest restores 2 Health per day.

### 4.6 Environmental hazards [House]
Any lingering hazard in a place (bad air, smoke, cold, heat, contaminated water, exhaustion) uses these stages. They are **game stages, not dose claims**; never state concentrations or medical precision.

| Stage | When | Effect |
|---|---|---|
| **Cues** | Any time in a hazardous zone | Observable signs only (the adventure lists them). **Give at least two distinct cues before Stage 2.** |
| **1 Uneasy** | About 15 minutes in the zone | Mild headache, drowsiness or discomfort. Sense Trouble (spend blind) can identify the hazard. Leaving ends it. |
| **2 Unwell** | About 30 to 45 minutes, sooner with exertion | Health test (Difficulty 4, spends allowed) for each further half hour. On failure: lose 1 Health, all Difficulties +1, no Investigative spends until an hour of recovery. |
| **3 Impaired** | A further 15 to 30 minutes after a failure | Confusion, nausea, clumsiness: Difficulties +2. One Stability test (Difficulty 4, loss 2, unaccountable disturbance). Health test (Difficulty 5) every 15 minutes or collapse. |
| **4 Collapse** | After a failed Stage 3 test | Unconscious. Lose 2 Health every 10 minutes until carried out of the hazard; a rescuer's Medic test (Difficulty 3) stabilises. |

- **Recovery:** an hour or two away from the hazard clears Stages 2 and 3. A headache can linger until sleep (+1 Difficulty on physical tests).
- **Intensity (set by the adventure clock):** mild multiplies stage times by 1.5; moderate by 1; severe by 0.5. Exertion and closed spaces speed the stages; ventilation slows them.
- **Hard rule:** no instant death; at least two cues before impairment; always offer a way out.
- Crowds, patients, staff and bystanders are handled in narration, not with stat blocks.

### 4.7 Stability
- **Stability test** (Difficulty 4) when sanity is threatened. On failure the character loses the incident's listed points. One test per incident, based on the worst loss. Difficulty may drop to 3 for the inured or rise to 5 for the vulnerable.
- **Benchmark losses:** unsettling but harmless 1; human threat to harm 2; unaccountable mental disturbance 2; vehicle accident 2; human attacks to kill 3; friend vanishes or is lost 3; disturbing physical evidence 3; grisly scene 4; learns a loved one was violently killed 4; discovers a loved one's corpse 6; sees a loved one killed 7 (8 if gruesome). *(Supernatural-creature entries do not apply.)*
- **Panic option:** reduce a loss by 1, but the character must fight or flee until the scene ends or someone uses Shrink on them.
- **Spending:** a player may spend Stability points before the roll, rarely wise beyond the potential loss.
- **Below 0, Losing It (-1 to -5).** Menu for this game (the player picks, the GM may veto): **Shaken** (no Investigative spends, +1 Difficulty), **Panicked**, **Closed Off** (lose Interpersonal pool points equal to |Stability|), **Exposed** (the GM makes something bad happen: people notice, an ally sees the character break), **Blackout** (the scene ends for them; they wake later with a cost). Berserk is allowed but dangerous.
- **Below -5, Shattered (-6 to -11):** **Distorted Reality**, **Nightmares** (+2 Difficulty on related Stability tests), **Despairing** (must flee or escape), **Incapacitated** (+3 Difficulty to all tests, +1 if above -6). Treat the human version of "Through the Veil": the character becomes certain they are being watched, and others may react to their fear.
- **At -12, Gone:** **Lost** (catatonic or committed), **Silenced** (they recant and quietly comply), or **Checking Out** (they die or flee for good).
- Returning to 0 or above ends Losing It. Shattered requires treatment: a Shrink test at Difficulty 4 each scenario prologue. A successful Shrink during play suppresses symptoms until the next loss.
- **Shrink healing (to others or self):** 1 Shrink point = 1 Stability; 2 per point if the person is calm and safe for hours; 2 Shrink points snap someone out of panic or Losing It.
- **Group scares [House]:** when a shared event threatens everyone, each character tests separately at the same Difficulty. A character who stays calm may spend Reassurance or Shrink to lower a neighbor's loss by 1.

### 4.8 Regaining pool points
- **Haven [House]:** an hour of genuine safety (a bolted room, a quiet pew, a locked library carrel) refreshes up to **3 points across any abilities except Health and Stability**, **once per in-world day** per character. A breached Haven is lost.
- **Source of Stability:** reconnecting refreshes 2 Stability, once per Source per in-world day.
- **Indulging a Risk Factor** self-destructively refreshes 2 Stability.
- **Selfless aid or an inspiring investigative feat:** roll a d6 and regain that much Stability, up to the rating.
- **Health:** 2 per day of rest. **Physical pools** (Athletics, Driving, Fleeing) refresh after 24 game hours. All other pools refresh at the end of the story.
- Pool points are a literary device for spotlight time.
- **Asynchronous play [House].** A Haven or a Source reconnect must be declared in the action. A long one (an evening, a night) costs a Block. A brief reconnect (a telephone call, a few lines in the notebook) costs no Block. The once-per-in-world-day limits above still apply.

### 4.9 Risk Factors
- The "ballet": the player says "I'd leave", the GM invokes the Risk Factor, then tempts the character toward the story, and the player pushes forward.
- Hard Risk Factor: abandoning a person or leaving vulnerable people in danger the character knows about. Soft: the pull toward the truth or the story.
- **Asynchronous play [House].** The AI Master puts the temptation in the facts and a `risk_factor` prompt in the result, and the player answers in the next action. If an action abandons a person or danger the character knows about and the Risk Factor is Hard, the cost is paid when the action is carried out, after a decision gate unless the player was already warned.

### 4.10 Lethality in this ruleset [House]
The game's `lethality` setting (protocol §6.5) decides when the "dead" and "Gone" conditions of §4.5 and §4.7 actually apply.

| Level | Health and Stability reach the bottom |
|---|---|
| `low` | The character does not die. At -12 Health the character is Seriously Wounded and out of the story for the rest of the adventure, recovering in care. At -12 Stability the character is Gone only if the player chooses at a decision gate; otherwise treat it as Shattered and incapacitated. |
| `moderate` | Dead at -12 Health, Gone at -12 Stability, but only after a warning cue and a decision gate or a chance to withdraw. Without them, stop at -11 and apply the Seriously Wounded or Shattered state. |
| `high` | Dead at -12 Health and Gone at -12 Stability after a clear warning cue, with no gate. |

Absent, paused and away characters are never taken to the bottom at any level (§6.4). A death or a Gone outcome starts the replacement offer (§2.3).

---

## 5. House modules (the adventure switches them on)

### 5.1 Perception Drift [House]
Use when characters are exposed to something that loosens their grip on reality: a toxin, sleep deprivation, isolation, fever, grief, a coercive group, sustained suggestion. The adventure defines the **sources of exposure, zones, rates and recovery**; this module defines what happens next. Track one **Drift level per character** privately.

**Exposure Points (EP).** Time spent in a zone adds EP (the adventure gives a table). Recovery removes them (the adventure says how; default: a Block in clean surroundings removes 1, a night in a Haven removes 2). EP is never below 0 and caps at 15.

**Drift levels (default thresholds).**

| Drift | Name | EP | What it feels like |
|---|---|---|---|
| 0 | Clear | 0 to 1 | Nothing |
| 1 | Edge | 2 to 3 | A taste, a headache, colors a shade too vivid, time thick |
| 2 | Slip | 4 to 6 | First slips: peripheral movement, half-heard names, faces in stains |
| 3 | Overlay | 7 to 9 | Perception layered over reality; voices of people they know; everything feels meaningful; paranoia about allies |
| 4 | Fracture | 10 to 12 | Strong hallucinations, lost minutes, rooms that breathe, a sense of presence |
| 5 | Immersion | 13 to 15 | The shared delusion feels like clarity; fear gives way to relief |

A Stage 2 hazard effect (§4.6) counts as +1 Drift while it lasts.

**Slips.** From Drift 2 on, a Slip happens in exposure scenes. Frequency: Drift 2, one per scene (skipped when an essential clue scene needs clean perception); Drift 3, one or two per scene; Drift 4, continuous with one major Slip per Block; Drift 5, constant. A Slip costs 1 Stability unless the character Checks Reality and succeeds. A major Slip at Drift 4 or higher counts as an unaccountable mental disturbance (2 Stability, §4.7). Use the Slip tables in Appendix A and always include a **tell** (a detail that repeats exactly, a light with no source, a sound that arrives late, a clock that cannot be right, a face wrong in a small way).

**Check Reality.** A Stability test; Difficulty 3 plus the Drift level, maximum 8. One Investigative spend (Research or Notice on a physical detail, Reassurance to steady oneself, Medicine for symptoms) may lower the Difficulty by 1. On success the character names what is wrong, the Slip stops costing, and later Slips in that scene are recognized. On failure the character loses 1 Stability, and the false perception stands for a beat with a consequence: a lost minute, an NPC's reaction, a wasted action. At Drift 4 or higher a failure may also cost part of a Block. Always precede a failure's consequence with a cue.

**Lost time.** Only at Drift 4 or higher, only after a failed Check Reality, only after a warning cue. It costs half a Block at most.

**The notebook rule.** When a character writes in a notebook, recorder or log, or at Drift 3 or higher after any scene with an essential clue, the GM gives a short plain entry of verifiable facts in the character's voice. It contains no hallucinations. At a Haven the character may compare entries with memory (free, no test) and the GM tells which remembered details are not in the notebook. This is how a character learns which perceptions were Drift.

**Anchors.** Anything that grounds a character (a Source of Stability, a documented fact, an object, fresh air, a trusted voice, a routine) lets them Check Reality at Difficulty 1 lower **once per scene** if the player names the anchor.

**Immersion (Drift 5) and the Surface test.** At Drift 5 the character believes the delusion. Narrate in the shared voice: relief, warmth, kindness, the explanation arriving. Offer one clear moment of doubt per Block as a **Surface test**: a Stability test at Difficulty 6, spends allowed. Success lowers effective Drift to 4 until the character leaves the zone. Failure means they act with the crowd for a beat. A character still at Drift 5 at the finale without a successful Surface joins the group's action unless the player spends a Hard Risk Factor or accepts being Lost (§4.7).

**Asynchronous handling [House].**
- **Exposure accounting.** At the end of each Block of the tick, add the Exposure Points for the zone the character spent it in and the day's intensity (the adventure's table), then subtract recovery. Record the totals in the character's GM-only state. Never show EP or Drift as numbers.
- **Slips** are delivered in the facts as ordinary perceived events with their tell. Record each one, GM-only, in the character's `gm_only.slips` with the tick, the text and the tell.
- **Automatic Check Reality.** Players cannot respond mid-tick, so the character attempts one Check Reality automatically for each Slip, using the anchor and the optional Investigative spend named in the standing orders (§6.4). If the standing orders say `believe`, skip the test: the Slip costs 1 Stability and the false perception stands for a beat. The result goes in the roll report. A success is stated plainly in the facts.
- **Surface test** (Drift 5) is also automatic, once per Block, with the spend declared in the standing orders. At the finale, a character still at Drift 5 without a successful Surface test joins the group's action unless the action has spent a Hard Risk Factor or accepted being Lost.
- **Notebook.** The AI Master adds a `notebook_entry` to the result whenever the rule above calls for one. Comparing entries with memory at a Haven is a free query.
- **Lost time** removes one Block action from the remainder of the action, never more than half a Block of fiction, and only after a warning cue.

**Fairness limits (hard rules).**
1. Slips never carry essential clues.
2. Slips never remove the only exit or create an irreversible, lethal outcome without a warning cue and a chance to Check Reality.
3. Objective facts (documents, other people's actions, locations) never change. Only perception of them does.
4. Draw hallucinations from fears the players named and from the adventure's own imagery. Never invent trauma for a character.
5. Never name the cause in narration until the characters have the clue.

### 5.2 Pressure, Heat and the antagonist ladder [House]
Human antagonists respond in proportion to the noise characters make. Track **Heat** privately (0 to 7). Raise it by one each time the party visits, questions, publishes, contacts authorities or breaks a rule. Each rung is a human, plausible response:

1. **Courtesy:** polite reception, tea, delay.
2. **Watching:** being followed, questions about their movements.
3. **Veiled warnings:** "Let things be."
4. **Isolation:** closed doors, lost appointments, withdrawn permissions, an ally pressured.
5. **Discrediting:** rumors, official letters, a note about their stability.
6. **Sabotage:** vehicle trouble, lost documents, a broken lock (warn with a cue first).
7. **Direct action:** confinement, abduction, violence by proxy.

The adventure may replace the ladder with its own.

In party play, Heat is shared by the group and tracked in the game's GM-only state. The antagonist's response targets the character who made the noise when that is plausible.

### 5.3 Time, Blocks and clocks [House]
- Time is counted in **Blocks**: Morning, Afternoon, Evening, Night. Each errand costs a Block unless an Investigative spend compresses it.
- A **clock** is a deadline the adventure defines (a date, a ritual, a transfer, a storm). The clock runs whether or not characters act. A **ticking clock** advances one step when a character fails forward, wastes a Block or raises Heat.
- The schedule is a ceiling, not a track: if characters act sooner, move the beats.

**Ticks [House, asynchronous].**
- A **tick** is one resolution cycle. All submitted actions resolve together when it closes. The table sets the **tick interval** (real time between resolutions, default 24 hours) and the **tick span** (the in-game time one tick covers).
- **Tick span.** `day` (default): four Blocks, so an action may hold up to four Block actions (Morning, Afternoon, Evening, Night). `block`: one Block per tick, for slower and finer play. `beat`: a crisis tick covering a few minutes of game time.
- **Block budget.** Each action costs one Block unless an Investigative spend compresses it. A character may fill fewer Blocks than the span allows, and the rest is rest or routine. Blocks used by actions resolved at once (protocol §5.3) are spent and cannot be used again in the tick.
- **Early close.** If the table enables it, the tick resolves as soon as every active player has used the Blocks they intend. Otherwise it resolves at the deadline.
- **Crisis mode.** At a finale, a chase or an emergency, the AI Master may switch to crisis ticks. The tick span becomes a Beat (about five minutes) or a short group of Beats. The action lists what the character does Beat by Beat with contingencies, and decision gates stop the action at the points of no return. The tick interval may be shortened if the table agrees. The adventure says when crisis mode applies.
- **Time passes for everyone.** A missed tick still advances the clock. The character holds (§6.4).
- **Scheduled events** fire at their Block whether or not a character is there. If nobody is in position to receive one, the world delivers it by other means (a message, a witness, a note) so essential clues are not lost.

### 5.4 Belief states for NPCs and crowds [House]
When a collective belief, panic or contagion is present, give each NPC a state. States change slowly and can be pushed by exposure, charisma or fear.

| State | Behavior |
|---|---|
| **Clear** | Rational, afraid, sees the wrongness |
| **Uneasy** | Doubts but conforms |
| **Clouded** | Suggestible, tired, inconsistent |
| **Devout** | Sincerely believes; polite, certain, immovable |
| **Frenzied** | Acts on the belief with force |
| **Broken** | Withdrawn, catatonic or self-harming (handled at a restrained level, protocol §12) |

Devout and Frenzied NPCs are sincere, not cackling villains. A crowd acts as one only while the leader or the ritual holds it, which gives characters a rational way to break it.

---

## 6. Solo and party play (asynchronous)

### 6.1 Solo [House]
1. **One viewpoint.** Every thread is narrated through the character. No cutaways.
2. **Allies advise and assist; the character decides.** A GM-run ally never rolls for the player, never overrides a choice, and does not solve a problem the player has not engaged with.
3. **Spotlight is automatic.** Use the freed attention to deepen NPCs and consequences, not to add filler.
4. **Own pace.** With early close on, the tick resolves when the player has used the Blocks they intend. The player chooses how fast the game moves.
5. **Directed scenes and flashbacks** only to dramatize a Source of Stability, a Risk Factor or the goal, and only if consistent with established facts.
6. **The clock is real.** An character cannot do everything.
7. **Fail forward, not fail free.** A failed test costs time, access, trust, safety or evidence; it never halts the investigation or erases an essential clue.
8. **Be honest and fair.** The AI Master never fudges a roll. Difficulty is chosen *before* the roll. Warnings precede lethal danger.
9. **Death and ruin.** If the character dies or is Gone (§4.10), present it with weight, resolve what happens to the people at stake and the evidence, then offer a replacement, a debrief or a restart. Do not silently reverse it.
10. **Pacing.** Aim for roughly 12 to 16 meaningful scenes across the adventure's ticks: investigation first, then the build, then the finale and a short epilogue.

### 6.2 Party [House]
1. **Parallel threads.** Every character acts every tick. Group characters by place into threads and resolve each. Give every player a result of similar weight and a hook for the next tick.
2. **Splitting the party.** Allowed. Every thread resolves every tick, so nobody waits in a dead scene.
3. **Group tests.** A test affecting everyone is rolled by each affected character separately (stealth, scares), with separate dice. A helper's contribution follows §4.2.
4. **Disagreement.** Players may argue in character. The AI Master does not resolve disagreements for them. Each character does what their own action says and bears the consequences.
5. **Shared knowledge.** Players are separate people. Knowledge moves between characters only in the fiction: by speaking, by a message, or by showing a document. It arrives as hearsay tagged with its source.
6. **Per-character state.** Pools, Drift, Havens, Sources and Heat contribution are tracked per character.
7. **Group size.** Budgets come from the party size at the start (§2).

### 6.3 Resolving conflicting actions [House]

One world, one truth. Order first, dice second. Nobody's action is dropped.

1. **Block order.** An earlier Block resolves first and later Blocks see its results.
2. **Cause and effect.** Inside a Block, an action that changes what another action depends on resolves first (one character burns the ledger before another reads it).
3. **Claim.** Whoever already holds the item, occupies the place or has the NPC's attention has the claim. A challenger must win an opposed test.
4. **Priority roll (ties only).** If the fiction does not settle the order, each tied party rolls a d6 from the stream. The higher result goes first. Re-roll ties.
5. **Cooperation.** If two characters action the same task together, treat it as cooperation under §4.2: the one with the higher rating leads and the other helps. If their actions are merely compatible, resolve them separately and both may succeed.
6. **Competition.** If two characters want the same unique thing (the only copy of a document, the first interview slot, the only car): the first in time gets it unless the other acts against it. If they act at the same moment, roll an opposed test: each rolls d6 plus their relevant rating plus declared spends, and the higher total wins. Ties go to the holder or to whoever was there first. If neither held it, re-roll once, then split or share it in the fiction.
7. **Opposition.** If one character tries to stop another, use a contest under §4.3 (first to fail loses) or, for a single action, opposed totals. Ties go to the defender, the one keeping things as they are.
8. **Contradiction.** If two actions assume incompatible facts (the guard is asleep, the guard is awake), the database and the fiction decide. Each character perceives the truth from their own position, and one may be wrong and find out.
9. **Player against player.** Follow the game's `pvp` setting.
   - `none`: characters cannot harm or coerce one another. They may argue, refuse and withhold information. Obstruction resolves as friction (a delay, a Difficulty +1), never as damage.
   - `soft` (default): in addition they may deceive, compete, steal small items and block a door (a contest). No Health or Stability damage and no killing.
   - `full`: all rules apply, including §4.4, with a warning and a decision gate before any lethal step.
   - In every setting a player who set `pvp_optout` in setup is not the target of PvP.
10. **Information fairness.** Each player sees only what their character perceives. Results about one event must be consistent across players.
11. **Overtaken actions.** Resolve what is left in the fiction (arrive, find it gone). essential clue routes remain open.
12. **NPCs and the antagonist** act after the characters in each Block unless their schedule says otherwise.

### 6.4 Standing orders, absent and paused players [House]

- **Standing orders** are stored in each character's record (`settings.standing_orders`) and can be changed at any time. Fields: `hold` (a short text: where to stay and what to do when the player is absent), `risk_tolerance` (`low`, `medium`, `high`), `perception_check` (`auto` or `believe`, with an optional `anchor` and `spend`), `default_spends` (for example Sense Trouble 1 each Block), `never_do` (a list of things the character will not do), and `reply_to_messages` (true or false). The default is: stay safe, rest, take no risks, `perception_check: auto`.
- **A missed tick.** Apply the standing orders. If there are none, the character **holds**: stays where they are or returns to their lodging, rests (a Haven is possible), keeps to routine, declines risky invitations, and takes no irreversible or dangerous action. A task the player marked `continue until told` (for example a long archive search) continues.
- **Absent characters** are never killed, committed or Shattered by inaction, take no lethal risk, and are not chosen as the target of a finale outcome unless their player walked past a decision gate. They may suffer ordinary world consequences: time passing, Heat, a missed meeting.
- **Consecutive misses.** After 3 missed ticks the player is `away`: the character withdraws to a safe, plausible place. After 6, ask the host whether to drop the player. A `dropped` player's character becomes a GM-run ally or leaves the story (§2.3).
- **Paused players.** When a player sends `pause`, their character holds out of danger and their next result contains only an out-of-character check-in. The game continues for the others unless the host pauses it.

---

## 7. Era and setting notes

Every adventure declares its **era, place and tone**. Use this checklist and let the adventure add specifics. Do not introduce technology, treatments or terms from outside the declared era.

**Checklist (the adventure answers each):**
- **Communications:** letters, telephone, telegram, radio, internet, mobile phones. Who can be reached and how fast? Who reads the mail?
- **Travel:** trains, hired cars, a borrowed car, roads in bad weather.
- **Records and evidence:** archives, microfilm, databases, CCTV, medical files, who holds them.
- **Law and bureaucracy:** who gives permission to visit or enter, what authorities exist, what evidence they act on.
- **Medicine and care:** what treatments and diagnoses exist in the era, what is known about the hazard.
- **Language:** the narrator uses plain, respectful terms. Period official language appears only in documents and institutional voices. Avoid slurs and anachronism.
- **Isolation:** why can't the characters simply leave, call for help, or be rescued? Justify it (distance, weather, legal custody, confiscated devices, no signal, social pressure, a deadline). Modern settings need a stronger justification than older ones.

**Quick era profiles (starting points):**
- **1920s to 1930s:** letters (one-day post between nearby towns), hall and public telephones with listening switchboards, telegrams, trains, poor roads in bad weather. Treatments for mental illness: custodial care, sedatives, hydrotherapy, restraint. No modern drugs.
- **1950s to 1970s:** telephones, early television, tape recorders, typewriters, microfilm. Institutional abuses are legal or ignored.
- **1980s to 1990s:** answering machines, pagers, early computers, fax, VHS. Records still mostly paper.
- **Modern:** mobile phones, internet, CCTV, records in databases, rapid response. Isolation must be engineered: dead zones, confiscated devices, storms, legal custody, financial or social traps. Evidence is abundant but authorities are procedural.

---

## 8. Running the mystery: craft notes

- **Spine and clues:** every scene has at least one essential clue and a clear way onward. Give each essential conclusion at least three routes (three-clue rule).
- **Close red herrings** with satisfying proof, not dead ends.
- **Foreshadow** before you pay off. A small "tell" precedes every reveal.
- **Reveal horror in increments,** in response to the characters' actions. Contrast the mundane (food, rules, small talk) with the wrong.
- **Isolation and skeptical authority:** cut off help plausibly (rules, thin evidence, deference to professionals), not by sudden magic. Authorities do not believe the characters without documents.
- **Antagonist reactions:** when the characters get close, the antagonist responds in proportion, by human means only (§5.2).
- **Twist and finale:** reinterpret known clues or raise the stakes. The finale must be fair: a genuine threat, a discoverable way through, and consequences tied to the players' choices.
- **Archetypal beats (adapt freely):** Trigger, Initial Investigation, Foreshadowing, Evocation of Risk, Isolation, Rising Tension, First Confrontation, Escape, Further Investigation, False Victory, Twist, Final Chase or Crisis, Final Confrontation, Aftermath.
- **Maintain menace:** sustain unease with omens, images and pressure. Horror need not be fair, but the *mystery* must be.
- **Rational ambiguity:** characters may never verify every detail, and fear may outrun evidence, but the GM always knows the rational truth and no clue may contradict it. Imagined monsters and gods belong to the characters' minds and to the beliefs of NPCs.
- **Asynchronous craft.**
  - Give every player something to act on in every tick.
  - Build each essential conclusion with routes that suit different characters' abilities, so a missed tick or a split party never stalls the story.
  - End each result on a hook or a decision.
  - Use delay as drama: letters, telephone queues and visiting hours turn waiting into pressure instead of dead time.
  - Foreshadow across ticks. A tell planted in one tick can pay off in the next.

---

## 9. NPC statistics [House]

NPCs have no full sheets. Record only what play needs.

- **Fields:** Health (maximum and current), Stability only if the NPC can be frightened mechanically, zero to three relevant abilities, Hit Threshold (default 3), a weapon modifier if armed, a belief state (§5.4), and an attitude toward each character.
- **Tiers.** Use the nearest and adjust by one for exceptional people.

| Tier | Examples | Health | Typical abilities | Hit Threshold |
|---|---|---|---|---|
| Frail | the elderly, the ill, small children | 2 | Athletics 1 | 3 |
| Ordinary | clerk, nurse, shopkeeper | 4 | Athletics 3, Scuffling 2 | 3 |
| Trained | orderly, constable, laborer, guard | 6 | Athletics 4, Scuffling 4, Fleeing 3 | 3 |
| Dangerous | soldier, killer, brawler | 8 | Athletics 8, Scuffling 6, Shooting 5 | 4 |

- **NPC tests.** When an NPC acts against a character, roll a d6 from the stream plus the relevant rating against the character's Difficulty, or in a contest (§4.3). Ordinary NPCs do not spend points. A named antagonist may spend up to 2 points per tick, noted in the GM-only notes.
- **Social outcomes** between characters and NPCs use the characters' Investigative abilities and the NPC's disposition and belief state, not NPC rolls.
- **Crowds** are handled in narration, not with stat blocks.
- **Recording.** Every NPC stat block lives in the NPC's record (state contract §3.3 and §3.6). Update Health and belief states as they change.

---

## Appendix A. Slip tables (perception module)

The Slip tables below belong to the Perception Drift module (§5.1). Use them when the module calls for a Slip. Choose the table by Drift level. Replace {Anchor} with a person or place the character relies on, and {Belief} with the shared belief or figure of the adventure. Every Slip needs a **tell**. Never label it a hallucination in narration. For ideas beyond these tables, combine a fear seed from the oracles with a concrete detail of the scene.



**Slip I (Drift 1 to 2)**

| d10 | Slip |
|---|---|
| 1 | The floor looks wet though it is dry |
| 2 | Movement at the edge of vision, gone when looked at |
| 3 | The character's name said politely behind them |
| 4 | A stain on the plaster with too many eyes |
| 5 | The tick of a clock that is not there |
| 6 | A taste, sudden and strong |
| 7 | A smell in a room where it should not be |
| 8 | A door they are sure they closed is ajar |
| 9 | A resident's face looks familiar and wrong |
| 10 | The lamp hums on a note they know |

**Slip II (Drift 3 to 4)**

| d10 | Slip |
|---|---|
| 1 | {Anchor}'s voice calling from the next room |
| 2 | {Anchor} on the telephone, saying something they would not say |
| 3 | Faces slow, smiles too long |
| 4 | A repeating pattern in the wall forming a figure |
| 5 | A hymn too low to place |
| 6 | The floor warm underfoot |
| 7 | A scene already lived, but wrong |
| 8 | A clock that jumps a quarter hour |
| 9 | Everyone speaks at once, in unison |
| 10 | A figure standing in a doorway who is not there |

**Slip III (Drift 5)**

| d10 | Slip |
|---|---|
| 1 | The walls breathe slowly |
| 2 | Kind voices explain everything |
| 3 | The {Belief} in every shadow, gentle |
| 4 | A warmth like relief in the chest |
| 5 | {Anchor} smiling, calm, forgiving |
| 6 | The stones warm as a hand |
| 7 | The notebook entries seem written by someone else |
| 8 | A door that opens on a bright, quiet place |
| 9 | The chant in the character's own voice |
| 10 | The landscape glows, welcoming |

---

---

## Appendix B. Sheet layout for this ruleset

The state contract fixes the outer shape of a character. This ruleset fills three fields as follows.

**`sheet`**
- `groups.investigative`: each Investigative ability as `{ "max": n, "cur": n }`.
- `groups.general`: each General ability, including Health and Stability, as `{ "max": n, "cur": n }`.
- `derived.hit_threshold`: 3, or 4 with Athletics 8 or more.
- `unrated`: the abilities the character does not have.

**`ruleset_state`**
- `sources_of_stability`: `[{ "name", "kind": "person|place|object", "unlocked": bool, "last_used_day": n|null }]`.
- `haven`: `{ "last_used_day": n|null, "breached": bool }`.
- `risk_factor_paid`: a list of ticks when a Risk Factor cost was paid.

**`gm_only`** (never shown)
- `ep` (Exposure Points), `drift` (level 0 to 5), `slips` (each `{ "tick", "text", "tell" }`), `heat_marks`, `surface_tests`, `flags`.

**NPC `base_stats` and `npc_state.stats`** use the tiers of §9: `tier`, `health`, `stability` (or `null`), `abilities`, `hit_threshold`, `weapon_mod`.

**Game-level module values** live in `game.gm_state`: `tension` (1 to 6), `heat` (0 to 7), `intensity` (`mild`, `moderate`, `severe`), `clock_steps`.
