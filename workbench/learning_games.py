"""
SynapseOS Learning Games Engine (Jeux Apprenants Multidisciplinaires)
=====================================================================
Interactive, curriculum-aligned educational learning games:
  1. 📐 Math Quest      — Mental math, geometry, fractions & logic puzzles
  2. 🔤 Word Voyage     — Spelling, grammar, vocabulary & bilingual wordplay
  3. 🌍 Geo Explorer    — Continents, oceans, capitals, flags & compass navigation
  4. ⏳ Time Traveler   — Historical timelines, civilisations & science breakthroughs
  5. 🗺️ Adventure Quest — Multi-subject RPG quest unlocking chambers with knowledge

Designed for 100% offline, potato-grade laptops (2007-2017) with zero external deps.
Full bilingual support (English / French) with instant Socratic feedback.
"""

import math
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ===========================================================================
# 1. CURRICULUM QUESTION BANKS (BILINGUAL EN/FR)
# ===========================================================================

MATH_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "m1",
        "category": "Arithmetic",
        "grade_level": "Elementary",
        "question_en": "What is 7 × 8?",
        "question_fr": "Combien fait 7 × 8 ?",
        "options": ["54", "56", "64", "48"],
        "correct_idx": 1,
        "explanation_en": "7 groups of 8 equals 56 (or 8 × 7 = 56).",
        "explanation_fr": "7 groupes de 8 font 56 (7 × 8 = 56).",
    },
    {
        "id": "m2",
        "category": "Geometry",
        "grade_level": "Elementary",
        "question_en": "How many degrees are in the angles of a triangle combined?",
        "question_fr": "Combien de degrés mesure la somme des angles d'un triangle ?",
        "options": ["90°", "180°", "270°", "360°"],
        "correct_idx": 1,
        "explanation_en": "The sum of the three interior angles of any planar triangle is always 180°.",
        "explanation_fr": "La somme des trois angles intérieurs de tout triangle plan est toujours égale à 180°.",
    },
    {
        "id": "m3",
        "category": "Fractions",
        "grade_level": "Middle School",
        "question_en": "What is 1/2 + 1/4?",
        "question_fr": "Combien fait 1/2 + 1/4 ?",
        "options": ["2/6", "3/4", "1/8", "2/4"],
        "correct_idx": 1,
        "explanation_en": "Convert 1/2 to 2/4. Then 2/4 + 1/4 = 3/4.",
        "explanation_fr": "Convertis 1/2 en 2/4. Ensuite 2/4 + 1/4 = 3/4.",
    },
    {
        "id": "m4",
        "category": "Algebra",
        "grade_level": "Middle School",
        "question_en": "Solve for x: 3x + 6 = 21",
        "question_fr": "Résous pour x : 3x + 6 = 21",
        "options": ["x = 3", "x = 5", "x = 7", "x = 15"],
        "correct_idx": 1,
        "explanation_en": "Subtract 6 from both sides: 3x = 15. Divide by 3: x = 5.",
        "explanation_fr": "Soustrais 6 des deux côtés : 3x = 15. Divise par 3 : x = 5.",
    },
    {
        "id": "m5",
        "category": "Logic",
        "grade_level": "Elementary",
        "question_en": "Which number comes next in the sequence: 2, 4, 8, 16, ...?",
        "question_fr": "Quel nombre vient ensuite dans la suite : 2, 4, 8, 16, ... ?",
        "options": ["24", "30", "32", "64"],
        "correct_idx": 2,
        "explanation_en": "Each number doubles (multiplied by 2). 16 × 2 = 32.",
        "explanation_fr": "Chaque nombre est multiplié par 2 (double). 16 × 2 = 32.",
    },
]

LANGUAGE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "l1",
        "category": "Vocabulary",
        "grade_level": "Elementary",
        "question_en": "What is the synonym of 'rapid'?",
        "question_fr": "Quel est le synonyme de 'rapide' ?",
        "options": ["Slow", "Swift", "Heavy", "Quiet"],
        "correct_idx": 1,
        "explanation_en": "'Swift' means moving or capable of moving with great speed.",
        "explanation_fr": "'Véloce' ou 'prompt' signifie qui se déplace à grande vitesse.",
    },
    {
        "id": "l2",
        "category": "Grammar",
        "grade_level": "Elementary",
        "question_en": "Identify the noun in: 'The brave astronaut explored Mars.'",
        "question_fr": "Identifie le nom commun dans : 'Le brave astronaute explore Mars.'",
        "options": ["Brave", "Explored", "Astronaut", "The"],
        "correct_idx": 2,
        "explanation_en": "'Astronaut' is the noun (person). 'Brave' is an adjective.",
        "explanation_fr": "'Astronaute' est un nom commun désignant une personne.",
    },
    {
        "id": "l3",
        "category": "Spelling & Roots",
        "grade_level": "Middle School",
        "question_en": "What does the Latin root 'tele' mean (as in telephone, telescope)?",
        "question_fr": "Que signifie la racine grecque 'télé' (comme dans téléphone, télescope) ?",
        "options": ["Sound", "Distant / Far", "Light", "Fast"],
        "correct_idx": 1,
        "explanation_en": "'Tele' means distant or far off (Greek: tēle).",
        "explanation_fr": "'Télé' signifie loin ou à distance (ex: voir au loin, entendre de loin).",
    },
    {
        "id": "l4",
        "category": "Bilingual / French",
        "grade_level": "Elementary",
        "question_en": "How do you say 'Thank you very much' in French?",
        "question_fr": "Comment dit-on 'Thank you very much' en français ?",
        "options": ["Bonjour", "Merci beaucoup", "Au revoir", "S'il vous plaît"],
        "correct_idx": 1,
        "explanation_en": "'Merci beaucoup' translates directly to 'Thank you very much'.",
        "explanation_fr": "'Merci beaucoup' est la formule de politesse pour remercier chaleureusement.",
    },
]

GEOGRAPHY_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "g1",
        "category": "Continents",
        "grade_level": "Elementary",
        "question_en": "Which is the largest continent on Earth by land area?",
        "question_fr": "Quel est le plus grand continent de la Terre par sa superficie ?",
        "options": ["Africa", "Asia", "North America", "Europe"],
        "correct_idx": 1,
        "explanation_en": "Asia covers about 30% of Earth's total land area and is the most populous.",
        "explanation_fr": "L'Asie couvre environ 30 % des terres émergées de la Terre et est le plus peuplé.",
    },
    {
        "id": "g2",
        "category": "Oceans & Relief",
        "grade_level": "Elementary",
        "question_en": "What is the deepest trench in the world's oceans?",
        "question_fr": "Quelle est la fosse la plus profonde de tous les océans ?",
        "options": ["Java Trench", "Mariana Trench", "Puerto Rico Trench", "Romanche Trench"],
        "correct_idx": 1,
        "explanation_en": "The Mariana Trench reaches a depth of about 10,994 meters in the Pacific.",
        "explanation_fr": "La fosse des Mariannes atteint près de 11 000 mètres de profondeur dans l'océan Pacifique.",
    },
    {
        "id": "g3",
        "category": "Capitals",
        "grade_level": "Middle School",
        "question_en": "What is the capital city of Japan?",
        "question_fr": "Quelle est la capitale du Japon ?",
        "options": ["Kyoto", "Tokyo", "Osaka", "Nagoya"],
        "correct_idx": 1,
        "explanation_en": "Tokyo has been the capital and seat of government of Japan since 1868.",
        "explanation_fr": "Tokyo est la capitale officielle et le siège du gouvernement du Japon depuis 1868.",
    },
    {
        "id": "g4",
        "category": "Compass & Navigation",
        "grade_level": "Elementary",
        "question_en": "If you are facing North, which direction is immediately to your right?",
        "question_fr": "Si tu fais face au Nord, quelle direction se trouve directement à ta droite ?",
        "options": ["West", "East", "South", "South-East"],
        "correct_idx": 1,
        "explanation_en": "Clockwise on a compass rose: North -> East -> South -> West.",
        "explanation_fr": "Dans le sens des aiguilles d'une montre : Nord -> Est -> Sud -> Ouest. L'Est est à droite.",
    },
]

HISTORY_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "h1",
        "category": "Ancient Civilisations",
        "grade_level": "Elementary",
        "question_en": "Which ancient civilisation built the Pyramids of Giza along the Nile River?",
        "question_fr": "Quelle civilisation antique a bâti les pyramides de Gizeh au bord du Nil ?",
        "options": ["Ancient Rome", "Ancient Egypt", "Mesopotamia", "Ancient Greece"],
        "correct_idx": 1,
        "explanation_en": "Ancient Egyptians constructed the monumental pyramids as royal tombs over 4,500 years ago.",
        "explanation_fr": "Les Égyptiens de l'Antiquité ont érigé ces monuments il y a plus de 4 500 ans.",
    },
    {
        "id": "h2",
        "category": "Science Discoveries",
        "grade_level": "Middle School",
        "question_en": "Which scientist discovered the principles of universal gravitation after observing falling apples?",
        "question_fr": "Quel savant a formulé la loi de la gravitation universelle au XVIIe siècle ?",
        "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Marie Curie"],
        "correct_idx": 1,
        "explanation_en": "Sir Isaac Newton published the laws of motion and gravitation in 1687 (Principia).",
        "explanation_fr": "Isaac Newton a publié les lois du mouvement et de la gravitation en 1687.",
    },
    {
        "id": "h3",
        "category": "Space Exploration",
        "grade_level": "Elementary",
        "question_en": "In what year did humans first land and walk on the Moon (Apollo 11)?",
        "question_fr": "En quelle année le premier être humain a-t-il posé le pied sur la Lune (Apollo 11) ?",
        "options": ["1959", "1969", "1975", "1981"],
        "correct_idx": 1,
        "explanation_en": "Neil Armstrong and Buzz Aldrin stepped onto the lunar surface on July 20, 1969.",
        "explanation_fr": "Neil Armstrong et Buzz Aldrin ont marché sur la Lune le 20 juillet 1969.",
    },
    {
        "id": "h4",
        "category": "Inventions",
        "grade_level": "Elementary",
        "question_en": "Who invented the movable-type printing press in Europe around 1440?",
        "question_fr": "Qui a inventé l'imprimerie à caractères mobiles en Europe vers 1440 ?",
        "options": ["Leonardo da Vinci", "Johannes Gutenberg", "Alexander Bell", "Thomas Edison"],
        "correct_idx": 1,
        "explanation_en": "Johannes Gutenberg mechanized the movable metal-type printing press, revolutionising education.",
        "explanation_fr": "Johannes Gutenberg a inventé l'imprimerie moderne, permettant de diffuser le savoir à tous.",
    },
]


# ===========================================================================
# 2. LEARNING GAMES ENGINE & STATE MANAGER
# ===========================================================================

class LearningGamesEngine:
    """
    Manages active state for all 5 educational games:
    - Math Quest
    - Word Voyage
    - Geo Explorer
    - Time Traveler
    - Adventure Odyssey (multi-subject RPG dungeon)
    """

    GAMES = {
        "math": {"title_en": "📐 Math Quest", "title_fr": "📐 Quête Mathématique", "bank": MATH_QUESTIONS},
        "language": {"title_en": "🔤 Word Voyage", "title_fr": "🔤 Voyage des Mots", "bank": LANGUAGE_QUESTIONS},
        "geography": {"title_en": "🌍 Geo Explorer", "title_fr": "🌍 Géo Explorateur", "bank": GEOGRAPHY_QUESTIONS},
        "history": {"title_en": "⏳ Time Traveler", "title_fr": "⏳ Voyageur du Temps", "bank": HISTORY_QUESTIONS},
        "adventure": {"title_en": "🗺️ Adventure Odyssey", "title_fr": "🗺️ L'Odyssée Apprenante", "bank": []},
    }

    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.active_game_id: str = "math"
        self.current_q_idx: int = 0
        self.score: int = 0
        self.combo_streak: int = 0
        self.best_streak: int = 0
        self.total_answered: int = 0
        self.total_correct: int = 0
        self.last_result: Optional[Dict[str, Any]] = None

        # Adventure Odyssey State
        self.dungeon_room: int = 1
        self.dungeon_gems: int = 0
        self.dungeon_max_rooms: int = 5
        self.dungeon_completed: bool = False

    def select_game(self, game_id: str) -> bool:
        if game_id in self.GAMES:
            self.active_game_id = game_id
            self.current_q_idx = 0
            self.last_result = None
            if game_id == "adventure":
                self.dungeon_room = 1
                self.dungeon_gems = 0
                self.dungeon_completed = False
            return True
        return False

    def get_current_question(self) -> Dict[str, Any]:
        """Returns the current active question for the selected game."""
        if self.active_game_id == "adventure":
            # Round-robin through Math -> Lang -> Geo -> History
            subject_banks = [MATH_QUESTIONS, LANGUAGE_QUESTIONS, GEOGRAPHY_QUESTIONS, HISTORY_QUESTIONS]
            bank = subject_banks[(self.dungeon_room - 1) % len(subject_banks)]
            q = bank[(self.current_q_idx) % len(bank)]
            return {
                **q,
                "room_num": self.dungeon_room,
                "max_rooms": self.dungeon_max_rooms,
                "gems": self.dungeon_gems,
            }

        bank = self.GAMES[self.active_game_id]["bank"]
        if not bank:
            bank = MATH_QUESTIONS
        return bank[self.current_q_idx % len(bank)]

    def submit_answer(self, chosen_idx: int) -> Dict[str, Any]:
        """
        Submits answer index (0..3). Returns grading outcome, score update, and explanation.
        """
        q = self.get_current_question()
        is_correct = (chosen_idx == q["correct_idx"])
        self.total_answered += 1

        points_earned = 0
        if is_correct:
            self.combo_streak += 1
            if self.combo_streak > self.best_streak:
                self.best_streak = self.combo_streak
            self.total_correct += 1
            # Base 100 pts + combo multiplier
            points_earned = 100 + (self.combo_streak - 1) * 25
            self.score += points_earned

            if self.active_game_id == "adventure":
                self.dungeon_gems += 1
                if self.dungeon_room < self.dungeon_max_rooms:
                    self.dungeon_room += 1
                else:
                    self.dungeon_completed = True
        else:
            self.combo_streak = 0

        explanation = q["explanation_fr"] if self.lang == "fr" else q["explanation_en"]
        res = {
            "is_correct": is_correct,
            "chosen_idx": chosen_idx,
            "correct_idx": q["correct_idx"],
            "points_earned": points_earned,
            "total_score": self.score,
            "combo_streak": self.combo_streak,
            "explanation": explanation,
            "timestamp": time.time(),
        }
        self.last_result = res
        return res

    def next_question(self) -> Dict[str, Any]:
        """Advances to the next question in the pool."""
        self.current_q_idx += 1
        self.last_result = None
        return self.get_current_question()

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Returns overall learning game stats for the student profile and report card."""
        accuracy = (self.total_correct / self.total_answered * 100.0) if self.total_answered > 0 else 0.0
        return {
            "score": self.score,
            "total_answered": self.total_answered,
            "total_correct": self.total_correct,
            "accuracy_pct": round(accuracy, 1),
            "best_streak": self.best_streak,
            "dungeon_gems": self.dungeon_gems,
            "dungeon_completed": self.dungeon_completed,
        }


# ===========================================================================
# 3. INTERACTIVE GTK3 LEARNING GAMES DIALOG (CLEAN, AIRY & CHILD-FRIENDLY)
# ===========================================================================

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib
    GTK_AVAILABLE = True
except Exception:
    GTK_AVAILABLE = False
    Gtk = None  # type: ignore[assignment]
    GLib = None  # type: ignore[assignment]


class LearningGamesDialog:
    """
    Child-friendly, distraction-free educational games workstation:
    - 5 learning game tabs (Math, Language, Geography, History, Adventure Quest)
    - Big clickable answer cards with instant Socratic feedback
    - Combo streak multipliers and Star points
    """

    def __init__(self, parent_window=None, lang: str = "en"):
        self.engine = LearningGamesEngine(lang=lang)
        self.lang = lang
        if not GTK_AVAILABLE:
            self.dialog = None
            return

        self.dialog = Gtk.Dialog(
            title="🎮 Synapse Learning Games Hub",
            transient_for=parent_window,
            flags=0,
        )
        self.dialog.set_default_size(780, 520)
        self.dialog.set_resizable(True)
        self.dialog.add_button("Fermer / Close", Gtk.ResponseType.CLOSE)

        content = self.dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(12)
        content.set_margin_end(12)

        # Header Selector Row
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        content.pack_start(top_bar, False, False, 0)

        self.game_buttons: Dict[str, Gtk.Button] = {}
        for gid, ginfo in self.engine.GAMES.items():
            title = ginfo["title_fr"] if self.lang == "fr" else ginfo["title_en"]
            btn = Gtk.Button(label=title)
            btn.connect("clicked", lambda _b, g=gid: self._on_select_game(g))
            top_bar.pack_start(btn, True, True, 0)
            self.game_buttons[gid] = btn

        # Score & Combo Banner
        self.score_lbl = Gtk.Label()
        self.score_lbl.set_markup("<b>Score : 0 pts</b> | Combo : 0 🔥")
        top_bar.pack_start(self.score_lbl, False, False, 8)

        # Main Question Card Frame
        self.card_frame = Gtk.Frame()
        self.card_frame.set_margin_top(10)
        content.pack_start(self.card_frame, True, True, 0)

        card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card_box.set_margin_top(12)
        card_box.set_margin_bottom(12)
        card_box.set_margin_start(16)
        card_box.set_margin_end(16)
        self.card_frame.add(card_box)

        # Question Title & Text
        self.q_cat_lbl = Gtk.Label()
        self.q_cat_lbl.set_xalign(0.0)
        card_box.pack_start(self.q_cat_lbl, False, False, 0)

        self.q_text_lbl = Gtk.Label()
        self.q_text_lbl.set_xalign(0.0)
        self.q_text_lbl.set_line_wrap(True)
        card_box.pack_start(self.q_text_lbl, False, False, 6)

        # 4 Option Buttons (Grid 2x2)
        self.option_grid = Gtk.Grid()
        self.option_grid.set_column_spacing(10)
        self.option_grid.set_row_spacing(10)
        self.option_grid.set_column_homogeneous(True)
        card_box.pack_start(self.option_grid, True, True, 4)

        self.option_buttons: List[Gtk.Button] = []
        for i in range(4):
            btn = Gtk.Button(label=f"Option {i+1}")
            btn.connect("clicked", lambda _b, idx=i: self._on_answer_clicked(idx))
            self.option_buttons.append(btn)
            row = i // 2
            col = i % 2
            self.option_grid.attach(btn, col, row, 1, 1)

        # Feedback & Explanation Label
        self.feedback_lbl = Gtk.Label()
        self.feedback_lbl.set_xalign(0.0)
        self.feedback_lbl.set_line_wrap(True)
        card_box.pack_start(self.feedback_lbl, False, False, 4)

        # Next Button Row
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        card_box.pack_start(bottom_row, False, False, 0)

        self.btn_next = Gtk.Button(label="Suivant / Next ➔")
        self.btn_next.set_sensitive(False)
        self.btn_next.connect("clicked", lambda _b: self._on_next_clicked())
        bottom_row.pack_end(self.btn_next, False, False, 0)

        self._render_question()
        self.dialog.show_all()

    def _on_select_game(self, game_id: str):
        self.engine.select_game(game_id)
        self.btn_next.set_sensitive(False)
        self.feedback_lbl.set_text("")
        self._render_question()

    def _render_question(self):
        q = self.engine.get_current_question()
        cat = q.get("category", "General")
        level = q.get("grade_level", "Elementary")
        q_text = q.get("question_fr" if self.lang == "fr" else "question_en", "")

        room_info = ""
        if "room_num" in q:
            room_info = f" · Salle {q['room_num']}/{q['max_rooms']} 💎 {q['gems']} gemmes"

        self.card_frame.set_label(f" {self.engine.GAMES[self.engine.active_game_id]['title_en']} ")
        self.q_cat_lbl.set_markup(f"<b><span foreground='#38bdf8'>★ {cat}</span></b> ({level}){room_info}")
        self.q_text_lbl.set_markup(f"<span size='large' weight='bold'>{q_text}</span>")

        options = q.get("options", ["A", "B", "C", "D"])
        for i, btn in enumerate(self.option_buttons):
            btn.set_sensitive(True)
            if i < len(options):
                btn.set_label(options[i])
                btn.show()
            else:
                btn.hide()

        self.score_lbl.set_markup(
            f"<b>Score : {self.engine.score} pts</b> | Combo : {self.engine.combo_streak} 🔥"
        )

    def _on_answer_clicked(self, chosen_idx: int):
        res = self.engine.submit_answer(chosen_idx)
        for btn in self.option_buttons:
            btn.set_sensitive(False)

        if res["is_correct"]:
            self.feedback_lbl.set_markup(
                f"<b><span foreground='#22c55e'>✓ Bravo ! (+{res['points_earned']} pts)</span></b>\n{res['explanation']}"
            )
        else:
            self.feedback_lbl.set_markup(
                f"<b><span foreground='#ef4444'>✗ Pas tout à fait...</span></b>\n{res['explanation']}"
            )

        self.score_lbl.set_markup(
            f"<b>Score : {self.engine.score} pts</b> | Combo : {self.engine.combo_streak} 🔥"
        )
        self.btn_next.set_sensitive(True)

    def _on_next_clicked(self):
        self.engine.next_question()
        self.btn_next.set_sensitive(False)
        self.feedback_lbl.set_text("")
        self._render_question()

    def show(self):
        if not GTK_AVAILABLE or not self.dialog:
            return
        self.dialog.run()
        self.dialog.destroy()

