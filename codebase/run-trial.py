"""
Project Aurora — Full Pipeline Orchestrator
=============================================
Usage:
  python run_pipeline.py [--data user_behavioral_data.csv] [--kb company_kb.md]

Pipeline: Task1 → Theme Engine → Template Generator → Timing Optimizer
         → Schedule Generator → Task3 (RL + iter1 templates + iter1 schedule + delta report)
"""

import os
import sys
import shutil
import subprocess
import argparse
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

CODEBASE_DIR = SCRIPT_DIR
ITER0_DIR = os.path.join(PROJECT_ROOT, "iteration_0_before_learning")
ITER1_DIR = os.path.join(PROJECT_ROOT, "iteration_1_after_learning")

if CODEBASE_DIR not in sys.path:
    sys.path.insert(0, CODEBASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def ensure_dirs():
    os.makedirs(ITER0_DIR, exist_ok=True)
    os.makedirs(ITER1_DIR, exist_ok=True)


def step_banner(num, title):
    print(f"\n{'='*70}\n  STEP {num}: {title}\n{'='*70}\n")


def copy_iter0_to_iter1():
    """Copy files that don't change between iterations to iter1."""
    copies = ["user_segments.csv", "communication_themes.csv", "timing_recommendations.csv"]
    for name in copies:
        src = os.path.join(ITER0_DIR, name)
        dst = os.path.join(ITER1_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"   Copied {src} → {dst}")


def run_full_pipeline(data_path=None, kb_path=None):
    pipeline_start = time.time()
    ensure_dirs()

    # ── STEP 1: Task 1 ──────────────────────────────────────────────────────
    step_banner(1, "Task 1 — System Architecture & Intelligence Design")
    t1_path = os.path.join(CODEBASE_DIR, "task1_aurora.py")
    result = subprocess.run([sys.executable, t1_path], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"   Task 1 failed with code {result.returncode}")
        return
    print("\n✅ Task 1 complete.")

    # ── STEP 2: Theme Engine ─────────────────────────────────────────────────
    step_banner(2, "Theme Engine — Octalysis Drive Assignment")
    from theme_engine import run_theme_engine
    run_theme_engine()
    print("\n✅ Theme Engine complete.")

    # ── STEP 3: Template Generator ───────────────────────────────────────────
    step_banner(3, "Template Generator — Bilingual Notification Templates")
    t2_path = os.path.join(CODEBASE_DIR, "generate_templates.py")
    result = subprocess.run([sys.executable, t2_path], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"   Template Generator failed with code {result.returncode}")
    print("\n✅ Template Generator complete.")

    # ── STEP 4: Timing Optimizer ─────────────────────────────────────────────
    step_banner(4, "Timing Optimizer — Notification Timing")
    from timing_optimizer import run_timing_optimizer
    run_timing_optimizer(behavioral_path=data_path)
    print("\n✅ Timing Optimizer complete.")

    # ── STEP 5: Schedule Generator (Iteration 0) ─────────────────────────────
    step_banner(5, "Schedule Generator — User Notification Schedules (Iter 0)")
    sched_path = os.path.join(CODEBASE_DIR, "schedule_generator.py")
    result = subprocess.run([sys.executable, sched_path], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"   Schedule Generator failed with code {result.returncode}")
    print("\n✅ Schedule Generator (Iter 0) complete.")

    # ── Copy iter0 files to iter1 before Task 3 ─────────────────────────────
    copy_iter0_to_iter1()

    # ── STEP 6: Task 3 — RL + iter1 templates + iter1 schedule + delta ──────
    step_banner(6, "Task 3 — RL Learning + Iter1 Generation + Delta Report")

    if not os.path.exists("experiment_results.csv"):
        print("   ⚠️  No experiment_results.csv found.")
        print("   The script will prompt you for the path.")

    t3_path = os.path.join(CODEBASE_DIR, "task3_learning_engine.py")
    result = subprocess.run([sys.executable, t3_path], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"   Task 3 failed with code {result.returncode}")
    else:
        print("\n✅ Task 3 complete.")

    # ── DONE ─────────────────────────────────────────────────────────────────
    elapsed = time.time() - pipeline_start
    mins, secs = divmod(int(elapsed), 60)
    print(f"\n{'='*70}")    
    print(f"  PIPELINE COMPLETE — {mins}m {secs}s")
    print(f"{'='*70}")

    for d in [ITER0_DIR, ITER1_DIR]:
        if os.path.exists(d):
            files = sorted(os.listdir(d))
            print(f"\n  {d}/")
            for f in files:
                size = os.path.getsize(os.path.join(d, f))
                print(f"    {f:<45} {size:>10,} bytes")
    for f in ["experiment_results.csv", "learning_delta_report.csv", "README.txt"]:
        if os.path.exists(f):
            print(f"  {f:<47} {os.path.getsize(f):>10,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Aurora — Full Pipeline")
    parser.add_argument("--data", default=None, help="Path to user_behavioral_data.csv")
    parser.add_argument("--kb", default=None, help="Path to company_kb.md")
    args = parser.parse_args()
    run_full_pipeline(data_path=args.data, kb_path=args.kb)
