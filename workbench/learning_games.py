"""
SynapseOS Learning Games Engine (Jeux Apprenants Multidisciplinaires)
=====================================================================
Interactive, curriculum-aligned educational learning games:
  1. 📐 Math Quest      — Mental math, geometry, fractions & logic puzzles (21 questions)
  2. 🔤 Word Voyage     — Spelling, grammar, vocabulary & bilingual roots (21 questions)
  3. 🌍 Geo Explorer    — Continents, oceans, capitals, flags & cartography (21 questions)
  4. ⏳ Time Traveler   — Historical timelines, civilisations & inventions (21 questions)
  5. 🔬 Science Explorer — Physics, chemistry, biology & astronomy (21 questions)
  6. 🗺️ Adventure Odyssey — Multi-subject RPG quest unlocking chambers across all 5 fields

Designed for 100% offline, potato-grade laptops (2007-2017) with zero external deps.
Full bilingual support (English / French) with instant Socratic feedback.
Integrated with student profile progress tracking (student_profile.json) & Lumi.
"""

import math
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ===========================================================================
# 1. CURRICULUM QUESTION BANKS (BILINGUAL EN/FR — 21 QUESTIONS PER SUBJECT)
# ===========================================================================

MATH_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "m01",
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
        "id": "m02",
        "category": "Geometry",
        "grade_level": "Elementary",
        "question_en": "How many degrees are in the interior angles of a triangle combined?",
        "question_fr": "Combien de degrés mesure la somme des angles intérieurs d'un triangle ?",
        "options": ["90°", "180°", "270°", "360°"],
        "correct_idx": 1,
        "explanation_en": "The sum of the three interior angles of any Euclidean planar triangle is always 180°.",
        "explanation_fr": "La somme des trois angles intérieurs de tout triangle euclidien est toujours égale à 180°.",
    },
    {
        "id": "m03",
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
        "id": "m04",
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
        "id": "m05",
        "category": "Logic & Sequences",
        "grade_level": "Elementary",
        "question_en": "Which number comes next in the sequence: 2, 4, 8, 16, ...?",
        "question_fr": "Quel nombre vient ensuite dans la suite : 2, 4, 8, 16, ... ?",
        "options": ["24", "30", "32", "64"],
        "correct_idx": 2,
        "explanation_en": "Each number doubles (multiplied by 2). 16 × 2 = 32.",
        "explanation_fr": "Chaque nombre est multiplié par 2 (double). 16 × 2 = 32.",
    },
    {
        "id": "m06",
        "category": "Number Theory",
        "grade_level": "Middle School",
        "question_en": "Which of the following numbers is a prime number?",
        "question_fr": "Lequel des nombres suivants est un nombre premier ?",
        "options": ["21", "27", "29", "35"],
        "correct_idx": 2,
        "explanation_en": "29 has only two divisors: 1 and 29. 21=3×7, 27=3×9, 35=5×7.",
        "explanation_fr": "29 n'a que deux diviseurs : 1 et lui-même. 21=3×7, 27=3×9, 35=5×7.",
    },
    {
        "id": "m07",
        "category": "Geometry",
        "grade_level": "Elementary",
        "question_en": "What is the area of a rectangle with length 9 m and width 6 m?",
        "question_fr": "Quelle est l'aire d'un rectangle de longueur 9 m et de largeur 6 m ?",
        "options": ["30 m²", "54 m²", "45 m²", "60 m²"],
        "correct_idx": 1,
        "explanation_en": "Area = length × width = 9 × 6 = 54 m².",
        "explanation_fr": "Aire = longueur × largeur = 9 × 6 = 54 m².",
    },
    {
        "id": "m08",
        "category": "Percentages",
        "grade_level": "Middle School",
        "question_en": "What is 25% of 80?",
        "question_fr": "Combien font 25 % de 80 ?",
        "options": ["15", "20", "25", "30"],
        "correct_idx": 1,
        "explanation_en": "25% is equal to 1/4. 80 ÷ 4 = 20.",
        "explanation_fr": "25 % correspond au quart (1/4). 80 ÷ 4 = 20.",
    },
    {
        "id": "m09",
        "category": "Roots & Powers",
        "grade_level": "Middle School",
        "question_en": "What is the square root of 144 (√144)?",
        "question_fr": "Quelle est la racine carrée de 144 (√144) ?",
        "options": ["11", "12", "14", "16"],
        "correct_idx": 1,
        "explanation_en": "12 × 12 = 144, so √144 = 12.",
        "explanation_fr": "12 × 12 = 144, donc √144 = 12.",
    },
    {
        "id": "m10",
        "category": "Geometry",
        "grade_level": "Middle School",
        "question_en": "In a right triangle with legs a = 3 and b = 4, what is the hypotenuse c?",
        "question_fr": "Dans un triangle rectangle avec les côtés a = 3 et b = 4, quelle est l'hypoténuse c ?",
        "options": ["5", "6", "7", "8"],
        "correct_idx": 0,
        "explanation_en": "By Pythagorean theorem: c² = 3² + 4² = 9 + 16 = 25. c = √25 = 5.",
        "explanation_fr": "Par Pythagore : c² = 3² + 4² = 9 + 16 = 25. c = √25 = 5.",
    },
    {
        "id": "m11",
        "category": "Geometry",
        "grade_level": "High School",
        "question_en": "Which formula gives the circumference of a circle with radius r?",
        "question_fr": "Quelle formule donne la circonférence d'un cercle de rayon r ?",
        "options": ["πr²", "2πr", "4/3 πr³", "2r²"],
        "correct_idx": 1,
        "explanation_en": "The circumference of a circle is 2 × π × r (or π × diameter).",
        "explanation_fr": "Le périmètre (circonférence) d'un cercle vaut 2 × π × r.",
    },
    {
        "id": "m12",
        "category": "Probability",
        "grade_level": "Middle School",
        "question_en": "What is the probability of rolling an even number on a fair 6-sided die?",
        "question_fr": "Quelle est la probabilité d'obtenir un nombre pair sur un dé équilibré à 6 faces ?",
        "options": ["1/6", "1/3", "1/2", "2/3"],
        "correct_idx": 2,
        "explanation_en": "Even numbers on a 6-sided die are 2, 4, 6 (3 outcomes out of 6) = 3/6 = 1/2.",
        "explanation_fr": "Les nombres pairs sont 2, 4, 6 (3 issues sur 6) = 3/6 = 1/2 (50 %).",
    },
    {
        "id": "m13",
        "category": "Integers",
        "grade_level": "Elementary",
        "question_en": "What is the result of -15 + (-7)?",
        "question_fr": "Quel est le résultat de -15 + (-7) ?",
        "options": ["-8", "-22", "22", "8"],
        "correct_idx": 1,
        "explanation_en": "Adding two negative numbers gives a negative sum: -15 - 7 = -22.",
        "explanation_fr": "L'addition de deux nombres négatifs s'additionne en valeur absolue : -15 - 7 = -22.",
    },
    {
        "id": "m14",
        "category": "Powers",
        "grade_level": "Middle School",
        "question_en": "What is the value of 2⁵ (2 to the power of 5)?",
        "question_fr": "Quelle est la valeur de 2⁵ (2 puissance 5) ?",
        "options": ["10", "25", "32", "64"],
        "correct_idx": 2,
        "explanation_en": "2 × 2 × 2 × 2 × 2 = 32.",
        "explanation_fr": "2 × 2 × 2 × 2 × 2 = 32.",
    },
    {
        "id": "m15",
        "category": "Ratios",
        "grade_level": "Middle School",
        "question_en": "If 12 apples are split between Leo and Mia in a 1:2 ratio, how many does Mia receive?",
        "question_fr": "Si 12 pommes sont partagées entre Léo et Mia dans un ratio 1:2, combien en reçoit Mia ?",
        "options": ["4", "6", "8", "9"],
        "correct_idx": 2,
        "explanation_en": "Total parts = 1 + 2 = 3. One part = 12 ÷ 3 = 4. Mia gets 2 parts = 2 × 4 = 8.",
        "explanation_fr": "Nombre total de parts = 1 + 2 = 3. Une part = 12 ÷ 3 = 4. Mia reçoit 2 parts = 8.",
    },
    {
        "id": "m16",
        "category": "Perimeter",
        "grade_level": "Elementary",
        "question_en": "What is the perimeter of an equilateral triangle with side length 7 cm?",
        "question_fr": "Quel est le périmètre d'un triangle équilatéral de côté 7 cm ?",
        "options": ["14 cm", "21 cm", "28 cm", "49 cm"],
        "correct_idx": 1,
        "explanation_en": "An equilateral triangle has 3 equal sides: 3 × 7 = 21 cm.",
        "explanation_fr": "Un triangle équilatéral possède 3 côtés égaux : 3 × 7 cm = 21 cm.",
    },
    {
        "id": "m17",
        "category": "Statistics",
        "grade_level": "Middle School",
        "question_en": "What is the median of the numbers [3, 7, 9, 15, 21]?",
        "question_fr": "Quelle est la médiane de la série [3, 7, 9, 15, 21] ?",
        "options": ["7", "9", "11", "15"],
        "correct_idx": 1,
        "explanation_en": "In the ordered set of 5 numbers, the middle (3rd) value is 9.",
        "explanation_fr": "Dans cette série ordonnée de 5 valeurs, l'élément central est 9.",
    },
    {
        "id": "m18",
        "category": "Speed & Kinematics",
        "grade_level": "Middle School",
        "question_en": "A train travels 180 km in 3 hours at constant speed. What is its speed?",
        "question_fr": "Un train parcourt 180 km en 3 heures à vitesse constante. Quelle est sa vitesse ?",
        "options": ["50 km/h", "60 km/h", "75 km/h", "90 km/h"],
        "correct_idx": 1,
        "explanation_en": "Speed = Distance ÷ Time = 180 km ÷ 3 h = 60 km/h.",
        "explanation_fr": "Vitesse = Distance ÷ Temps = 180 km ÷ 3 h = 60 km/h.",
    },
    {
        "id": "m19",
        "category": "Combinatorics",
        "grade_level": "High School",
        "question_en": "What is the value of 4! (4 factorial)?",
        "question_fr": "Quelle est la valeur de 4! (factorielle 4) ?",
        "options": ["12", "16", "24", "48"],
        "correct_idx": 2,
        "explanation_en": "4! = 4 × 3 × 2 × 1 = 24.",
        "explanation_fr": "4! = 4 × 3 × 2 × 1 = 24.",
    },
    {
        "id": "m20",
        "category": "Linear Functions",
        "grade_level": "High School",
        "question_en": "What is the slope (m) of the linear equation y = 5x - 7?",
        "question_fr": "Quel est le coefficient directeur (pente m) de la droite y = 5x - 7 ?",
        "options": ["-7", "5", "-5", "7"],
        "correct_idx": 1,
        "explanation_en": "In slope-intercept form y = mx + b, the coefficient of x is the slope m = 5.",
        "explanation_fr": "Dans la forme y = mx + p, le coefficient de x est la pente m = 5.",
    },
    {
        "id": "m21",
        "category": "Geometry",
        "grade_level": "Elementary",
        "question_en": "What is the sum of interior angles of any planar quadrilateral (4-sided polygon)?",
        "question_fr": "Combien mesure la somme des angles intérieurs de tout quadrilatère plan ?",
        "options": ["180°", "270°", "360°", "540°"],
        "correct_idx": 2,
        "explanation_en": "Any quadrilateral can be split into 2 triangles: 2 × 180° = 360°.",
        "explanation_fr": "Tout quadrilatère se découpe en 2 triangles : 2 × 180° = 360°.",
    },
]

LANGUAGE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "l01",
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
        "id": "l02",
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
        "id": "l03",
        "category": "Roots & Prefixes",
        "grade_level": "Middle School",
        "question_en": "What does the Greek root 'tele' mean (as in telephone, telescope)?",
        "question_fr": "Que signifie la racine grecque 'télé' (comme dans téléphone, télescope) ?",
        "options": ["Sound", "Distant / Far", "Light", "Fast"],
        "correct_idx": 1,
        "explanation_en": "'Tele' means distant or far off (Greek: tēle).",
        "explanation_fr": "'Télé' signifie loin ou à distance (ex: voir au loin, entendre de loin).",
    },
    {
        "id": "l04",
        "category": "Bilingual / French",
        "grade_level": "Elementary",
        "question_en": "How do you say 'Thank you very much' in French?",
        "question_fr": "Comment dit-on 'Thank you very much' en français ?",
        "options": ["Bonjour", "Merci beaucoup", "Au revoir", "S'il vous plaît"],
        "correct_idx": 1,
        "explanation_en": "'Merci beaucoup' translates directly to 'Thank you very much'.",
        "explanation_fr": "'Merci beaucoup' est la formule de politesse pour exprimer sa gratitude.",
    },
    {
        "id": "l05",
        "category": "Antonyms",
        "grade_level": "Elementary",
        "question_en": "What is the antonym (opposite) of 'generous'?",
        "question_fr": "Quel est l'antonyme (contraire) de 'généreux' ?",
        "options": ["Kind", "Selfish", "Friendly", "Honest"],
        "correct_idx": 1,
        "explanation_en": "'Selfish' or 'stingy' is the opposite of generous.",
        "explanation_fr": "'Avare' ou 'égoïste' est le contraire de généreux.",
    },
    {
        "id": "l06",
        "category": "Grammar",
        "grade_level": "Elementary",
        "question_en": "Identify the action verb in: 'The blue whale swims silently.'",
        "question_fr": "Identifie le verbe d'action dans : 'La baleine bleue nage en silence.'",
        "options": ["Whale", "Blue", "Swims", "Silently"],
        "correct_idx": 2,
        "explanation_en": "'Swims' (nage) describes the action performed by the subject.",
        "explanation_fr": "'Nage' (swims) est le verbe conjugué exprimant l'action.",
    },
    {
        "id": "l07",
        "category": "Irregular Plurals",
        "grade_level": "Elementary",
        "question_en": "What is the plural form of 'child' in English?",
        "question_fr": "Quelle est la forme plurielle du mot 'child' (enfant) en anglais ?",
        "options": ["Childs", "Children", "Childes", "Childrens"],
        "correct_idx": 1,
        "explanation_en": "'Children' is the irregular plural form of 'child'.",
        "explanation_fr": "'Children' est le pluriel irrégulier de 'child'.",
    },
    {
        "id": "l08",
        "category": "Greek Roots",
        "grade_level": "Middle School",
        "question_en": "What does the root 'bio' mean (as in biology, biography)?",
        "question_fr": "Que signifie la racine grecque 'bio' (dans biologie, biographie) ?",
        "options": ["Earth", "Life", "Book", "Time"],
        "correct_idx": 1,
        "explanation_en": "'Bio' comes from the Greek bios, meaning 'life'.",
        "explanation_fr": "'Bio' provient du grec bios signifiant 'la vie'.",
    },
    {
        "id": "l09",
        "category": "Homophones",
        "grade_level": "Middle School",
        "question_en": "Which word correctly completes: 'The students put ___ backpacks on the rack.'?",
        "question_fr": "Quel mot complète correctement : 'Les élèves ont rangé ___ sacs' en anglais ?",
        "options": ["there", "their", "they're", "thier"],
        "correct_idx": 1,
        "explanation_en": "'Their' is the possessive pronoun indicating ownership.",
        "explanation_fr": "'Their' est le pronom possessif (leur/leurs). 'There' indique le lieu.",
    },
    {
        "id": "l10",
        "category": "Figures of Speech",
        "grade_level": "High School",
        "question_en": "What figure of speech is: 'The wind whispered secrets through the trees'?",
        "question_fr": "Quelle figure de style est : 'Le vent murmurait des secrets entre les arbres' ?",
        "options": ["Metaphor", "Personification", "Hyperbole", "Oxymoron"],
        "correct_idx": 1,
        "explanation_en": "Personification attributes human actions (whispering) to non-human things (the wind).",
        "explanation_fr": "La personnification prête un comportement humain (chuchoter) à un élément naturel.",
    },
    {
        "id": "l11",
        "category": "Verb Tenses",
        "grade_level": "Elementary",
        "question_en": "What is the simple past tense of the irregular verb 'write'?",
        "question_fr": "Quel est le prétérit (passé simple) du verbe irrégulier anglais 'write' ?",
        "options": ["Writed", "Wrote", "Written", "Writing"],
        "correct_idx": 1,
        "explanation_en": "The past forms are: write -> wrote -> written.",
        "explanation_fr": "Les formes sont : write (présent) -> wrote (passé) -> written (participe).",
    },
    {
        "id": "l12",
        "category": "Bilingual / French",
        "grade_level": "Elementary",
        "question_en": "What is the French translation for the word 'Library'?",
        "question_fr": "Quelle est la traduction française correcte de 'Library' ?",
        "options": ["Librairie", "Bibliothèque", "Boutique", "Cahier"],
        "correct_idx": 1,
        "explanation_en": "'Library' is 'Bibliothèque' (place to borrow books). 'Librairie' is a bookstore.",
        "explanation_fr": "'Library' est un faux-ami : il signifie 'Bibliothèque'. 'Librairie' se dit 'bookstore'.",
    },
    {
        "id": "l13",
        "category": "Suffixes",
        "grade_level": "Middle School",
        "question_en": "What does the suffix '-ology' mean (as in geology, zoology)?",
        "question_fr": "Que signifie le suffixe '-logie' (comme dans géologie, zoologie) ?",
        "options": ["Instrument", "Study or science of", "Fear of", "Measurement of"],
        "correct_idx": 1,
        "explanation_en": "'-ology' derives from logos, meaning the study or branch of knowledge.",
        "explanation_fr": "Le suffixe '-logie' désigne l'étude raisonnée ou la science d'un domaine.",
    },
    {
        "id": "l14",
        "category": "Adjectives & Comparison",
        "grade_level": "Elementary",
        "question_en": "What is the superlative form of 'good'?",
        "question_fr": "Quelle est la forme superlative de 'good' en anglais (le meilleur) ?",
        "options": ["Goodest", "Better", "Best", "Most good"],
        "correct_idx": 2,
        "explanation_en": "Good -> Better (comparative) -> Best (superlative).",
        "explanation_fr": "Good -> Better (comparatif) -> Best (superlatif).",
    },
    {
        "id": "l15",
        "category": "Adverbs",
        "grade_level": "Middle School",
        "question_en": "Identify the adverb in: 'The spacecraft descended smoothly.'",
        "question_fr": "Identifie l'adverbe dans : 'La navette est descendue doucement.'",
        "options": ["Spacecraft", "Descended", "Smoothly", "The"],
        "correct_idx": 2,
        "explanation_en": "'Smoothly' describes how the action was performed (modifying the verb).",
        "explanation_fr": "'Doucement' (smoothly) précise la manière dont s'est déroulée l'action.",
    },
    {
        "id": "l16",
        "category": "Etymology",
        "grade_level": "Middle School",
        "question_en": "What dietary habit does the Latin word 'omnivore' describe?",
        "question_fr": "Quel régime alimentaire le terme 'omnivore' (du latin omnis + vorare) désigne-t-il ?",
        "options": ["Eats only plants", "Eats both plants and meat", "Eats only fish", "Eats only insects"],
        "correct_idx": 1,
        "explanation_en": "'Omni' means all/everything, so an omnivore consumes both plant and animal matter.",
        "explanation_fr": "'Omnis' signifiant tout, un omnivore consomme des végétaux et des animaux.",
    },
    {
        "id": "l17",
        "category": "Bilingual / French",
        "grade_level": "Elementary",
        "question_en": "How do you greet someone in French specifically in the evening?",
        "question_fr": "Comment salue-t-on quelqu'un en français spécifiquement le soir ?",
        "options": ["Bonjour", "Bon après-midi", "Bonsoir", "Bonne nuit"],
        "correct_idx": 2,
        "explanation_en": "'Bonsoir' is the standard polite greeting for the evening hours.",
        "explanation_fr": "'Bonsoir' est la salutation d'usage à partir de la fin d'après-midi.",
    },
    {
        "id": "l18",
        "category": "Literary Devices",
        "grade_level": "High School",
        "question_en": "Which literary term describes combining two contradictory terms, like 'deafening silence'?",
        "question_fr": "Quel terme littéraire désigne la juxtaposition de deux mots opposés, comme 'silence assourdissant' ?",
        "options": ["Alliteration", "Oxymoron", "Onomatopoeia", "Euphemism"],
        "correct_idx": 1,
        "explanation_en": "An oxymoron juxtaposes apparently contradictory terms for dramatic effect.",
        "explanation_fr": "L'oxymore réunit deux termes contraires dans une même expression.",
    },
    {
        "id": "l19",
        "category": "Conjunctions",
        "grade_level": "Middle School",
        "question_en": "Identify the coordinating conjunction in: 'We prepared well, yet the storm surprised us.'",
        "question_fr": "Identifie la conjonction dans : 'Nous étions prêts, mais la tempête nous a surpris.'",
        "options": ["Prepared", "Yet", "Storm", "Well"],
        "correct_idx": 1,
        "explanation_en": "'Yet' (ou 'mais') is the coordinating conjunction linking the two clauses.",
        "explanation_fr": "'Yet' / 'mais' est la conjonction reliant les deux propositions.",
    },
    {
        "id": "l20",
        "category": "Synonyms",
        "grade_level": "Elementary",
        "question_en": "Which word is a synonym for 'courageous'?",
        "question_fr": "Quel mot est un synonyme de 'courageux' ?",
        "options": ["Timid", "Valiant", "Cautious", "Hesitant"],
        "correct_idx": 1,
        "explanation_en": "'Valiant' means possessing or showing courage or determination.",
        "explanation_fr": "'Vaillant' ou 'brave' désigne une personne faisant preuve de courage.",
    },
    {
        "id": "l21",
        "category": "Grammar & Pronouns",
        "grade_level": "Elementary",
        "question_en": "Which pronoun correctly replaces 'Alice and Bob' as the subject?",
        "question_fr": "Quel pronom personnel remplace correctement 'Alice et Bob' comme sujet en anglais ?",
        "options": ["He", "She", "They", "Them"],
        "correct_idx": 2,
        "explanation_en": "'They' is the third-person plural subject pronoun.",
        "explanation_fr": "'They' (ils) est le pronom sujet pluriel correspondant.",
    },
]

GEOGRAPHY_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "g01",
        "category": "Continents",
        "grade_level": "Elementary",
        "question_en": "Which is the largest continent on Earth by total land area?",
        "question_fr": "Quel est le plus grand continent de la Terre par sa superficie terrestre ?",
        "options": ["Africa", "Asia", "North America", "Europe"],
        "correct_idx": 1,
        "explanation_en": "Asia covers about 30% of Earth's total land area and has the highest population.",
        "explanation_fr": "L'Asie couvre environ 30 % des terres émergées de la Terre et est le plus peuplé.",
    },
    {
        "id": "g02",
        "category": "Oceans & Relief",
        "grade_level": "Elementary",
        "question_en": "What is the deepest known trench in the world's oceans?",
        "question_fr": "Quelle est la fosse la plus profonde de tous les océans ?",
        "options": ["Java Trench", "Mariana Trench", "Puerto Rico Trench", "Romanche Trench"],
        "correct_idx": 1,
        "explanation_en": "The Mariana Trench reaches a depth of about 10,994 meters in the western Pacific.",
        "explanation_fr": "La fosse des Mariannes atteint près de 11 000 mètres de profondeur dans le Pacifique.",
    },
    {
        "id": "g03",
        "category": "Capitals",
        "grade_level": "Middle School",
        "question_en": "What is the capital city of Japan?",
        "question_fr": "Quelle est la capitale du Japon ?",
        "options": ["Kyoto", "Tokyo", "Osaka", "Nagoya"],
        "correct_idx": 1,
        "explanation_en": "Tokyo has been the capital and imperial seat of Japan since 1868.",
        "explanation_fr": "Tokyo est la capitale officielle et le siège du gouvernement du Japon depuis 1868.",
    },
    {
        "id": "g04",
        "category": "Compass & Navigation",
        "grade_level": "Elementary",
        "question_en": "If you are facing North, which cardinal direction is immediately to your right?",
        "question_fr": "Si tu fais face au Nord, quelle direction cardinale se trouve directement à ta droite ?",
        "options": ["West", "East", "South", "South-East"],
        "correct_idx": 1,
        "explanation_en": "Clockwise on a compass rose: North -> East -> South -> West. East is to your right.",
        "explanation_fr": "Dans le sens horaire : Nord -> Est -> Sud -> Ouest. L'Est est donc à droite.",
    },
    {
        "id": "g05",
        "category": "Rivers",
        "grade_level": "Elementary",
        "question_en": "Which major river flows northward through northeastern Africa into the Mediterranean Sea?",
        "question_fr": "Quel grand fleuve s'écoule vers le nord à travers l'Afrique jusqu'à la Méditerranée ?",
        "options": ["Amazon", "Nile", "Congo", "Yangtze"],
        "correct_idx": 1,
        "explanation_en": "The Nile is the famous African river that empties northward into the Mediterranean.",
        "explanation_fr": "Le Nil est le grand fleuve d'Afrique qui coule vers le nord et se jette dans la Méditerranée.",
    },
    {
        "id": "g06",
        "category": "Mountains",
        "grade_level": "Elementary",
        "question_en": "What is the highest mountain peak above sea level on Earth?",
        "question_fr": "Quel est le plus haut sommet du monde au-dessus du niveau de la mer ?",
        "options": ["K2", "Mount Everest", "Kilimanjaro", "Mont Blanc"],
        "correct_idx": 1,
        "explanation_en": "Mount Everest rises to 8,848.86 meters in the Himalayas on the Nepal-Tibet border.",
        "explanation_fr": "L'Everest culmine à 8 848,86 m dans la chaîne de l'Himalaya.",
    },
    {
        "id": "g07",
        "category": "Capitals",
        "grade_level": "Middle School",
        "question_en": "What is the capital city of Australia?",
        "question_fr": "Quelle est la capitale officielle de l'Australie ?",
        "options": ["Sydney", "Canberra", "Melbourne", "Brisbane"],
        "correct_idx": 1,
        "explanation_en": "Canberra is the federal capital of Australia, chosen as a compromise between Sydney and Melbourne.",
        "explanation_fr": "Canberra est la capitale fédérale de l'Australie (choisie comme compromis entre Sydney et Melbourne).",
    },
    {
        "id": "g08",
        "category": "Cartography",
        "grade_level": "Elementary",
        "question_en": "What is the name of the imaginary line at 0° latitude dividing Earth into North and South?",
        "question_fr": "Quel est le nom de la ligne imaginaire à 0° de latitude séparant l'hémisphère Nord et Sud ?",
        "options": ["Tropic of Cancer", "Equator", "Prime Meridian", "Arctic Circle"],
        "correct_idx": 1,
        "explanation_en": "The Equator is the zero-degree latitude parallel circumnavigating the planet.",
        "explanation_fr": "L'Équateur est le parallèle 0° séparant l'hémisphère Nord et l'hémisphère Sud.",
    },
    {
        "id": "g09",
        "category": "Deserts",
        "grade_level": "Elementary",
        "question_en": "Which is the largest hot subtropical desert in the world?",
        "question_fr": "Quel est le plus grand désert chaud subtropical du monde ?",
        "options": ["Gobi", "Sahara", "Kalahari", "Atacama"],
        "correct_idx": 1,
        "explanation_en": "The Sahara covers over 9 million square kilometers across North Africa.",
        "explanation_fr": "Le Sahara couvre plus de 9 millions de km² en Afrique du Nord.",
    },
    {
        "id": "g10",
        "category": "Oceans",
        "grade_level": "Middle School",
        "question_en": "Which ocean lies directly between Africa and Australia?",
        "question_fr": "Quel océan est situé directement entre l'Afrique et l'Australie ?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Southern Ocean"],
        "correct_idx": 1,
        "explanation_en": "The Indian Ocean is bounded by Asia to the north, Africa to the west, and Australia to the east.",
        "explanation_fr": "L'océan Indien est bordé par l'Afrique à l'ouest, l'Asie au nord et l'Australie à l'est.",
    },
    {
        "id": "g11",
        "category": "Capitals",
        "grade_level": "Middle School",
        "question_en": "What is the capital city of Canada?",
        "question_fr": "Quelle est la capitale fédérale du Canada ?",
        "options": ["Toronto", "Ottawa", "Montreal", "Vancouver"],
        "correct_idx": 1,
        "explanation_en": "Ottawa is the national capital of Canada, located in Ontario.",
        "explanation_fr": "Ottawa est la capitale fédérale du Canada, située dans la province de l'Ontario.",
    },
    {
        "id": "g12",
        "category": "Cartography",
        "grade_level": "Middle School",
        "question_en": "Through which London borough does the internationally adopted Prime Meridian (0° longitude) pass?",
        "question_fr": "Par quel quartier de Londres passe le méridien de Greenwich (0° de longitude) ?",
        "options": ["Westminster", "Greenwich", "Kensington", "Camden"],
        "correct_idx": 1,
        "explanation_en": "The Royal Observatory at Greenwich was chosen as the prime meridian reference point in 1884.",
        "explanation_fr": "L'observatoire royal de Greenwich définit le méridien origine (0° de longitude).",
    },
    {
        "id": "g13",
        "category": "Physical Geography",
        "grade_level": "High School",
        "question_en": "Which country contains more natural lakes than all other countries combined?",
        "question_fr": "Quel pays possède plus de lacs naturels que le reste du monde réuni ?",
        "options": ["Russia", "Canada", "United States", "Brazil"],
        "correct_idx": 1,
        "explanation_en": "Canada holds over 60% of all the world's natural lakes due to past glaciation.",
        "explanation_fr": "Le Canada compte plus de 60 % des lacs naturels de la planète grâce à son passé glaciaire.",
    },
    {
        "id": "g14",
        "category": "Waterfalls",
        "grade_level": "Middle School",
        "question_en": "What is the tallest uninterrupted waterfall in the world, located in Venezuela?",
        "question_fr": "Quelle est la plus haute chute d'eau ininterrompue du monde, située au Venezuela ?",
        "options": ["Niagara Falls", "Angel Falls", "Victoria Falls", "Iguazu Falls"],
        "correct_idx": 1,
        "explanation_en": "Angel Falls (Salto Ángel) drops 979 meters from the Auyán-tepui plateau.",
        "explanation_fr": "Le Salto Ángel (chutes de l'Ange) fait une chute vertigineuse de 979 mètres au Venezuela.",
    },
    {
        "id": "g15",
        "category": "Continents",
        "grade_level": "Elementary",
        "question_en": "Which continent has no permanent native human population and is covered in ice?",
        "question_fr": "Quel continent ne possède aucune population humaine permanente et est couvert de glace ?",
        "options": ["Greenland", "Antarctica", "Arctic", "Patagonia"],
        "correct_idx": 1,
        "explanation_en": "Antarctica is dedicated to peaceful scientific research under the Antarctic Treaty.",
        "explanation_fr": "L'Antarctique est le continent glacé du pôle Sud dédié à la recherche scientifique internationale.",
    },
    {
        "id": "g16",
        "category": "Capitals",
        "grade_level": "Middle School",
        "question_en": "What is the capital city of Senegal, located on the Cap-Vert peninsula?",
        "question_fr": "Quelle est la capitale du Sénégal, située sur la presqu'île du Cap-Vert ?",
        "options": ["Saint-Louis", "Dakar", "Touba", "Thiès"],
        "correct_idx": 1,
        "explanation_en": "Dakar is the capital of Senegal and the westernmost city on the African mainland.",
        "explanation_fr": "Dakar est la capitale du Sénégal et la ville la plus occidentale du continent africain.",
    },
    {
        "id": "g17",
        "category": "Mountain Ranges",
        "grade_level": "Middle School",
        "question_en": "Which mountain range traditionally forms the boundary between Europe and Asia?",
        "question_fr": "Quelle chaîne de montagnes marque traditionnellement la frontière entre l'Europe et l'Asie ?",
        "options": ["Alps", "Ural Mountains", "Carpathians", "Pyrenees"],
        "correct_idx": 1,
        "explanation_en": "The Ural Mountains run north-south through western Russia, separating Europe and Asia.",
        "explanation_fr": "L'Oural est la chaîne montagneuse délimitant géographiquement l'Europe et l'Asie.",
    },
    {
        "id": "g18",
        "category": "Straits & Navigation",
        "grade_level": "High School",
        "question_en": "Which narrow strait connects the Atlantic Ocean to the Mediterranean Sea?",
        "question_fr": "Quel détroit maritime relie l'océan Atlantique à la mer Méditerranée ?",
        "options": ["Strait of Malacca", "Strait of Gibraltar", "Bering Strait", "Bosporus"],
        "correct_idx": 1,
        "explanation_en": "The Strait of Gibraltar is about 13 km wide at its narrowest point between Spain and Morocco.",
        "explanation_fr": "Le détroit de Gibraltar sépare l'Espagne du Maroc et ouvre la Méditerranée sur l'Atlantique.",
    },
    {
        "id": "g19",
        "category": "Rainforests",
        "grade_level": "Elementary",
        "question_en": "Which is the largest tropical rainforest in the world?",
        "question_fr": "Quelle est la plus grande forêt tropicale humide de la planète ?",
        "options": ["Congo Rainforest", "Amazon Rainforest", "Borneo Rainforest", "Daintree Rainforest"],
        "correct_idx": 1,
        "explanation_en": "The Amazon rainforest covers most of the Amazon basin in South America.",
        "explanation_fr": "La forêt amazonienne représente le plus vaste réservoir de biodiversité tropicale sur Terre.",
    },
    {
        "id": "g20",
        "category": "Time Zones",
        "grade_level": "High School",
        "question_en": "Which country spans the most time zones (12 time zones including overseas territories)?",
        "question_fr": "Quel pays compte le plus de fuseaux horaires (12 fuseaux avec ses territoires d'outre-mer) ?",
        "options": ["Russia", "France", "United States", "China"],
        "correct_idx": 1,
        "explanation_en": "France spans 12 distinct time zones because of its overseas territories worldwide.",
        "explanation_fr": "La France compte 12 fuseaux horaires grâce à ses départements et collectivités d'outre-mer.",
    },
    {
        "id": "g21",
        "category": "Capitals",
        "grade_level": "Elementary",
        "question_en": "What is the capital city of Egypt, situated near the Giza Pyramids?",
        "question_fr": "Quelle est la capitale de l'Égypte, située près des pyramides de Gizeh ?",
        "options": ["Alexandria", "Cairo", "Luxor", "Aswan"],
        "correct_idx": 1,
        "explanation_en": "Cairo is the capital of Egypt and one of the largest metropolitan areas in Africa.",
        "explanation_fr": "Le Caire (Cairo) est la capitale de l'Égypte et une métropole historique majeure.",
    },
]

HISTORY_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "h01",
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
        "id": "h02",
        "category": "Science Pioneers",
        "grade_level": "Middle School",
        "question_en": "Which scientist formulated the laws of universal gravitation and classical mechanics in 1687?",
        "question_fr": "Quel savant a formulé la loi de la gravitation universelle et du mouvement en 1687 ?",
        "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Marie Curie"],
        "correct_idx": 1,
        "explanation_en": "Sir Isaac Newton published the laws of motion and gravitation in his Philosophiae Naturalis Principia Mathematica.",
        "explanation_fr": "Isaac Newton a publié les lois fondamentales du mouvement et de la gravité dans les Principia.",
    },
    {
        "id": "h03",
        "category": "Space Exploration",
        "grade_level": "Elementary",
        "question_en": "In what year did humans first land and walk on the Moon (Apollo 11)?",
        "question_fr": "En quelle année l'être humain a-t-il marché sur la Lune pour la première fois (Apollo 11) ?",
        "options": ["1959", "1969", "1975", "1981"],
        "correct_idx": 1,
        "explanation_en": "Neil Armstrong and Buzz Aldrin stepped onto the lunar surface on July 20, 1969.",
        "explanation_fr": "Neil Armstrong et Buzz Aldrin ont foulé le sol lunaire le 20 juillet 1969.",
    },
    {
        "id": "h04",
        "category": "Inventions",
        "grade_level": "Elementary",
        "question_en": "Who mechanized the movable-type printing press in Europe around 1440?",
        "question_fr": "Qui a inventé l'imprimerie à caractères métalliques mobiles en Europe vers 1440 ?",
        "options": ["Leonardo da Vinci", "Johannes Gutenberg", "Alexander Bell", "Thomas Edison"],
        "correct_idx": 1,
        "explanation_en": "Johannes Gutenberg mechanized the movable-type printing press, sparking a knowledge revolution.",
        "explanation_fr": "Johannes Gutenberg a inventé l'imprimerie moderne, démocratisant l'accès au savoir.",
    },
    {
        "id": "h05",
        "category": "Ancient Rome",
        "grade_level": "Middle School",
        "question_en": "Which shallow river did Julius Caesar cross in 49 BCE, uttering 'Alea iacta est' (The die is cast)?",
        "question_fr": "Quel cours d'eau Jules César a-t-il franchi en 49 av. J.-C. en déclarant 'Le sort en est jeté' ?",
        "options": ["Tiber", "Rubicon", "Rhine", "Danube"],
        "correct_idx": 1,
        "explanation_en": "Crossing the Rubicon river with his legion marked Caesar's defiance of the Roman Senate.",
        "explanation_fr": "Le franchissement du Rubicon a déclenché la guerre civile à Rome.",
    },
    {
        "id": "h06",
        "category": "Renaissance",
        "grade_level": "Elementary",
        "question_en": "Which polymath painted the Mona Lisa and designed early concepts of helicopters?",
        "question_fr": "Quel génie universel a peint La Joconde et dessiné les premiers croquis d'hélicoptère ?",
        "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
        "correct_idx": 1,
        "explanation_en": "Leonardo da Vinci excelled across art, engineering, anatomy, and mathematics during the Renaissance.",
        "explanation_fr": "Léonard de Vinci était à la fois artiste, ingénieur et scientifique d'exception.",
    },
    {
        "id": "h07",
        "category": "Space Exploration",
        "grade_level": "Middle School",
        "question_en": "Who was the first human to travel into outer space, orbiting Earth in Vostok 1 in 1961?",
        "question_fr": "Qui a été le tout premier être humain dans l'espace à bord de Vostok 1 en 1961 ?",
        "options": ["Neil Armstrong", "Yuri Gagarin", "John Glenn", "Alan Shepard"],
        "correct_idx": 1,
        "explanation_en": "Soviet cosmonaut Yuri Gagarin made history on April 12, 1961 by completing one orbit around Earth.",
        "explanation_fr": "Youri Gagarine a accompli le premier vol orbital habité le 12 avril 1961.",
    },
    {
        "id": "h08",
        "category": "Monuments",
        "grade_level": "Elementary",
        "question_en": "What monumental structure in northern China stretches thousands of kilometers for border defense?",
        "question_fr": "Quelle immense fortification traverse le nord de la Chine pour protéger ses frontières ?",
        "options": ["Terracotta Army", "Great Wall of China", "Forbidden City", "Grand Canal"],
        "correct_idx": 1,
        "explanation_en": "The Great Wall of China was constructed and rebuilt over dynasties to defend against northern invasions.",
        "explanation_fr": "La Grande Muraille de Chine a été érigée sur plusieurs millénaires à des fins défensives.",
    },
    {
        "id": "h09",
        "category": "Industrial Era",
        "grade_level": "Middle School",
        "question_en": "Whose crucial improvements to the steam engine powered the Industrial Revolution?",
        "question_fr": "Quel ingénieur écossais a perfectionné la machine à vapeur, moteur de la Révolution industrielle ?",
        "options": ["Henry Ford", "James Watt", "Robert Fulton", "George Stephenson"],
        "correct_idx": 1,
        "explanation_en": "James Watt's separate condenser dramatically improved efficiency and sparked industrial automation.",
        "explanation_fr": "James Watt a perfectionné le condenseur séparé de la machine à vapeur.",
    },
    {
        "id": "h10",
        "category": "Medicine & Science",
        "grade_level": "Middle School",
        "question_en": "Who discovered the first antibiotic, penicillin, in 1928 after noticing mold killed bacteria?",
        "question_fr": "Qui a découvert le premier antibiotique, la pénicilline, en 1928 ?",
        "options": ["Louis Pasteur", "Alexander Fleming", "Edward Jenner", "Robert Koch"],
        "correct_idx": 1,
        "explanation_en": "Alexander Fleming observed that Penicillium notatum mold prevented staphylococcus bacterial growth.",
        "explanation_fr": "Alexander Fleming a découvert la pénicilline issue d'une moisissure bactériostatique.",
    },
    {
        "id": "h11",
        "category": "Ancient Philosophy",
        "grade_level": "High School",
        "question_en": "Which ancient Greek philosopher was the personal tutor of young Alexander the Great?",
        "question_fr": "Quel philosophe grec de l'Antiquité a été le précepteur d'Alexandre le Grand ?",
        "options": ["Socrates", "Aristotle", "Plato", "Pythagoras"],
        "correct_idx": 1,
        "explanation_en": "Aristotle tutored Alexander in Macedon before founding his own Lyceum academy in Athens.",
        "explanation_fr": "Aristote a instruit le jeune Alexandre en Macédoine avant de fonder le Lycée à Athènes.",
    },
    {
        "id": "h12",
        "category": "Human Rights",
        "grade_level": "High School",
        "question_en": "In what year did the United Nations adopt the Universal Declaration of Human Rights in Paris?",
        "question_fr": "En quelle année l'Assemblée générale de l'ONU a-t-elle adopté la Déclaration universelle des droits de l'homme ?",
        "options": ["1919", "1945", "1948", "1954"],
        "correct_idx": 2,
        "explanation_en": "The landmark Declaration of Human Rights was adopted on December 10, 1948.",
        "explanation_fr": "La Déclaration universelle des droits de l'homme a été adoptée le 10 décembre 1948 à Paris.",
    },
    {
        "id": "h13",
        "category": "Science Pioneers",
        "grade_level": "Middle School",
        "question_en": "Who is the only person to win two Nobel Prizes in two different scientific fields (Physics & Chemistry)?",
        "question_fr": "Qui est la seule personne à avoir reçu deux prix Nobel dans deux sciences distinctes (Physique et Chimie) ?",
        "options": ["Albert Einstein", "Marie Curie", "Linus Pauling", "Max Planck"],
        "correct_idx": 1,
        "explanation_en": "Marie Curie won the 1903 Nobel in Physics (radiation) and 1911 Nobel in Chemistry (radium and polonium).",
        "explanation_fr": "Marie Curie a remporté le Nobel de Physique en 1903 et de Chimie en 1911.",
    },
    {
        "id": "h14",
        "category": "Pre-Columbian History",
        "grade_level": "Middle School",
        "question_en": "Which South American civilization built the mountain citadel of Machu Picchu in the Andes?",
        "question_fr": "Quelle civilisation précolombienne a érigé la cité sacrée du Machu Picchu dans les Andes ?",
        "options": ["Aztecs", "Incas", "Mayas", "Toltecs"],
        "correct_idx": 1,
        "explanation_en": "The Inca Empire constructed Machu Picchu around 1450 CE under Emperor Pachacuti.",
        "explanation_fr": "L'Empire inca a édifié la citadelle du Machu Picchu au sommet des Andes péruviennes.",
    },
    {
        "id": "h15",
        "category": "Age of Discovery",
        "grade_level": "Middle School",
        "question_en": "Whose expedition completed the first recorded circumnavigation of the globe between 1519 and 1522?",
        "question_fr": "Quelle expédition a accompli le premier tour du monde à la voile entre 1519 et 1522 ?",
        "options": ["Christopher Columbus", "Ferdinand Magellan", "Vasco da Gama", "James Cook"],
        "correct_idx": 1,
        "explanation_en": "Magellan led the expedition, which was completed by Juan Sebastián Elcano after Magellan's death in the Philippines.",
        "explanation_fr": "L'expédition de Fernand de Magellan (achevée par Elcano) a prouvé la rotondité des mers du globe.",
    },
    {
        "id": "h16",
        "category": "Ancient Law",
        "grade_level": "High School",
        "question_en": "The Code of Hammurabi, one of history's earliest deciphered legal codes, originated in which ancient region?",
        "question_fr": "Le Code de Hammurabi, l'un des premiers recueils de lois gravés, provient de quelle civilisation ?",
        "options": ["Ancient Rome", "Babylon (Mesopotamia)", "Ancient Persia", "Shang China"],
        "correct_idx": 1,
        "explanation_en": "King Hammurabi of Babylon promulgated the basalt stele code around 1750 BCE.",
        "explanation_fr": "Hammurabi, roi de Babylone en Mésopotamie, a fait graver ce célèbre code de lois vers 1750 av. J.-C.",
    },
    {
        "id": "h17",
        "category": "Literature & Drama",
        "grade_level": "Elementary",
        "question_en": "Which English playwright authored 'Romeo and Juliet', 'Hamlet', and 'Macbeth'?",
        "question_fr": "Quel dramaturge anglais a écrit 'Roméo et Juliette', 'Hamlet' et 'Macbeth' ?",
        "options": ["Charles Dickens", "William Shakespeare", "George Orwell", "Jane Austen"],
        "correct_idx": 1,
        "explanation_en": "William Shakespeare wrote some of the most enduring plays in world literature during the Elizabethan era.",
        "explanation_fr": "William Shakespeare est considéré comme l'un des plus grands auteurs de l'époque élisabéthaine.",
    },
    {
        "id": "h18",
        "category": "Inventions",
        "grade_level": "Middle School",
        "question_en": "Who is credited with securing the first practical patent for the acoustic telephone in 1876?",
        "question_fr": "Qui a déposé le premier brevet pratique du téléphone acoustique en 1876 ?",
        "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Samuel Morse"],
        "correct_idx": 1,
        "explanation_en": "Alexander Graham Bell was awarded the US patent for transmitting vocal sounds telegraphically in 1876.",
        "explanation_fr": "Alexander Graham Bell a breveté l'invention du téléphone en 1876.",
    },
    {
        "id": "h19",
        "category": "Cold War",
        "grade_level": "Middle School",
        "question_en": "In what year did the Berlin Wall fall, signaling the end of the Cold War division in Europe?",
        "question_fr": "En quelle année le mur de Berlin est-il tombé, marquant la fin de la Guerre froide en Europe ?",
        "options": ["1979", "1989", "1991", "1995"],
        "correct_idx": 1,
        "explanation_en": "On November 9, 1989, border checkpoints opened and citizens dismantled the wall.",
        "explanation_fr": "Le 9 novembre 1989, l'ouverture des frontières a conduit à la chute du mur de Berlin.",
    },
    {
        "id": "h20",
        "category": "Nonviolent Resistance",
        "grade_level": "High School",
        "question_en": "Who led the Salt March in 1930 against British colonial salt monopoly using Satyagraha (nonviolence)?",
        "question_fr": "Qui a conduit la Marche du sel en 1930 pour dénoncer le monopole colonial britannique par la non-violence ?",
        "options": ["Nelson Mandela", "Mahatma Gandhi", "Martin Luther King Jr.", "Jawaharlal Nehru"],
        "correct_idx": 1,
        "explanation_en": "Mahatma Gandhi marched 390 km to Dandi to produce salt and spark mass civil disobedience in India.",
        "explanation_fr": "Le Mahatma Gandhi a mené la Marche du sel pour libérer pacifiquement l'Inde du joug colonial.",
    },
    {
        "id": "h21",
        "category": "Archaeology",
        "grade_level": "High School",
        "question_en": "Which famous multilingual stone tablet enabled Jean-François Champollion to decipher ancient Egyptian hieroglyphs?",
        "question_fr": "Quelle célèbre stèle multilingue a permis à Jean-François Champollion de déchiffrer les hiéroglyphes égyptiens ?",
        "options": ["Behistun Inscription", "Rosetta Stone", "Dead Sea Scrolls", "Palermo Stone"],
        "correct_idx": 1,
        "explanation_en": "The Rosetta Stone contained the same decree in Hieroglyphic, Demotic, and Ancient Greek.",
        "explanation_fr": "La pierre de Rosette présentait le même texte en hiéroglyphes, démotique et grec ancien.",
    },
]

SCIENCE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "s01",
        "category": "Physics & Chemistry",
        "grade_level": "Elementary",
        "question_en": "What is the central core of an atom that contains protons and neutrons called?",
        "question_fr": "Comment appelle-t-on le cœur central d'un atome contenant les protons et neutrons ?",
        "options": ["Electron cloud", "Nucleus", "Molecule", "Photon"],
        "correct_idx": 1,
        "explanation_en": "The nucleus is the extremely dense core where almost all of an atom's mass resides.",
        "explanation_fr": "Le noyau atomique rassemble les nucléons (protons et neutrons) et concentre l'essentiel de la masse.",
    },
    {
        "id": "s02",
        "category": "Cell Biology",
        "grade_level": "Middle School",
        "question_en": "Which organelle is known as the 'powerhouse of the cell' because it produces ATP energy?",
        "question_fr": "Quel organite cellulaire est surnommé la 'centrale énergétique' car il produit l'ATP ?",
        "options": ["Ribosome", "Mitochondrion", "Golgi apparatus", "Endoplasmic reticulum"],
        "correct_idx": 1,
        "explanation_en": "Mitochondria generate most of the chemical energy needed to power the cell's biochemical reactions.",
        "explanation_fr": "La mitochondrie réalise la respiration cellulaire et produit l'énergie vitale sous forme d'ATP.",
    },
    {
        "id": "s03",
        "category": "Periodic Table",
        "grade_level": "Middle School",
        "question_en": "What is the chemical symbol for the noble metal Gold on the periodic table?",
        "question_fr": "Quel est le symbole chimique de l'Or dans le tableau périodique des éléments ?",
        "options": ["Ag", "Au", "Fe", "Cu"],
        "correct_idx": 1,
        "explanation_en": "Au comes from the Latin word for gold, 'aurum' (shining dawn).",
        "explanation_fr": "Le symbole Au provient du latin 'aurum' signifiant 'brillant' ou 'aurore'.",
    },
    {
        "id": "s04",
        "category": "Astronomy",
        "grade_level": "Elementary",
        "question_en": "Which planet in our solar system is nicknamed the 'Red Planet' due to iron oxide rust on its surface?",
        "question_fr": "Quelle planète de notre système solaire est surnommée la 'Planète rouge' à cause de l'oxyde de fer ?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "correct_idx": 1,
        "explanation_en": "Mars appears reddish because of pervasive iron(III) oxide (rust) across its dusty surface.",
        "explanation_fr": "Mars présente une teinte rougeâtre caractéristique causée par la poussière d'oxyde de fer.",
    },
    {
        "id": "s05",
        "category": "Botany & Ecology",
        "grade_level": "Elementary",
        "question_en": "What biological process allows green plants to convert sunlight, carbon dioxide, and water into glucose?",
        "question_fr": "Quel processus permet aux plantes vertes de transformer la lumière, le CO₂ et l'eau en sucres ?",
        "options": ["Fermentation", "Photosynthesis", "Transpiration", "Decomposition"],
        "correct_idx": 1,
        "explanation_en": "Photosynthesis uses chlorophyll to capture photon energy and synthesize sugars while releasing O2.",
        "explanation_fr": "La photosynthèse capte la lumière du soleil pour synthétiser des glucides et libérer de l'oxygène.",
    },
    {
        "id": "s06",
        "category": "Optics & Physics",
        "grade_level": "Middle School",
        "question_en": "What is the approximate speed of light (c) traveling through a vacuum?",
        "question_fr": "Quelle est la vitesse approximative de la lumière (c) dans le vide ?",
        "options": ["3,000 km/s", "300,000 km/s", "3,000,000 km/s", "30,000 km/s"],
        "correct_idx": 1,
        "explanation_en": "Light travels at approximately 299,792 km per second (often rounded to 300,000 km/s).",
        "explanation_fr": "La lumière se déplace à près de 300 000 km par seconde dans le vide.",
    },
    {
        "id": "s07",
        "category": "States of Matter",
        "grade_level": "Elementary",
        "question_en": "Which state of matter has a definite volume but adapts to the shape of its container?",
        "question_fr": "Quel état de la matière possède un volume défini mais adopte la forme du récipient qui le contient ?",
        "options": ["Solid", "Liquid", "Gas", "Plasma"],
        "correct_idx": 1,
        "explanation_en": "Liquids have fixed volume due to cohesive intermolecular forces, but flow freely to take container shape.",
        "explanation_fr": "Un liquide a un volume propre invariable mais n'a pas de forme propre.",
    },
    {
        "id": "s08",
        "category": "Atmospheric Science",
        "grade_level": "Middle School",
        "question_en": "Which gas makes up approximately 78% of Earth's atmosphere by volume?",
        "question_fr": "Quel gaz compose environ 78 % de l'atmosphère terrestre en volume ?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Argon"],
        "correct_idx": 1,
        "explanation_en": "Nitrogen (N₂) makes up 78%, Oxygen (O₂) makes up 21%, and Argon makes up ~0.9%.",
        "explanation_fr": "Le diazote (N₂) représente environ 78 % de l'air, devant l'oxygène (~21 %).",
    },
    {
        "id": "s09",
        "category": "Genetics",
        "grade_level": "Middle School",
        "question_en": "What geometric shape describes the two intertwined strands of a DNA molecule?",
        "question_fr": "Quelle forme géométrique décrit la structure enroulée de la molécule d'ADN ?",
        "options": ["Single Ring", "Double Helix", "Triple Strand", "Planar Sheet"],
        "correct_idx": 1,
        "explanation_en": "Watson and Crick, aided by Rosalind Franklin's X-ray photo 51, revealed the DNA double helix.",
        "explanation_fr": "La molécule d'ADN forme une double hélice hélicoïdale stabilisée par des liaisons hydrogène.",
    },
    {
        "id": "s10",
        "category": "Classical Mechanics",
        "grade_level": "Elementary",
        "question_en": "What fundamental force attracts two objects with mass toward each other?",
        "question_fr": "Quelle force fondamentale attire deux corps massifs l'un vers l'autre ?",
        "options": ["Magnetism", "Gravity", "Strong force", "Friction"],
        "correct_idx": 1,
        "explanation_en": "Gravity is the attractive force that keeps planets in orbit and objects on the ground.",
        "explanation_fr": "La gravitation est l'interaction attractive qui régit les orbites et le poids des objets.",
    },
    {
        "id": "s11",
        "category": "Chemistry & Solutions",
        "grade_level": "Middle School",
        "question_en": "On the pH scale (0 to 14), what number represents pure neutral water at 25°C?",
        "question_fr": "Sur l'échelle de pH (0 à 14), quelle valeur correspond à une eau pure neutre à 25 °C ?",
        "options": ["0", "7", "10", "14"],
        "correct_idx": 1,
        "explanation_en": "A pH of 7 represents equal concentrations of H+ and OH- ions (neutral). Less than 7 is acidic, above 7 is basic.",
        "explanation_fr": "Un pH de 7 est neutre. En dessous de 7 la solution est acide, au-dessus elle est basique.",
    },
    {
        "id": "s12",
        "category": "Astronomy",
        "grade_level": "Elementary",
        "question_en": "What is the closest star to our planet Earth?",
        "question_fr": "Quelle est l'étoile la plus proche de la Terre ?",
        "options": ["Proxima Centauri", "The Sun", "Sirius", "Polaris"],
        "correct_idx": 1,
        "explanation_en": "The Sun is our local star, located about 150 million kilometers (1 AU) from Earth.",
        "explanation_fr": "Le Soleil est l'étoile centrale de notre système planétaire, à 150 millions de km de la Terre.",
    },
    {
        "id": "s13",
        "category": "Human Anatomy",
        "grade_level": "Middle School",
        "question_en": "Which blood cells contain hemoglobin and transport oxygen to bodily tissues?",
        "question_fr": "Quelles cellules sanguines contiennent l'hémoglobine et transportent l'oxygène ?",
        "options": ["White Blood Cells", "Red Blood Cells (Erythrocytes)", "Platelets", "Plasma"],
        "correct_idx": 1,
        "explanation_en": "Red blood cells (erythrocytes) bind oxygen using iron-rich hemoglobin protein.",
        "explanation_fr": "Les globules rouges (hématies) transportent l'oxygène grâce à l'hémoglobine.",
    },
    {
        "id": "s14",
        "category": "Newton's Laws",
        "grade_level": "Middle School",
        "question_en": "What does Newton's Third Law of Motion state?",
        "question_fr": "Quel principe énonce la troisième loi du mouvement de Newton (action-réaction) ?",
        "options": [
            "Objects at rest stay at rest",
            "For every action, there is an equal and opposite reaction",
            "Force equals mass times acceleration",
            "Energy cannot be created or destroyed",
        ],
        "correct_idx": 1,
        "explanation_en": "When body A exerts a force on body B, body B exerts an equal and opposite force on body A.",
        "explanation_fr": "Tout corps exerçant une force sur un autre subit en retour une force d'égale intensité mais de sens opposé.",
    },
    {
        "id": "s15",
        "category": "Thermodynamics",
        "grade_level": "Elementary",
        "question_en": "At standard atmospheric pressure, at what Celsius temperature does pure water boil?",
        "question_fr": "À pression atmosphérique standard, à quelle température l'eau pure entre-t-elle en ébullition ?",
        "options": ["50°C", "100°C", "150°C", "212°C"],
        "correct_idx": 1,
        "explanation_en": "Water boils at 100°C (212°F) at 1 atmosphere of pressure at sea level.",
        "explanation_fr": "L'eau pure bout à 100 °C au niveau de la mer sous 1 atmosphère de pression.",
    },
    {
        "id": "s16",
        "category": "Electromagnetism",
        "grade_level": "Elementary",
        "question_en": "Which atomic subparticle possesses a negative elementary electric charge (-1e)?",
        "question_fr": "Quelle particule de l'atome possède une charge électrique élémentaire négative (-1e) ?",
        "options": ["Proton", "Electron", "Neutron", "Positron"],
        "correct_idx": 1,
        "explanation_en": "Electrons carry a negative charge (-1), protons carry positive (+1), and neutrons are neutral (0).",
        "explanation_fr": "L'électron porte une charge négative, le proton est positif et le neutron est neutre.",
    },
    {
        "id": "s17",
        "category": "Plate Tectonics",
        "grade_level": "High School",
        "question_en": "What type of tectonic boundary occurs when two tectonic plates slide horizontally past one another?",
        "question_fr": "Quel type de frontière tectonique se forme lorsque deux plaques glissent horizontalement l'une contre l'autre ?",
        "options": ["Convergent boundary", "Transform boundary", "Divergent boundary", "Subduction zone"],
        "correct_idx": 1,
        "explanation_en": "A transform fault (such as the San Andreas Fault) accommodates horizontal shear motion.",
        "explanation_fr": "Une faille transformante (comme la faille de San Andreas) coulisse horizontalement sous contrainte de cisaillement.",
    },
    {
        "id": "s18",
        "category": "Astrophysics",
        "grade_level": "High School",
        "question_en": "What nuclear reaction powers the core of our Sun, converting hydrogen into helium?",
        "question_fr": "Quelle réaction nucléaire alimente le cœur du Soleil en fusionnant l'hydrogène en hélium ?",
        "options": ["Nuclear Fission", "Nuclear Fusion", "Radioactive Decay", "Chemical Combustion"],
        "correct_idx": 1,
        "explanation_en": "In stellar cores, intense pressure fuses hydrogen nuclei into helium, releasing enormous radiative energy.",
        "explanation_fr": "La fusion thermonucléaire transforme les noyaux d'hydrogène en hélium avec un dégagement d'énergie colossal.",
    },
    {
        "id": "s19",
        "category": "Compounds",
        "grade_level": "Elementary",
        "question_en": "What is the common chemical formula for ordinary table salt?",
        "question_fr": "Quelle est la formule chimique du sel de table ordinaire ?",
        "options": ["H₂O", "NaCl", "CO₂", "CaCO₃"],
        "correct_idx": 1,
        "explanation_en": "Table salt is sodium chloride (NaCl), composed of sodium (Na+) and chloride (Cl-) ions.",
        "explanation_fr": "Le sel de cuisine est le chlorure de sodium (NaCl), constitué d'ions sodium et chlorure.",
    },
    {
        "id": "s20",
        "category": "Classification of Life",
        "grade_level": "Middle School",
        "question_en": "To which biological biological kingdom do mushrooms, molds, and yeasts belong?",
        "question_fr": "À quel règne du vivant appartiennent les champignons, moisissures et levures ?",
        "options": ["Plantae", "Fungi", "Protista", "Animalia"],
        "correct_idx": 1,
        "explanation_en": "Fungi are eukaryotic organisms with chitinous cell walls that absorb nutrients by heterotrophy.",
        "explanation_fr": "Les champignons forment le règne des Eumycètes (Fungi), distincts des végétaux et des animaux.",
    },
    {
        "id": "s21",
        "category": "Kinetic Energy",
        "grade_level": "High School",
        "question_en": "According to the kinetic energy formula (Ek = 1/2 m v²), if speed doubles, kinetic energy increases by:",
        "question_fr": "D'après la formule de l'énergie cinétique (Ec = 1/2 m v²), si la vitesse double, l'énergie cinétique est :",
        "options": ["Doubled (2×)", "Quadrupled (4×)", "Tripled (3×)", "Unchanged"],
        "correct_idx": 1,
        "explanation_en": "Because velocity is squared (v²), doubling velocity multiplies kinetic energy by 2² = 4.",
        "explanation_fr": "La vitesse intervenant au carré (v²), doubler la vitesse multiplie l'énergie par 2² = 4 (quadruplée).",
    },
]


# ===========================================================================
# 2. LEARNING GAMES ENGINE & STATE MANAGER
# ===========================================================================

class LearningGamesEngine:
    """
    Manages active state for all 6 educational games:
    - 📐 Math Quest
    - 🔤 Word Voyage
    - 🌍 Geo Explorer
    - ⏳ Time Traveler
    - 🔬 Science Explorer
    - 🗺️ Adventure Odyssey (multi-subject RPG dungeon across all 5 fields)

    Hooks into student profile persistence (student_profile.json) and Lumi tutor.
    """

    GAMES = {
        "math": {"title_en": "📐 Math Quest", "title_fr": "📐 Quête Mathématique", "bank": MATH_QUESTIONS},
        "language": {"title_en": "🔤 Word Voyage", "title_fr": "🔤 Voyage des Mots", "bank": LANGUAGE_QUESTIONS},
        "geography": {"title_en": "🌍 Geo Explorer", "title_fr": "🌍 Géo Explorateur", "bank": GEOGRAPHY_QUESTIONS},
        "history": {"title_en": "⏳ Time Traveler", "title_fr": "⏳ Voyageur du Temps", "bank": HISTORY_QUESTIONS},
        "science": {"title_en": "🔬 Science Explorer", "title_fr": "🔬 Explorateur Scientifique", "bank": SCIENCE_QUESTIONS},
        "adventure": {"title_en": "🗺️ Adventure Odyssey", "title_fr": "🗺️ L'Odyssée Apprenante", "bank": []},
        "revision": {"title_en": "🧠 Smart Revision", "title_fr": "🧠 Révision Lumi", "bank": []},
    }

    def __init__(
        self,
        lang: str = "en",
        pack_mgr: Optional[Any] = None,
        adaptive_tutor: Optional[Any] = None,
    ):
        self.lang = lang
        self.pack_mgr = pack_mgr
        self.adaptive_tutor = adaptive_tutor
        self.active_game_id: str = "math"
        self.current_q_idx: int = 0
        self.score: int = 0
        self.combo_streak: int = 0
        self.best_streak: int = 0
        self.total_answered: int = 0
        self.total_correct: int = 0
        self.last_result: Optional[Dict[str, Any]] = None
        self.sound_enabled: bool = True

        # Missed questions queue for Lumi Smart Revision
        self.missed_question_ids: List[str] = []
        if self.pack_mgr is not None and hasattr(self.pack_mgr, "profile"):
            self.missed_question_ids = list(self.pack_mgr.profile.get("missed_question_ids", []))

        # Subject-specific metrics
        self.subject_stats: Dict[str, Dict[str, int]] = {
            "math": {"answered": 0, "correct": 0, "score": 0},
            "language": {"answered": 0, "correct": 0, "score": 0},
            "geography": {"answered": 0, "correct": 0, "score": 0},
            "history": {"answered": 0, "correct": 0, "score": 0},
            "science": {"answered": 0, "correct": 0, "score": 0},
            "adventure": {"answered": 0, "correct": 0, "score": 0},
        }

        # Adventure Odyssey State (5 chambers representing the 5 disciplines)
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

    def get_revision_bank(self) -> List[Dict[str, Any]]:
        """Builds a personalized Lumi Smart Revision deck from missed questions or advanced challenges."""
        all_qs = (
            MATH_QUESTIONS
            + LANGUAGE_QUESTIONS
            + GEOGRAPHY_QUESTIONS
            + HISTORY_QUESTIONS
            + SCIENCE_QUESTIONS
        )
        if self.missed_question_ids:
            missed_set = set(self.missed_question_ids)
            missed_qs = [q for q in all_qs if q.get("id") in missed_set]
            if missed_qs:
                return missed_qs
        # Fallback: Middle & High School mastery review across all 5 subjects
        adv = [q for q in all_qs if q.get("grade_level") in ("Middle School", "High School")]
        return adv if adv else all_qs

    def get_current_question(self) -> Dict[str, Any]:
        """Returns the current active question for the selected game."""
        if self.active_game_id == "revision":
            bank = self.get_revision_bank()
            q = bank[self.current_q_idx % len(bank)]
            return {**q, "is_revision": True, "missed_count": len(self.missed_question_ids)}

        if self.active_game_id == "adventure":
            # Round-robin through Math -> Lang -> Geo -> History -> Science
            subject_banks = [
                MATH_QUESTIONS,
                LANGUAGE_QUESTIONS,
                GEOGRAPHY_QUESTIONS,
                HISTORY_QUESTIONS,
                SCIENCE_QUESTIONS,
            ]
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
        Synchronizes with student profile and Lumi adaptive tutor.
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
            elif self.active_game_id == "revision":
                qid = q.get("id")
                if qid and qid in self.missed_question_ids:
                    self.missed_question_ids.remove(qid)
                    points_earned += 50  # Mastery bonus
                    self.score += 50
        else:
            self.combo_streak = 0
            qid = q.get("id")
            if qid and qid not in self.missed_question_ids:
                self.missed_question_ids.append(qid)

        if self.pack_mgr is not None and hasattr(self.pack_mgr, "profile"):
            self.pack_mgr.profile["missed_question_ids"] = list(self.missed_question_ids)

        # Offline audio chime feedback
        try:
            from workbench.audio_feedback import play_chime
            if is_correct:
                play_chime("combo" if self.combo_streak >= 3 else "correct", enabled=self.sound_enabled)
            else:
                play_chime("wrong", enabled=self.sound_enabled)
        except Exception:
            pass

        # Update per-subject stats
        cur_subj = self.active_game_id
        if cur_subj in self.subject_stats:
            self.subject_stats[cur_subj]["answered"] += 1
            if is_correct:
                self.subject_stats[cur_subj]["correct"] += 1
                self.subject_stats[cur_subj]["score"] += points_earned

        # Sync to student profile if LearningPackManager is available
        if self.pack_mgr is not None and hasattr(self.pack_mgr, "record_learning_game_activity"):
            try:
                self.pack_mgr.record_learning_game_activity(
                    subject=cur_subj,
                    is_correct=is_correct,
                    points=points_earned,
                    combo=self.combo_streak,
                    dungeon_gems=self.dungeon_gems,
                    dungeon_completed=self.dungeon_completed,
                )
            except Exception:
                pass

        # Sync to Lumi adaptive tutor if available
        if self.adaptive_tutor is not None and hasattr(self.adaptive_tutor, "record_attempt"):
            try:
                cat = q.get("category", cur_subj)
                self.adaptive_tutor.record_attempt(
                    subject=cur_subj,
                    score=100.0 if is_correct else 0.0,
                    concept=cat,
                    struggle_detected=(not is_correct),
                )
            except Exception:
                pass

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
        """Returns overall learning game stats for student profile and report card."""
        accuracy = (self.total_correct / self.total_answered * 100.0) if self.total_answered > 0 else 0.0
        return {
            "score": self.score,
            "total_answered": self.total_answered,
            "total_correct": self.total_correct,
            "accuracy_pct": round(accuracy, 1),
            "best_streak": self.best_streak,
            "dungeon_gems": self.dungeon_gems,
            "dungeon_completed": self.dungeon_completed,
            "subject_stats": dict(self.subject_stats),
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
    - 6 learning game tabs (Math, Language, Geography, History, Science, Adventure Odyssey)
    - Big clickable answer cards with instant Socratic feedback
    - Combo streak multipliers and Star points
    - Persists progress to student profile on every answer
    """

    def __init__(
        self,
        parent_window=None,
        lang: str = "en",
        pack_mgr: Optional[Any] = None,
        adaptive_tutor: Optional[Any] = None,
    ):
        self.engine = LearningGamesEngine(lang=lang, pack_mgr=pack_mgr, adaptive_tutor=adaptive_tutor)
        self.lang = lang
        self.pack_mgr = pack_mgr
        if not GTK_AVAILABLE:
            self.dialog = None
            return

        self.dialog = Gtk.Dialog(
            title="🎮 Synapse Learning Games Hub — 6 Disciplines",
            transient_for=parent_window,
            flags=0,
        )
        self.dialog.set_default_size(820, 540)
        self.dialog.set_resizable(True)
        self.dialog.add_button("Fermer / Close", Gtk.ResponseType.CLOSE)

        content = self.dialog.get_content_area()
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        content.set_margin_start(12)
        content.set_margin_end(12)

        # Header Selector Row (6 tabs)
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

        # Next Button Row + Offline Read-Aloud TTS Button
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        card_box.pack_start(bottom_row, False, False, 0)

        self.btn_speak = Gtk.Button(label="🔊 Lire / Read Aloud")
        self.btn_speak.connect("clicked", lambda _b: self._on_speak_clicked())
        bottom_row.pack_start(self.btn_speak, False, False, 0)

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
        elif q.get("is_revision"):
            mc = q.get("missed_count", 0)
            room_info = f" · 🧠 Révision Lumi ({mc} à consolider)" if mc > 0 else " · 🧠 Défi Maîtrise"

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

    def _on_speak_clicked(self):
        from workbench.audio_feedback import speak_text
        q = self.engine.get_current_question()
        q_text = q.get("question_fr" if self.lang == "fr" else "question_en", "")
        speak_text(q_text, lang=self.lang, enabled=True)

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
