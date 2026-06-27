# =============================================================================
# config.py
# Global settings, constants, and topic definitions for the Math Learning App.
# All other modules import from here — change a value once, it applies everywhere.
# =============================================================================

APP_NAME = "MathLearningApp"
APP_TITLE = "Math Foundation Builder"
APP_VERSION = "1.0.0"

# -----------------------------------------------------------------------------
# Phase gate thresholds
# -----------------------------------------------------------------------------

# Phase 1 → Phase 2 (Learn → Practice):
# Student must open the lesson page before the completion route unlocks Practice.
# No numeric score is used for this phase.

# Phase 2 → Phase 3 (Practice → Evaluate):
# Student must answer this many consecutive problems correctly
# WITHOUT using "Show Solution" to unlock the Evaluate phase.
PRACTICE_PASS_STREAK = 3          # correct answers needed in a row
PRACTICE_WINDOW_SIZE = 5          # practice problem buffer size, not a pass rule

# Phase 3 — Evaluate:
PROBLEMS_PER_ROUND = 10           # questions per evaluation session
MASTERY_SCORE_PERCENT = 80        # % correct to mark topic as mastered (8/10)
MIN_EVALUATE_ATTEMPTS = 1         # attempts before mastery can be granted

# -----------------------------------------------------------------------------
# Difficulty levels
# Each problem generator accepts one of these strings.
# Difficulty auto-advances when best_score exceeds MASTERY_SCORE_PERCENT
# on the current difficulty level.
# -----------------------------------------------------------------------------
DIFFICULTY_EASY   = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD   = "hard"
DIFFICULTY_ORDER  = [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]

# -----------------------------------------------------------------------------
# Topic definitions
# These keys must exactly match the module filenames in problems/ and content/.
# The order here controls the display order in the UI.
# -----------------------------------------------------------------------------
ALGEBRA_TOPICS = [
    "linear_equations",
    "inequalities",
    "quadratics",
    "exponents_radicals",
    "word_problems",
]

GEOMETRY_TOPICS = [
    "angles_lines",
    "triangles",
    "polygons",
    "circles",
    "coordinate_geometry",
]

ADVANCED_TOPICS = [
    "linear_functions",
    "systems_of_equations",
    "similar_triangles",
    "trigonometry",
    "parabolas_graphs",
    "circle_equations",
    "solid_geometry",
]

# Human-readable labels for each topic key (used in the UI)
TOPIC_LABELS = {
    # Algebra
    "linear_equations":   "Linear Equations",
    "inequalities":       "Inequalities",
    "quadratics":         "Quadratics",
    "exponents_radicals": "Exponents & Radicals",
    "word_problems":      "Word Problems",
    # Geometry
    "angles_lines":         "Angles & Lines",
    "triangles":            "Triangles",
    "polygons":             "Polygons",
    "circles":              "Circles",
    "coordinate_geometry":  "Coordinate Geometry",
    # Advanced
    "linear_functions":    "Linear Functions",
    "systems_of_equations":"Systems of Equations",
    "similar_triangles":   "Similar Triangles",
    "trigonometry":        "Trigonometry",
    "parabolas_graphs":    "Parabolas & Graphs",
    "circle_equations":    "Circle Equations",
    "solid_geometry":      "Solid Geometry",
}

# Subject keys
SUBJECT_ALGEBRA  = "algebra"
SUBJECT_GEOMETRY = "geometry"
SUBJECT_ADVANCED = "advanced"
SUBJECTS_IN_ORDER = [SUBJECT_ALGEBRA, SUBJECT_GEOMETRY, SUBJECT_ADVANCED]

# Geometry is locked until all algebra topics are mastered
GEOMETRY_REQUIRES_ALGEBRA_MASTERY = True
# Advanced is locked until all geometry topics are mastered
ADVANCED_REQUIRES_GEOMETRY_MASTERY = True

# -----------------------------------------------------------------------------
# Phase state constants
# Used throughout progress tracking, sessions, and web routes.
# -----------------------------------------------------------------------------
PHASE_LEARN    = "learn"
PHASE_PRACTICE = "practice"
PHASE_EVALUATE = "evaluate"
PHASES_IN_ORDER = [PHASE_LEARN, PHASE_PRACTICE, PHASE_EVALUATE]

STATUS_NOT_STARTED  = "not_started"
STATUS_IN_PROGRESS  = "in_progress"
STATUS_COMPLETE     = "complete"
STATUS_LOCKED       = "locked"
STATUS_MASTERED     = "mastered"

# -----------------------------------------------------------------------------
# Encouragement messages (shown after correct answers in practice)
# Randomly selected by evaluator.py
# -----------------------------------------------------------------------------
ENCOURAGEMENT_CORRECT = [
    "Great work! Keep it up!",
    "Exactly right! You're getting this.",
    "Perfect! That's the right approach.",
    "Correct! You're building strong foundations.",
    "Nailed it! On to the next one.",
    "Yes! That's exactly it.",
    "Well done! That one wasn't easy.",
]

ENCOURAGEMENT_STREAK = [
    "🔥 {n} in a row! You're on a roll!",
    "🔥 {n} consecutive correct! Great momentum!",
    "🔥 {n} straight! Keep this up!",
]

ENCOURAGEMENT_INCORRECT = [
    "Not quite — check the hint and try again.",
    "Close! Read the hint carefully.",
    "That's not right yet — the hint will guide you.",
    "Keep trying — mistakes are how we learn.",
    "Almost there — take another look at the steps.",
]

ENCOURAGEMENT_MASTERED = [
    "🌟 Topic Mastered! Outstanding work!",
    "🌟 You've mastered this topic! On to the next challenge!",
    "🌟 Mastered! Your hard work is paying off!",
]

ENCOURAGEMENT_RETRY = [
    "Good effort! Review the mistakes and try again.",
    "Not quite there yet — practice a bit more and retry.",
    "Almost! Go back to Practice and lock in the concept.",
]
