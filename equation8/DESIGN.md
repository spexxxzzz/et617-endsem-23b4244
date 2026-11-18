# ET617 design: Equation8 / Find your balance

Identity: **23b4244**. Card: **P4-T3-L5-C4**. Topic: Class 8 linear equations in one variable.

## Educational problem
Aarav can carry out arithmetic but treats a term as changing sides without an inverse operation, and distributes a negative multiplier inconsistently. Repeating a failed topic has made him reluctant to expose uncertainty. The app gives a private, bounded sequence of explanations, varied tasks and evidence-based support. Success means independently explaining and applying equality-preserving operations, rather than obtaining a final value by guessing.

## Three outcomes
1. Solve one- and two-step linear equations and verify a solution by substitution.
2. Explain why the same operation on both sides preserves equality.
3. Identify and repair sign-change and negative-distribution errors.

## Persona
Aarav, 13, Class 8, English-medium learner. Uses a shared Android phone at home for one quiet 10-minute session. Can perform whole-number arithmetic; negative signs and inverse operations are fragile. Repeating after an unsuccessful test, he wants a fresh attempt without public comparison. Two misconceptions: M1 keeps the same sign when a term moves across equality; M2 applies a negative multiplier to only part of a bracket.

## Sequence and content
Welcome/confidence check (30 s); balance, inverse-operation and distribution examples (90 s); eight tasks across numerical, MCQ, error-correction and explanation formats (6 min); exit record/reflection (2 min). Optional stretch is outside the essential sequence. A 10-minute reminder offers pause without a penalty. Timing is a design target; a real learner trial is still needed.

## Adaptive decision
An incorrect basic skill or ambiguous explanation leads to prerequisite instruction and a small check. An answer matching the M1 or M2 error pattern leads to a different representation and targeted check. Two independently correct answers in succession offer a harder AI-generated equation. Hints break the independent-success streak. The learner can choose the regular path instead of the optional stretch. Model calls do not change the deterministic arithmetic answer key.

## AI and fallback
Hyde GLM-5.3 Flash assesses explanations, writes a small hint and generates a constrained stretch equation. Server-side keys only. Model JSON and enums are validated; generated arithmetic is checked exactly. Hints receive a second pass, with the limitation that this uses the same model. Invalid/failed calls use explicitly labelled reviewed support. Unclear explanations remain unscored.

## Evidence and remaining work
Unit/integration tests, live-provider smoke checks and browser scenario screenshots are kept under output/evidence. Public deployment, final repository sharing and AI chat exports remain submission work. The original Equation8 MIT project is named in the app and report; its Git history is retained.
