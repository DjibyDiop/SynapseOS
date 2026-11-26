#!/usr/bin/env python3
"""
Seed SynapseOS Cortex Knowledge Base with:
1. Atom & Molecule Quantum Physics (Lab 8)
2. Multidisciplinary Learning Games Hub (6 Games & 105 Curriculum Questions)
"""

import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "cortex", "knowledge", "cortex_kb.sqlite")

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if entries already exist
    existing = {row[0] for row in cur.execute("SELECT slug FROM ai_fts").fetchall()}

    entries = [
        (
            "atom_molecule_quantum_physics",
            "Quantum & Chemical Dynamics",
            "atom physics molecules covalent ionic chemical bonds quantum electron shells bohr rutherford protons neutrons coulomb",
            "⚛️ Atom & Molecule Physics (Quantum & Chemical Dynamics Lab)",
            "A fast 2D physics simulation of Rutherford-Bohr atomic shells and chemical bonds. Electrons orbit in quantized energy levels (K, L, M shells) around a nucleus of packed protons and neutrons. Atoms attract and repel via Coulomb electrostatic forces and Lennard-Jones core repulsion to form stable molecules like H2O, CO2, CH4, and NaCl.",
            "Electrostatic Coulomb force: F = (k * q1 * q2) / r^2. Repulsive Pauli exclusion potential: V(r) = 4 * epsilon * (sigma/r)^12. Orbital angular momentum quantization: L = n * h_bar. Bond energy release: Delta E < 0 indicates exothermic stable molecular formation.",
            json.dumps({
                "temperature_k": 298.0,
                "coulomb_factor": 1.0,
                "bond_threshold": 70.0,
                "electron_speed": 1.2,
                "pop_atoms": 6,
                "target_molecule": 0
            }),
            "from workbench.labs.atom_physics import AtomPhysicsLab\nlab = AtomPhysicsLab()\nlab.update_param('temperature_k', 320.0)\nstats = lab.fast_forward_generations(10)\nprint('Synthesized molecules:', stats['molecules_formed'])",
            "If atoms bounce away without bonding, lower temperature_k or increase bond_threshold. For ionic bonds like NaCl, ensure Coulomb factor is at least 1.0."
        ),
        (
            "multidisciplinary_learning_games_hub",
            "K-12 Gamified EdTech",
            "learning games math quest word voyage geo explorer time traveler science explorer adventure odyssey bilingual curriculum",
            "🎮 Multidisciplinary Learning Games Hub (6 Educational Games)",
            "A distraction-free, 100% offline educational game suite covering 5 core disciplines (Math Quest, Word Voyage, Geo Explorer, Time Traveler, Science Explorer) plus a 5-chamber RPG dungeon quest (Adventure Odyssey). Features 105 curriculum-aligned bilingual questions (EN/FR) with instant Socratic hints and combo streak multipliers.",
            "Pedagogical spacing & mastery tracking: Accuracy = (Total Correct / Total Answered) * 100%. Score formula: Points = 100 + (Combo - 1) * 25. Micro-pathing adapts challenge level based on consecutive failure / success streaks via Lumi tutor.",
            json.dumps({
                "disciplines": 5,
                "total_questions": 105,
                "questions_per_subject": 21,
                "bilingual": True,
                "languages": ["en", "fr"],
                "gamification": ["combos", "stars", "badges", "coins", "dungeon_gems"]
            }),
            "from workbench.learning_games import LearningGamesEngine\nengine = LearningGamesEngine(lang='en')\nengine.select_game('math')\nq = engine.get_current_question()\nres = engine.submit_answer(q['correct_idx'])\nprint('Correct:', res['is_correct'], 'Points:', res['points_earned'])",
            "Use engine.get_summary_metrics() to inspect student progress. Progress automatically syncs to LearningPackManager and student_profile.json on every answer."
        )
    ]

    added = 0
    for entry in entries:
        slug = entry[0]
        if slug in existing:
            print(f"Slug already exists: {slug}")
            continue

        cur.execute("""
            INSERT INTO ai_fts (slug, paradigm, keywords, title, layman_guide, math_and_theory, hyperparameters_json, code_template, debugging_tips)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, entry)
        added += 1
        print(f"Added to ai_fts: {slug}")

    conn.commit()
    conn.close()
    print(f"Done! Seeded {added} new knowledge entries into cortex_kb.sqlite.")

if __name__ == "__main__":
    seed()
