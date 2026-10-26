---
id: genius_loci_danvers_1925
title: "Genius Loci, Danvers, November 1925: The Breathing Hill"
ruleset: fear_itself
generation: supplied
era: "1925"
place: Massachusetts
players: { min: 1, max: 5 }
recommended:
  tick_span: day
  tick_interval_hours: 24
  early_close_solo: true
  early_close_party: false
  lethality: moderate
pace_options: [slow, fast]
pregenerated: [pregen_eleanor_vance]
language: en
summary: November 1925. A freelance journalist receives two contradictory letters from a friend held at the Danvers State Hospital. She has five days. Realistic psychological horror with no supernatural elements.
---

# *Genius Loci*, Danvers, November 1925: "The Breathing Hill"
## Adventure file · Ruleset: `fear_itself` · Solo or party · Asynchronous play · No supernatural elements

> **How this file is organized.**
> **PART A** is the character sheet, the starting values and the party-play notes, and is **player-safe**: the AI Master may show any part of it at any time.
> **PART B** is the adventure and is **GM-ONLY**: never show, quote or summarize it to the player.
>
> This adventure is written for the ruleset `fear_itself` and is played with the generic protocol, oracles and state contract. This file supplies the world, the secrets, the cast and the character. It is **fixed content**: everything specific to one run (the characters' current state, what they know, what the NPCs have become) lives in the game and character records of the database, not here.
>
> Adapted from the structure of *Genius Loci* (Danvers asylum, a captive friend, a ritual at the dark of the moon). **Everything here is mundane.** There is no lloigor, no god, no Elder Sign, no telekinesis. The horror is a fungus, a man, a crowd, and the slow loss of the character's grip on what is real.

---

# PART A: THE PREGENERATED CHARACTER (player-safe)

## A1. Identity

- **Name:** Eleanor Vance
- **Concept:** Dutiful freelance journalist
- **Occupation:** Freelance correspondent for regional newspapers and literary magazines
- **Era / place:** November 1925; Boston-based by default (her lodgings are within a day's post and train ride of Danvers)
- **Age / appearance:** Not fixed by the source sheet. Leave them open unless the player supplies them; the GM never invents physical details the player has not offered, beyond what a scene needs.
- **Risk Factor (Drive): Duty** — to expose institutional harm and protect the vulnerable through truth.
  - **Hard** when the choice is to abandon Larry or leave vulnerable people in danger she knows about (resisting costs 4 Stability or one third of a pool, whichever is greater).
  - **Soft** when the pull is only toward printing or exposing the story (resisting costs 2 Stability).
  - Used as a nudge toward action, never as a punishment for caution.
- **Personal goal:** Bring Larry home safely, and put what she learns into print in a form no editor or lawyer can wave away.

### Hook
Lawrence "Larry" Croswell is a former colleague from her days covering New England folklore societies; they collaborated on a pamphlet about Victorian burial customs three years ago. His letter is not just a professional lead — it is a plea from someone who once trusted her judgment to see beyond polite fictions. She feels obligated to act, not merely curious.

---

## A2. Investigative Abilities (never rolled) — 26 build points

| Ability | Rating | What it covers for Eleanor |
|---|---|---|
| Research | 8 | Libraries, newspaper morgues, archives, town and county records, directories |
| Bullshit Detector | 5 | Spotting lies, evasions and rehearsed statements (psychopaths can evade it) |
| Reassurance | 4 | Calming frightened people, earning trust, gentle extraction of information; her oral-history interviewing technique |
| Medicine | 3 | Reportorial and self-taught medical knowledge from hospital and public-health beats. **Not a licensed physician**: she cannot legally practise, certify, or perform autopsies |
| Negotiation | 2 | Bargaining, brokering access, trading favours |
| Flattery | 1 | Charming officials and clerks |
| Interrogation | 1 | Pressing a subject in a formal or confined setting |
| Notice | 1 | Small physical details |
| Bureaucracy | 1 | Forms, procedures, who signs what |

*Investigative pools are spent for extras (see the ruleset). Having 1+ in an ability automatically yields its essential clues when she uses it in a relevant scene.*

## A3. General Abilities (rolled with a d6) — 60 build points

| Ability | Rating | | Ability | Rating |
|---|---|---|---|---|
| Health | 8 | | Medic | 4 |
| Stability | 12 | | Athletics | 4 |
| Preparedness | 6 | | Fleeing | 4 |
| Infiltration | 6 | | Driving | 3 |
| Sense Trouble | 5 | | Shrink | 2 |
| Hiding | 4 | | Mechanics | 2 |

**Not rated (automatic failure if attempted as a rolled test):** Filch, Scuffling, Shooting. She is not a fighter.
**Hit Threshold:** 3 (Athletics is below 8).
**Build checks passed:** 60 General points spent exactly; second-highest General (Health 8) is at least half the highest (Stability 12); no capped abilities (Occult Studies, Investigative Procedure, Scuffling, Shooting) are held; no Fleeing/Hiding discounts claimed.

## A4. Pool tracker (current / maximum)

These are the **starting values**. During play the current values live in the game database (the character record, state contract §3.5), not in this file. Health may go below 0; Stability may go below 0.

```
INVESTIGATIVE
Research 8/8 · Bullshit Detector 5/5 · Reassurance 4/4 · Medicine 3/3
Negotiation 2/2 · Flattery 1/1 · Interrogation 1/1 · Notice 1/1 · Bureaucracy 1/1

GENERAL
Health 8/8 · Stability 12/12 · Preparedness 6/6 · Infiltration 6/6
Sense Trouble 5/5 · Hiding 4/4 · Medic 4/4 · Athletics 4/4
Fleeing 4/4 · Driving 3/3 · Shrink 2/2 · Mechanics 2/2

CONDITIONS: none
```

---

## A5. Sources of Stability

Stability 12 supports up to four sources (one per 3 points). Following the one-shot convention, **only one is set at the start, and it is a person**; the rest are discovered in play and become available once the player has shown them on the page.

1. **Person (set at start): Peg Doyle**, her editor and old friend. *(Default; the player may swap in someone else at the start of play.)*
2. **Trait (unlock in play):** stubborn faith in documented fact.
3. **Activity (unlock in play):** typing up her notes at day's end.
4. **Second person (unlock in play):** the player may name one more.

Reconnecting with a Source of Stability (a call to Peg, an evening with her notes) refreshes 2 Stability, once per Source per in-world day.

## A6. Relationships and allies (GM-controlled, never rolled for her)

- **Larry Croswell** — the reason she is here.
- **Peg Doyle** *(added for solo play)* — Eleanor's editor at a Boston daily. Reachable by telephone or telegram. Brisk and sceptical; can provide press leverage, a cover assignment, and a sounding board. Wants documentation before she will print or push.
- **Dr. Samuel Whitcombe** *(added for solo play)* — a Salem general practitioner, antiquarian, and old correspondent of Larry's from the folklore circle. Can offer independent medical corroboration. Reached through Peg, Larry's contacts, or Research.

Allies fill the gaps in her sheet (see §A8). They advise and assist; they never act in her place or decide for her.

## A7. Means and equipment

- **Means:** modest freelance income. She can afford train and local hired-car fares, a boarding house room, telegrams, telephone calls and small gratuities. She cannot buy large bribes or fund a legal campaign without Peg.
- **Transport:** train to Danvers or Salem, hired cars, or a borrowed car (Driving 3).
- **Starting kit:** notebook and pencils, fountain pen, press card, electric torch, coins for telephone boxes, Larry's letter, the hospital's letter.
- **Other items:** produced with a Preparedness test, subject to period plausibility and what the fiction has established.
- **Era limits:** no portable telephones, no computers, no modern gas or air-quality instruments.

## A8. Known gaps (for the GM and player)

Eleanor has no Cop Talk, Streetwise, Law, Science, Photography, Occult Studies, Investigative Procedure, Mechanics beyond 2, or combat skills. The adventure routes every essential clue through at least one ability she has, a Simple Search, or an ally, so none of these gaps can stall the story. They do shape how expensive, slow and risky each route is.

---

## A9. How this sheet was converted (for traceability)

The original sheet was written for a different rules set (Trail of Cthulhu style). It was converted to Fear Itself as follows.

| Original entry | Fear Itself result | Note |
|---|---|---|
| Library Use 8 | Research 8 | Direct equivalent |
| Assess Honesty 5 | Bullshit Detector 5 | Direct equivalent |
| Medicine 3 | Medicine 3 | Rating kept; flagged as unlicensed reportorial knowledge |
| Persuasion 6 | Negotiation 2, Flattery 1, Bureaucracy 1, Reassurance 2 | Fear Itself splits "Persuasion" into several Interpersonal abilities |
| Oral History 4 | Reassurance 2, Interrogation 1, Notice 1 | Her interviewing craft |
| Stability 5 | Stability 12 | Fear Itself pools are larger; bought from the 60 General points |
| Stealth 4 | Infiltration 6, Hiding 4 | |
| Preparedness 3 | Preparedness 6 | Rescaled |
| Persuasion (General) 2 | (none) | Fear Itself Interpersonal abilities are Investigative and unrolled; points redistributed to Sense Trouble, Medic, Athletics, Fleeing, Driving, Shrink, Mechanics and Health |
| Credit Rating 6 | Narrative "Means" (§A7) | Fear Itself has no equivalent ability |
| Drive: Duty | Risk Factor: Duty | Hard/Soft rules in §A1 |

**Budget note (house rule):** the published Fear Itself budget for Investigative abilities assumes a group (for example 16 points each for two players). A solo character has no one to cover her gaps, so she keeps the original sheet's total of **26** Investigative points. General abilities use the standard 60. Health and Stability are bought from that 60.

---

## A10. Party play: scaling Eleanor and additional characters

Eleanor is built on the solo budget (26 Investigative points). In a party she is rescaled (the ruleset §2.2) to the budget for the party size at the start. This trim table wins over the general trimming rule. Her General abilities (60 points) do not change.

| Party size | Budget | Research | Bullshit Detector | Reassurance | Medicine | Negotiation | Flattery | Interrogation | Notice | Bureaucracy |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 (solo) | 26 | 8 | 5 | 4 | 3 | 2 | 1 | 1 | 1 | 1 |
| 2 | 22 | 6 | 4 | 3 | 3 | 2 | 1 | 1 | 1 | 1 |
| 3 | 18 | 5 | 3 | 3 | 2 | 1 | 1 | 1 | 1 | 1 |
| 4 | 16 | 5 | 3 | 2 | 2 | 1 | 0 | 1 | 1 | 1 |
| 5 | 14 | 4 | 3 | 2 | 1 | 1 | 0 | 1 | 1 | 1 |

**Other characters.** This file has no other pregenerated characters. Players may create their own with quick creation (the ruleset §2), bring a sheet to be checked (the ruleset §2.1), or ask the AI Master to generate pregenerated characters on demand (the ruleset §2.2). Useful gaps to cover, because Eleanor has none of them: Law or Cop Talk, Science or Photography, Streetwise, and a steadier body.

**Hook variants for additional characters.** Each character needs a reason to be in Danvers and a copy of Larry's letter (Handout 1) or the hospital's letter (Handout 2) with their own name in the salutation. Choose one per character, or invent a similar one:

- A friend of Larry's from the folklore societies, who received a second pencil letter in the same batch.
- A colleague of Peg Doyle's, a junior reporter or a photographer, assigned to go with Eleanor.
- A younger physician or assistant of Dr. Whitcombe's, asked as a favour to look in on Larry.
- A relative of a patient at the hospital, who has received the same kind of typed letter asking them not to visit.

Each additional character is also a possible Source of Stability for the others (the ruleset §2).

---

# PART B: THE ADVENTURE (GM ONLY)

> **GM ONLY.** Never show, quote or summarize Part B to the player. Behavior is governed by the protocol, rule numbers by the ruleset, random tables by the oracles, and the database and message shapes by the state contract.

## 0. Using this file

**Setup parameters (module contract, protocol §16.1).**
- **Format:** solo (Eleanor Vance, pregenerated in Part A) or a party of up to five (Eleanor scaled by the table in A10, plus other characters created or generated by the rules in the ruleset §2). Peg and Whitcombe are GM allies in both.
- **Pace:** *slow* starts on Day 1 Morning (Handout 1 arrives at her lodgings); *fast* starts on Day 2 Afternoon, stepping off the train at Danvers with both letters already in her bag.
- **Era and place:** Massachusetts, November 1925 (era notes in §14).
- **Tone preset:** Sordid and Gritty (ruleset §1).
- **Modules on:** hazard stages (ruleset §4.6), Perception Drift (ruleset §5.1), Belief states (ruleset §5.4), Heat ladder replaced by §7 below, Blocks and clocks (ruleset §5.3).
- **Default Source of Stability:** Peg Doyle.

**Principles.**
- **The schedule is a ceiling, not a track.** If the character acts sooner, move the beats. The clock runs regardless.
- **Fair play.** Every essential clue has at least three routes, a Simple Search, or an ally. Hallucinations never carry essential clues. Warnings precede lethal danger.
- **Spine:** Letters, then the hospital, then the pattern in the air, then the history, then the date, then the finale at midnight on Day 5.
- **Three ways to win, any combination:** get Larry out; document the truth so the State acts; stop or blunt the rite. She must also keep her own mind.
- **Tone:** sordid and gritty. Authorities do not help without documents. Time is short.

### 0.1 Asynchronous play (adventure contract item 17)

**Recommended settings.** Lethality `moderate` (default). `tick_span: day` (four Blocks per tick) and `tick_interval_hours: 24`, with `early_close: true` in solo play and `false` in a party. Tick 1 is Day 1, and so on, so the adventure runs five ticks at the slow pace and four at the fast pace (Day 2 Afternoon is a short first tick of three Blocks). A table that wants finer play may use `tick_span: block`.

**State to seed at the start of `active`** (protocol §16.2). Create `npc_state` records for the NPCs of Part C that matter at the start (belief state, location, attitudes, inventory, schedule), and `location_state` records for the starting places, scheduled events from §5, the starting `gm_state` (Tension 2, Heat 0, intensity mild, the clock), and each character's starting location (Boston lodgings, or Danvers Square at the fast pace). Do not copy this file into state.

**Scheduled events.** Make one for each row of §5: Letter 1, Letter 2, the interview with Berger when a character asks for it, MacBride's call, staff in street clothes, the Hour-of-Telling invitation, MacBride's visit, the Herald notice, the inspector window, the rite. The schedule is a ceiling: if characters act sooner, move the beat. An event fires at its Block whether or not a character is there.

**Events aimed at "Eleanor".** In a party, aim each event at the character who fits its condition:
- Letters reach every character who has a hook (A10).
- A call to the lodging reaches whoever is at the hall telephone. If nobody is, Mrs. Tolland takes a message and passes it on in the morning.
- MacBride's night visit goes to the room of the character who has been most visible. The others hear a disturbance.
- Shadowing and sabotage target the character who made the most noise (§7).

**Exposure.** At the end of each Block, add Exposure Points for each character's zone and the day's intensity (§2.2) and subtract recovery. Heat is shared by the party (§7).

**Spend offers.** Investigative extras (for example a second page of Shine's journal, or a clerk's remark about the 1922 minutes) are offered as spend offers for the next tick rather than lost.

**Clues in a party.** Each essential conclusion in §6 must be reachable by more than one character and by more than one tick. A clue belongs to the character who found it until they share it in the fiction (protocol §5.4).

**The finale in crisis ticks.** From about 10:30 pm on Night 5, switch to `beat` ticks. By default one tick covers two Beats (Beats 1 and 2, 3 and 4, 5 and 6, then 7). Each character's action lists what they do Beat by Beat, with contingencies. Decision gates stop the plan before Beat 5 (the Offering, the point of no return for Larry), before Beat 6 (a Drift 5 character's Surface test and the Hard Risk Factor), and before any step that could kill a character (protocol §6.5). A table may instead agree a compressed finale: one crisis tick with gates at the same points. The crisis tick interval is set by the table. In solo play with early close, the finale resolves as fast as the player submits.

**Absent characters at the finale.** They are not exposed to lethal risk (the ruleset §6.4). Place them somewhere safe: Mrs. Tolland's house, the old farm cottage, Whitcombe's house. If Larry is out of reach, the rite's offering falls on someone else (§9) only through a character whose player walked past a decision gate.

---

## 1. The truth (what is really going on)

**1.1 The hill and the cellar.** Hathorne Hill holds the foundations of Judge John Hathorne's old homestead. On the slope above the reservoir lies the stone-lined cellar and spring chamber of that house, half sunk in the earth, its vault roof only about a yard below the grass. In its damp dark grows a pale mushroom with a grey-blue cap that bruises darker blue where touched (the gardeners later call them *Hathorne's caps*). People near it have always been peculiar. Local lore calls the hill "witches' ground", and the indigenous people before the settlers avoided it and marked the cellar mouth with a carved warning stone, a flame inside a star. Hathorne dismissed the stone as a pagan sign, removed it, and built his house on the place. His zeal in the witch trials is, in this telling, partly the work of a man breathing air he should not have been breathing. This is a theory the world of 1925 does not hold.

**1.2 Dr. Shine's stone.** Dr. William Shine, superintendent from 1890 to 1915, a physician and world traveler who had seen mushroom ceremonies abroad, mapped the asylum's accidents ward by ward and month by month and found them downwind of the hollow. He found the cellar, the pale caps and the old warning stone lying in a barn. He had the stone set over the cellar mouth beside the reservoir and bricked the vent. Patient accidents fell. He told no one the true reason, because he would have been committed himself, and he begged his successor never to move the stone.

**1.3 The amphitheater, 1922.** Dr. James Berger, superintendent since 1915, built an amphitheater for the patients on the slope. His workmen, patient laborers led by Andrew MacBride, broke up and hauled away the capstone, cut drains, laid tiered stone seats and filled and graded the slope. The tiers sit directly over the old vault. The drains opened a new vent into the old spring conduit that runs down to the hospital's steam tunnels. The fungus colonized the manure and compost beds of the kitchen garden, the amphitheater flowerbeds, and the drains. The tunnels carry its spores to the steam plant, the greenhouse and the fresh-air shafts that feed the wards. Each autumn the fruiting grows worse.

**1.4 The air.** The spores are the cause. Dust and aerosol drift through the tunnels and ventilation. Cold weather, rain and closed windows push them indoors and concentrate them. Kitchen-garden produce adds a lighter second exposure. The effect is headache and drowsiness, then a loosening of perception: suggestible, vivid, frightening. Over weeks it produces a shared delusional state. In 1925 no one can explain this pharmacologically. A physician like Whitcombe can only observe that the symptoms follow the air and the place.

**1.5 Berger and the Guest.** Berger sleeps above the boiler plant, in the worst of the air. Lonely, ambitious and brilliant, he was first and heaviest exposed. He read his visions as a mission. He began "the Hour of Telling" each morning in the dining hall, where patients and staff recount their dreams and he records them in a green ledger. Those accounts converged on one image, a many-eyed, toad-headed figure rising from water. He taught them it was the **Guest**, a visitor from beyond the sky, who will come on the dark of the moon, cure all suffering, and take the wounded into peace if it is welcomed with blood. The painting in his office, a gift from a patient, shows St. George losing to the dragon. Newcomers convert in weeks. This is mass induced delusion (*folie à plusieurs* to a period physician), driven by the spores and a charismatic leader.

**1.6 The rite.** On the dark of the moon, at midnight, staff and willing patients process with torches (flames tinted blue-green by copper salts) from J Ward to the amphitheater beside the reservoir. They sing a plain litany, wound one another in a frenzy of devotion, and offer a sacrifice. This month the offering is Larry Croswell, whom Berger judged "willing" because he is lucid enough to be useful and a witness too dangerous to release.

**1.7 What is not true.** There is no Guest. The "glow" on the reservoir is foxfire from fungus in the rotten timbers and a spore film on the water, plus fog and torchlight. The "many-eyed dragon" is shared suggestion fed by Berger's imagery and the painting. The finale's "implosion" is a sinkhole: the vault roof collapses under the packed crowd and the saturated slope.

---

## 2. The spore system (this adventure's parameters)

This section gives the adventure's settings for the hazard stages (the ruleset §4.6) and the Perception Drift module (the ruleset §5.1). The generic rules (Drift levels, Slips, Check Reality, lost time, notebook rule, anchors, Immersion and Surface test, fairness limits) are in the ruleset §5.1 and apply unchanged.

### 2.1 Intensity clock (the ruleset §4.6)

| Day | Intensity | Why |
|---|---|---|
| 1 to 3 | Mild | Mild damp, windows still open |
| 4 | Moderate | Rain, cold, windows shut, steam higher |
| 5 | Severe | Cold snap and fog, steam at full, fruiting at its autumn peak |

Stage times in the ruleset §4.6 apply to time inside Active and Hot zones. In Fringe zones the stage clock runs at half speed.

### 2.2 Zones and Exposure Points (EP)

Track Exposure Points privately. Each Block mostly spent inside a zone adds EP. A visit of an hour or less counts as half. Round up only in Hot zones.

| Zone | Mild | Moderate | Severe |
|---|---|---|---|
| Clear (town, boarding house, Salem, Boston, libraries) | 0 | 0 | 0 |
| Fringe (gate lodge, drive, front office, visitors' parlor, chapel porch) | 0 | 1 | 1 |
| Active (wards, corridors, dining hall, laundry, kitchens, superintendent's quarters) | 1 | 1 | 2 |
| Hot (greenhouse, kitchen garden, steam plant and tunnels, amphitheater, reservoir shore, J Ward, Berger's quarters) | 2 | 2 | 3 |

**Recovery.** A Block in Clear air removes 1 EP. A night's sleep in a Haven removes 2. A room with a window opened to cold, clean air may add a little at the GM's discretion. EP cannot go below 0 and caps at 15.

### 2.3 Bodily effects and cues

Use the ruleset §4.6 for the body (Cues, then stages). Cues available in this adventure, at least two before any Health test: stale warm air that smells of cellars and wet leaves; a dull headache; drowsy patients; staff rubbing their temples; a caged canary drooping in the superintendent's anteroom; a grey dust like ash on ledges and windowsills; condensation on grilles; blue-grey bruising on damp stone and bark; a metallic sheen on the reservoir; dew rings in the garden lawn. A Sense Trouble spend (blind) can identify "the air" as the problem.

### 2.4 Drift settings

- Uses the default EP thresholds of the ruleset §5.1 (Drift 0 at EP 0 to 1, 1 at 2 to 3, 2 at 4 to 6, 3 at 7 to 9, 4 at 10 to 12, 5 at 13 to 15).
- Slips occur in Active or Hot zones. Use the Slip tables in Appendix A of the ruleset with **{Anchor}** = Peg (or Larry) and **{Belief}** = the Guest.
- A Stage 2 bodily effect counts as +1 Drift while it lasts.
- At the finale, Drift 5 without a successful Surface test means she joins the rite, as in the ruleset §5.1.
- Slips are delivered as ordinary perceived facts with a tell. Check Reality and the Surface test are automatic, using the anchor named in the player's standing orders (the ruleset §5.1, asynchronous handling).

### 2.5 Anchors and Sources of Stability

Anchors that help her: a call to Peg (refreshes 2 Stability once per day, the ruleset §4.8), typing up her notes in a Haven (second Source), documented facts (her trait Source), Larry's letter and her press card (touch, narrative), fresh air, a grounding word from Whitcombe. Each lets her Check Reality at Difficulty 1 lower **once per scene** when she names the anchor she uses.

### 2.6 Narration palette

Mix the palette across senses. Keep most of the text ordinary.

| Drift | Sight | Sound | Smell, taste, body | Time and mind |
|---|---|---|---|---|
| 1 | Colors a shade too bright, a lamp too white | The hum of pipes slightly louder | Pennies on the tongue, tight headache | Minutes feel thick |
| 2 | Motion at the edge of vision; stains turn into eyes | Her name, politely, from an empty corridor | A smell of wet earth in dry rooms | She checks her watch twice |
| 3 | Faces slow, smiles that last too long; patterns repeat | Voices overlap in unison; Larry's voice, Peg's voice | Warmth that smells like a cellar | Cause and effect blur; everything feels like a message |
| 4 | Walls breathe; the floor is warm; rooms slide | A hymn too low to place; footsteps that match hers | Her hands tingle; her mouth is full of earth | She loses minutes; Peg on the telephone sounds wrong |
| 5 | A rosy clarity; the Guest in every grain | Kind voices explaining | Peace in the chest | Fear is gone; the explanation seems obvious |

Examples to adapt:
- Drift 1: "The corridor floor shines wet though it was mopped an hour ago. You can taste pennies."
- Drift 2: "Behind you someone says your name, politely, the way a clerk does. The corridor is empty. The stain on the plaster has more eyes than it had."
- Drift 3: "Nurse Hallett is smiling. Nurse Hallett is not smiling. You write the word smiling and cross it out."
- Drift 4: "The ward is breathing. In. Out. You count with it and the count is yours and not yours."
- Drift 5: "It is a mercy, you think, that someone finally explains. Everyone is so kind. The stones are warm."

### 2.7 Adventure-specific limits

1. Never name the cause in narration (no "spores", no "fungus") until she has the clue. She may suspect "the air".
2. Draw hallucinations from the fears the player named and from Larry, Peg, the unreachable exit, being disbelieved and the hospital's own imagery.
3. All other fairness limits are in the ruleset §5.1.

---

## 3. The cast

All NPCs have a visible trait and a goal. Spore state is given as Clear, Clouded, Devout or Frenzied.

**Lawrence "Larry" Croswell** (52). Writer of New England folklore. *Trait:* a pencil behind his ear and restless hands. *Goal:* leave and warn. *State:* Clouded, sedated at times, thinner each day. Larry gave her the clues in his pencil letter. He keeps folded notes sewn in his mattress: a rough map of which wards are worse and when, patients' names, the staff's scars (**E7**). He is partly reliable: some of his stories carry his own slips. Use Bullshit Detector and Interrogation to separate them.

**Dr. James Berger** (39). Superintendent. *Trait:* pale green eyes, always touching the third button of his coat, speaks slowly. *Goal:* bring the Guest on the dark of the moon. Devout. Polished and courteous with outsiders, absolutely certain. Berger cannot be persuaded or intimidated. He sleeps above the boiler plant and keeps the green ledger in his office safe. His anteroom has a caged canary; it is drooping.

**Nurse Hallett.** Desk nurse. *Trait:* half of her left ear is missing, she touches the scar. *Goal:* keep order. Devout.

**Orderlies Kessler and Mull.** Large, quiet, scarred wrists. *Goal:* obey Berger. Kessler is Devout. Gus Mull has a wife in Peabody and is wavering, Clouded.

**Thomas Greer.** Night attendant, 22, three weeks in the job, on the west wing. *Trait:* trembling hands. *Goal:* leave, and protect his sick mother. Clear but fraying. He can become a witness (**E4**) or a way in, with Reassurance.

**Andrew MacBride** (56). Patient, laborer foreman of the amphitheater crew. *Trait:* hums hymn tunes, huge gentle hands. *Goal:* confess and stop it. Clouded. His ward, H Ward, is in the cold west wing with a broken steam line and he works outdoors, so he is clearer than most. He calls Eleanor on Night 3 and visits her on Night 4. He is found dead on Day 5 Morning.

**Peg Doyle.** Eleanor's editor. *Trait:* an unlit cigar. *Goal:* a story she can print and defend. Clear. Will not print without documents, will give press leverage, will join Eleanor if she is called to Danvers by Day 5.

**Dr. Samuel Whitcombe.** Salem general practitioner, antiquarian, correspondent of Larry. *Trait:* spectacles pushed up on his forehead. *Goal:* the truth, and a safe place to examine. Clear. Owns a microscope. Believably an associate medical examiner for the district (keep vague, 1925). He will not go near the hospital.

**Mrs. Abigail Tolland.** Landlady in Danvers Square. *Trait:* speaks in a whisper. *Goal:* quiet. Her nephew Walter, a hospital cook, comes to dinner quiet and hollow-eyed and has begun to report on lodgers. Her house is Eleanor's Haven until Night 4.

**Inspector Edwin Pratt.** State Department of Mental Diseases. *Trait:* gloved, precise. *Goal:* protect the Department from scandal. Will act only on documents and a credible witness.

**Chief Ormsby.** Danvers police. *Trait:* chewing a toothpick. *Goal:* avoid trouble with the state hospital. Cannot act without evidence.

**Miss Cora Wentworth.** Librarian, Peabody Institute Library, Danvers. *Trait:* ink-stained fingers. *Goal:* help a researcher. Clear.

**Staff in street clothes.** Men sent by Berger to follow Eleanor. They deny everything and flee if cornered.

---

## 4. The places

| Place | Zone | Past detail | Notes |
|---|---|---|---|
| Danvers Square, Mrs. Tolland's house | Clear | The wallpaper was hung by her late husband | Haven; hall telephone |
| Peabody Institute Library, Town Hall, Danvers Herald, Salem News, Danvers Historical Society | Clear | Dusty drawers of 1922 minutes | Research |
| Salem: Dr. Whitcombe's house, Salem Hospital archive | Clear | Shine's papers languish in a basement | Shine's journal (E1) |
| Gate lodge, drive, front office, visitors' parlor | Fringe | Worn marble where hundreds waited | Admission; permission |
| Main building and wards (H Ward west wing; Dining Hall) | Active | Brass plaques of founders | Hour of Telling, 7 am |
| J Ward (cell J-12) | Hot | Steel doors added in 1919 | Larry |
| Laundry, kitchens | Active | A brick oven from the first decade | Walter Tolland |
| Greenhouse and kitchen garden | Hot | A trowel rusted into a wall | Compost beds, blue-grey caps |
| Steam plant and tunnels | Hot | Names scratched in the brick | Spore path; Escape route |
| Amphitheater and reservoir shore | Hot | New stone against old stone | Finale site |
| Potter's field | Fringe | Numbered stakes, no names | MacBride buried |
| Old farm cottage | Fringe | A cracked churn | Clean-air refuge on the west |

---

## 5. Timeline and clock

Five days, four Blocks each (Morning, Afternoon, Evening, Night). The ritual is at midnight on Night 5. At the default tick span each Day is one tick (§0.1).

| Day | Intensity | Events |
|---|---|---|
| 1 | Mild | **M:** Letter 1 (pencil) arrives at her lodgings. **A to E:** free scenes: call Peg, Boston library, preparation. **N:** sleep |
| 2 | Mild | **M:** Letter 2 (typed) arrives. Decision, train to Danvers. **A:** arrive Danvers Square, Mrs. Tolland's; she may approach the hospital gate. **E, N:** lodgings |
| 3 | Mild | **M:** Interview with Berger, request for a visit. **A:** supervised visit to Larry if allowed, or research. **E:** research, Greer or Walter Tolland. **N:** MacBride's call |
| 4 | Moderate | **M:** staff in street clothes appear. **A:** research or confrontation. **E:** possible Hour-of-Telling invitation from Berger; sabotage. **N:** MacBride visits her room (Haven breached) |
| 5 | Severe | **M:** Danvers Herald death notice; Larry moved to seclusion. **A:** inspector window; preparation. **E:** staging. **N:** 11 pm to 1 am: the rite |

**Larry's location:** J-12 until Day 5 Evening, then sedated in a seclusion room beside the J Ward service door. At 11 pm he is wheeled out on a gurney with the procession.

---

## 6. The clue matrix

Each conclusion has at least three routes. Any route suffices.

| # | Conclusion | Routes |
|---|---|---|
| C1 | The typed letter is coerced and the hospital is lying | Automatic (Eleanor knows Larry never types and never uses "Lawrence"); Bullshit Detector on Berger's phrasing; Notice a mismatched signature |
| C2 | Staff are afraid and bear scars | Notice (Hallett's ear, Mull's wrists); Medicine (bite and gouge wounds, not infections); Reassurance with a patient; Larry |
| C3 | Larry is in J-12 and is not allowed visitors | Berger's office; Hallett; Cop Talk is absent so Negotiation, Flattery, Bureaucracy with the office; Greer |
| C4 | The trouble follows the air and the place | Sense Trouble spend (blind); Medicine (the pattern); Larry's notes (E7); the canary; Whitcombe; MacBride; Research (annual reports show ventilation complaints) |
| C5 | The amphitheater site is the wound | Handout 3; MacBride; Notice (blue-bruised caps, drainage); Shine's journal |
| C6 | The hill's history: Hathorne, the cellar, the warning stone, Shine | Research (libraries, Historical Society); Whitcombe; Shine's papers in Salem |
| C7 | The date: the dark of the moon, midnight, Day 5 | Larry's visit; MacBride's call; an almanac (Research); Peg |
| C8 | The ground below the amphitheater is hollow | Shine's journal; Historical Society plan of the homestead; MacBride; Notice (cracks in the tiers, seepage) |
| C9 | What the authorities need to act | Peg; Bureaucracy; Whitcombe |
| C10 | Ways in and out of the hospital | Greer; the tunnel hatch (Notice or Infiltration); Mull; laundry cart; Larry |

**Floating clues** (release to unstick play): Peg telegrams a quote from the annual report; Whitcombe telephones with a lead on Shine's papers; MacBride's call; Greer approaches her at the library.

---

## 7. The antagonist's reactions (escalation)

Berger and his followers respond in proportion, by human means. Raise the rung each time a character makes noise (visiting, questioning staff, contacting the State). In party play the rung is shared by the group, and the reaction targets the character who made the noise.

1. **Courtesy:** Berger receives her politely, offers tea, delays.
2. **Watching:** staff in street clothes appear at libraries and the station.
3. **Veiled warnings:** "Let things be." "Stay away from Danvers."
4. **The night call:** hall telephone, static, MacBride's voice.
5. **Sabotage:** slashed tires, loosened wheel nuts, a smear on the windshield of a blood-colored many-eyed figure, loosened pipes in her lodging (warn first: a cue that a wheel feels wrong).
6. **Invitation:** Berger invites her to an Hour of Telling "to see the method". Heavy exposure and a recruitment attempt. If she goes she gets C2, C4, a glimpse of the green ledger (E8), and +2 EP.
7. **Abduction attempt:** at night on the road or at the station.

---

## 8. Evidence and outside help

| Id | Evidence | Source |
|---|---|---|
| E1 | Shine's journal pages | Salem Hospital archive; Research; Whitcombe |
| E2 | State annual reports: injuries and deaths rising since 1922 | Research |
| E3 | Whitcombe's statement and microscope notes on the fungus | A sample from the garden (Infiltration or Notice); Whitcombe |
| E4 | Sworn statement from Greer | Reassurance, protection |
| E5 | MacBride's death inconsistent with suicide | Whitcombe examines the body; Medicine |
| E6 | Larry's testimony | After rescue |
| E7 | Larry's notes | J-12 mattress |
| E8 | The green ledger of dreams | Berger's safe; very risky |

**Trigger.** With **three pieces** including E3 or E5, Peg and Whitcombe can raise Inspector Pratt. If raised by Day 4 Evening, he arrives Day 5 at 2 pm with a constable. Berger stages a sanitized tour. A decisive extra (Larry himself, Greer's statement, or the green ledger) turns the visit into an inspection that orders Larry discharged into Whitcombe's care and orders windows opened and wards aired. This does not stop the rite that night: the loyal remnant still goes ahead, and Eleanor must choose whether to go.

---

## 9. Getting Larry out before midnight

- **By law:** needs the Inspector (§8).
- **By stealth:** the laundry cart at the afternoon change; the tunnel hatch from the greenhouse to the cellar level beside J Ward; Greer's key during the evening shift; the service road at 10:30 pm. All of these run through Hot zones.
- **At the finale:** take him off the gurney.

If Larry is out, Berger improvises. Staff hunt in the town on Night 5. The rite picks another offering: Eleanor herself (if reachable), Greer, or a patient. Her Duty (Hard Risk Factor) then pulls her back toward the hill.

**Escape Pool** (the ruleset §4.3, if she is trapped inside): start at 0; +1 to 3 per way-out clue (the tunnel hatch, the laundry cart, Greer's key, the shift change, the service road); +1 per relevant Investigative spend; +1 per relevant successful General test. Difficulty 8. Failure empties the pool and triggers a hazard (a locked door, a patrol, a Slip).

---

## 10. The finale: the dark of the moon

**Conditions.** Night 5, Severe. Cold fog, steam at full, the amphitheater thick with spore puffs lit by torches. Hot zone, 3 EP per Block. Eleanor is probably at Drift 3 to 5.

**Beats.** Each Beat is about five minutes of game time. The player may stretch or compress them by acting.

1. **Approach.** Hiding or Infiltration, Difficulty 4. She can see torches coming down from J Ward. Orderlies are recalled to the ritual, so the yard is empty.
2. **The procession.** Torches burn blue-green (copper salts, a Notice or Science clue). Larry on the gurney.
3. **The litany.** Hundreds speak together in plain words: "We are ready. We are open. We are ready." Berger leads, never touching anyone.
4. **The rite of wounds.** The crowd attacks itself in ecstasy. Larry loses Health each Beat she delays (use 1 per Beat, no more than 3 Beats before he is Seriously Wounded).
5. **The Offering.** Berger steps to the gurney with a long surgical blade. This is the point of no return for Larry.
6. **The Guest rises.** Fog, foxfire and torch glare make a vague shape above the water. At Drift 3 or higher she sees it as vast. Check Reality (Difficulty 3 plus Drift) to know it for fog. The crowd screams.
7. **The ground gives.** The vault roof fails beneath the central tiers. A sinkhole and the reservoir's seep take everything at the center.

**Fair warning (give at least three cues before Beat 7).** Cracks in the tiers (Notice or Infiltration); water standing in footprints; a dull knock from under the stone; Shine's line that the cellar vault is "barely a yard of earth below the grass" (E1); the tiers sinking slightly; the clogged drain.

**Ways through.** Break the gurney straps (Preparedness for scissors or a pocketknife, Difficulty 4). Reach Larry by moving along the outer edge (Infiltration, Difficulty 5). Wake him (Reassurance spend). Pull people from the circle: each Reassurance or Interrogation spend breaks one person away, and Eleanor decides who and how many. Hard Risk Factor: leaving vulnerable people in danger she knows about costs Stability.

**Berger.** Fate is open. If the player drags him from the pit he can be arrested. If not, he dies in the sinkhole.

---

## 11. Endings and epilogue

| Outcome | Result |
|---|---|
| Larry saved, Berger exposed, Eleanor lucid | Best ending. The State orders ventilation sealed, the garden burned, the cellar filled, the staff reviewed. Larry recovers slowly. The story is printed. |
| Larry saved, Eleanor Fractured | She finishes the story but takes months to trust her own senses. |
| Larry lost, truth printed | A grim win. Larry dies; Peg prints with the documents. |
| Eleanor committed or Lost | She is among the patients. Peg and Whitcombe fight to find her. |
| Eleanor dies | Narrate with weight. Resolve Larry's fate and the evidence. |

In party play, judge each character's outcome separately and give each player an epilogue for their own character.

After the finale, offer a debrief.

---

## 12. Difficulty sheet

| Test | Difficulty |
|---|---|
| Sneak past an unalerted orderly | 4 |
| Sneak past an alert orderly or at night in the yard | 5 |
| Pick an ordinary lock | 4 |
| Force a door | 5 |
| Climb the wall | 4 |
| Drive in mud or rain | 3 (4 in rain) |
| Hiding in shadow | 3 |
| Preparedness: a plausible item | 4 |
| Check Reality | 3 plus Drift (max 8) |
| Surface test at Drift 5 | 6 |
| Health, Bad Air Stage 2 | 4 |
| Health, Bad Air Stage 3 | 5 |
| Restrained by orderlies (Athletics or Fleeing) | 3 plus number of orderlies |

---

## 13. Handouts (show when found)

In party play, additional characters receive Handouts 1 and 2 with their own name in the salutation (A10). Record each handout a player holds in that character's knowledge (state contract §3.5).

### Handout 1: Larry's pencil letter (given Day 1 Morning)

> Dear Eleanor,
>
> I have put myself into the State Hospital at Danvers for my nerves, after the winter I had. It was a mistake and I think a bad one. I will be plain, since the mail is read here. There is something the matter with this place that is not the patients. The attendants are afraid, and the doctors, though they smile. Everyone has the same headache.
>
> They talk of moving me to a ward where no visitors are allowed, and I do not think I will be asked. I am slipping this out with a laundryman who owes me a kindness.
>
> Please come. If you cannot reach me, tell Peg where I am. Bring your press card and your patience. You will need both. Do not come on a visiting day. They put on a show.
>
> Your friend,
> Larry

### Handout 2: The hospital's letter (given Day 2 Morning)

> State Hospital at Danvers, 450 Maple Street, Danvers, Massachusetts. Office of the Superintendent.
>
> Dear Miss Vance,
>
> Please disregard the note I sent you. I was overwrought and wrote things that were not so. I am well cared for and I need rest, quiet and counsel, nothing more. Visitors would only set me back. I ask you not to come to Danvers.
>
> Sincerely,
> Lawrence Croswell

*(Typewritten. Signed in a shaky hand. Larry never uses "Lawrence" and never types.)*

### Handout 3: Danvers Herald, 1922

> **SUPERINTENDENT BUILDS AMPHITHEATER FOR PATIENTS.** Workmen at the Danvers State Hospital broke ground yesterday for an open-air amphitheater beside the reservoir, for the use of patients in fine weather. "A place where earth and water meet," says Superintendent Berger. Patient Andrew MacBride, foreman of the labor crew, reports that his men had some trouble breaking up and removing a large carved stone disk, set into the slope by Dr. Shine years ago. Some ratepayers question the expense. Dr. Berger replied that "the welfare of the afflicted is the welfare of all."

### Handout 4: Danvers Herald, 1915

> **DR. SHINE TO RETIRE.** After twenty-five years as superintendent at Danvers, Dr. William Shine will retire. Known for his kindly manner and progressive methods, he is credited with the hospital's recovery. Readers may recall the complaints when Dr. Shine placed a carved stone at the edge of the reservoir at public expense. He asked that it be left undisturbed. Of his successor, Dr. James Berger, he says: "I trust he will leave a few old stones unturned."

### Handout 5: Shine's journal (Salem Hospital archive)

> *June 1890.* The troubles at the asylum are not those of a rational administration. I have mapped them by ward and by month. They cluster on the lee side of the hollow behind the reservoir, and they worsen after rain.
>
> *September 1890.* I have found the old Hathorne cellar under the hill, half sunk in the earth. In its damp dark grows a pale mushroom with a grey-blue cap that bruises darker where touched. I saw the like in Siberia, in a ceremony. The people sat before the growth and spoke with their dead.
>
> *November 1890.* In a barn on the property I found a carved stone disk, a flame inside a star. It is old. I believe it was laid over the cellar mouth long ago as a warning. Hathorne must have removed it.
>
> *December 1890.* I have set the stone over the cellar and bricked the vent. Already the patients look as if they are waking from a long dream. I cannot publish this. I would be committed.
>
> *May 1915.* I have told Berger never to move the stone. I could not tell him why. The vault is barely a yard of earth below the grass.

### Handout 6: Danvers Herald, Day 5

> **PATIENT DIES AT DANVERS HOSPITAL.** Andrew MacBride, aged about 56, was found dead in his room this morning, an apparent suicide. "It is a tragedy when these things happen," said Superintendent James Berger. MacBride leaves no known relatives and will be buried in the hospital's cemetery.

### Handout 7: State annual report extract (E2)

| Year | Deaths by accident or self-inflicted injury | Injuries recorded as "infection or self-mutilation" |
|---|---|---|
| 1921 | 3 | 11 |
| 1922 | 9 | 30 |
| 1923 | 17 | 88 |
| 1924 | 26 | 140 |

### Handout 8: Larry's hidden notes (E7)

Pages of pencil on laundry paper sewn into his mattress: a rough plan of the wards with "worse" and "better" written beside them, names of patients, the scars he has seen on staff, and a line: *"The steam heat is the same in every ward. The air is not."*


---

## 14. Era notes: Massachusetts, 1925

- **Communications:** letters (one-day post between Boston and Danvers), telephone (hotel and boarding-house hall phones, telephone boxes, switchboards that listen), telegrams. No portable phones, no computers.
- **Travel:** trains, hired cars, a borrowed car. Roads are poor in bad weather.
- **Medicine:** carbon monoxide poisoning was known to physicians; miners used small caged birds. No portable gas meters. Treatments for mental illness included custodial care, sedatives, hydrotherapy and restraint. **Do not introduce lobotomy, insulin coma, electroconvulsive therapy or modern drugs.** The 1925 threats here are a back ward and commitment papers.
- **Law and bureaucracy:** visits to patients need written permission from the superintendent's office. Commitment papers can be long-lasting and hard to challenge. The state has a department that oversees public mental hospitals; a hospital's board of trustees exists; both respond to documents and credible witnesses, not to rumor.
- **Journalism:** a freelance woman reporter in 1925 meets skepticism and condescension; Peg Doyle is a rare ally. Libel is a real fear for editors.
- **Language:** the narrator uses plain, respectful terms ("patients"). Period official language ("insane", "nervous agitation") appears only in documents and institutional voices, never as the narrator's own. Avoid slurs and anachronism.

---

# PART C: IDS FOR FIXED RECORDS (GM only)

This adventure defines its NPCs and locations itself, in §3 and §4. A game refers to them by the stable ids below. Run changes go in `npc_state` and `location_state` records with these ids. Create a database `npc` or `location` record only for something not listed here. Part A's sheet is the pregenerated character `pregen_eleanor_vance`.

## C1. NPC ids

| id | Name | Role | Replacement candidate |
|---|---|---|---|
| `npc_larry_croswell` | Lawrence "Larry" Croswell | The captive friend | No (essential) |
| `npc_berger` | Dr. James Berger | Superintendent, antagonist | No |
| `npc_hallett` | Nurse Hallett | Desk nurse | No |
| `npc_kessler` | Orderly Kessler | Orderly | No |
| `npc_mull` | Gus Mull | Orderly | No |
| `npc_greer` | Thomas Greer | Night attendant | Yes, after Day 2 if he is Clear and free |
| `npc_macbride` | Andrew MacBride | Patient, foreman | No (dies Day 5) |
| `npc_peg_doyle` | Peg Doyle | Editor, ally | Yes |
| `npc_whitcombe` | Dr. Samuel Whitcombe | Physician, antiquarian, ally | Yes |
| `npc_tolland` | Mrs. Abigail Tolland | Landlady | No |
| `npc_walter_tolland` | Walter Tolland | Hospital cook, her nephew | No |
| `npc_pratt` | Inspector Edwin Pratt | State Department of Mental Diseases | No |
| `npc_ormsby` | Chief Ormsby | Danvers police | No |
| `npc_wentworth` | Miss Cora Wentworth | Librarian | Yes |
| `npc_staff_shadow` | Staff in street clothes | Berger's watchers | No |

A replacement candidate is marked `available_as_replacement: true` in its `npc_state` when it becomes plausible in the fiction.

## C2. Location ids

| id | Place | Zone |
|---|---|---|
| `loc_tolland_house` | Danvers Square, Mrs. Tolland's house | Clear |
| `loc_boston_lodgings` | Eleanor's lodgings, Boston (slow-pace start) | Clear |
| `loc_danvers_square` | Danvers Square, station and shops (fast-pace start) | Clear |
| `loc_peabody_library` | Peabody Institute Library | Clear |
| `loc_town_hall` | Town Hall, Danvers | Clear |
| `loc_herald` | Danvers Herald | Clear |
| `loc_historical_society` | Danvers Historical Society | Clear |
| `loc_whitcombe_house` | Dr. Whitcombe's house, Salem | Clear |
| `loc_salem_archive` | Salem Hospital archive | Clear |
| `loc_gate_lodge` | Gate lodge and drive | Fringe |
| `loc_front_office` | Front office and visitors' parlor | Fringe |
| `loc_main_wards` | Main building, wards and Dining Hall | Active |
| `loc_h_ward` | H Ward, west wing | Active |
| `loc_j_ward` | J Ward, cell J-12 | Hot |
| `loc_laundry_kitchens` | Laundry and kitchens | Active |
| `loc_greenhouse` | Greenhouse and kitchen garden | Hot |
| `loc_steam_tunnels` | Steam plant and tunnels | Hot |
| `loc_amphitheater` | Amphitheater and reservoir shore | Hot |
| `loc_potters_field` | Potter's field | Fringe |
| `loc_farm_cottage` | Old farm cottage | Fringe |

Zones follow §4 and §2.2. If the adventure text above disagrees with a zone here, §4 wins.
