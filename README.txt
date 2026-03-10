Project Aurora — Self-Learning Notification Orchestrator
========================================================
Team: Hostel 2613 | Kriti 2026 | SpeakX Challenge

ARCHITECTURE OVERVIEW
---------------------
Aurora is a 3-task, 7-stage pipeline that builds a domain-agnostic,
self-learning notification orchestration system. The pipeline ingests
a company Knowledge Bank (text/markdown) and user behavioral data (CSV),
then generates personalized notification schedules that improve over time
through reinforcement learning.

Task 1 — System Architecture & Intelligence Design:
  - Knowledge Bank Engine (Gemini 2.5 Flash): Extracts north star metric,
    feature-goal mappings, tone/hook matrix, propensity dimensions, and
    journey/goal templates from any company KB.
  - User Data Ingestion: 5-layer validation (schema, types, ranges,
    imputation, dedup) on behavioral CSV per the defined schema.
  - MECE Segmentation Engine: K-Means on KB-derived propensity space
    (gamification, ai_tutor, leaderboard, social) with silhouette sweep
    k=6-12. Within-lifecycle percentile normalization prevents lifecycle-
    stratified clusters. Persona naming via 3-axis (dominant, activeness,
    churn) key with iterative collision resolution.
  - Goal & Journey Builder: Generates primary goals, sub-goals, and
    day-on-day progression per segment x lifecycle from KB templates.

Task 2 — Communication & Timing Intelligence:
  - Theme Engine (Gemini): Maps top-3 Octalysis drives per segment.
  - Template Generator (Gemini REST): 5 bilingual templates per
    Segment x Lifecycle x Theme (Hindi + English), concurrent batched.
  - Timing Optimizer: 4-model comparison (RF, GB, LR, SVM) on
    preferred_hour -> time zone classification, outputs top-3 zones
    per user and per segment.
  - Schedule Generator (Claude Sonnet): Octalysis drive scoring,
    activeness-based frequency (3-9/day), zone-aware channel routing
    (push/in_app/whatsapp/sms), template-to-notification mapping.

Task 3 — Execution & Self-Learning:
  - RL Classification: Grid-search optimal reward weights (CTR, engagement,
    uninstall penalty). Bayesian engagement estimation. Quantile-based
    GOOD/NEUTRAL/BAD classification with confidence gating.
  - Strategy Generator: Traffic allocation (GOOD 70%, NEUTRAL 25%, BAD 5%),
    segment safety analysis (uninstall guardrails), optimal timing analysis.
  - Goal Updater (Gemini): 3-tier strategy — GOOD preserved, NEUTRAL gets
    A/B variants, BAD rewritten. Causal reasoning from RL data.
  - Iteration 1 Template Generator: Regenerates only changed templates.
  - Iteration 1 Schedule Generator: RL-informed template scoring, guardrail
    frequency reduction for high-uninstall segments.
  - Delta Report: Documents every change with causal explanations.

MODELS USED
-----------
  - Gemini 2.5 Flash (google-genai): KB extraction, theme mapping, goal
    optimization, template generation
  - Claude Sonnet 4.6 (anthropic): Drive scoring for schedule generation
  - scikit-learn: K-Means segmentation, Random Forest / Gradient Boosting /
    Logistic Regression / SVM for timing classification

RUN INSTRUCTIONS
----------------
Prerequisites:
  pip install pandas numpy scikit-learn scipy joblib google-genai
  pip install google-generativeai requests anthropic

Run full pipeline:
  python run_pipeline.py --data user_behavioral_data.csv --kb company_kb.md --experiment experiment_results.csv

Or run steps individually from the codebase/ directory:
  python codebase/task1_aurora.py
  python codebase/theme_engine.py
  python codebase/generate_templates.py
  python codebase/timing_optimizer.py
  python codebase/schedule_generator.py
  python codebase/task3_learning_engine.py
  python codebase/generate_delta_report.py

Input files (place in working directory):
  - user_behavioral_data.csv (1500 users, schema per PS)
  - company_kb.md (company knowledge bank)
  - experiment_results.csv (provided by SpeakX for Demo 2)

Windows compatible: All paths use os.path.join, no Unix-specific commands.
