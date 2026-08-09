import re


def score_learning_objectives(objectives):

    # --------------------------------------------------
    # Initial score
    # --------------------------------------------------

    score = 10
    feedback = []

    # --------------------------------------------------
    # Weak and strong action verbs
    # --------------------------------------------------

    weak_verbs = [
        "understand",
        "know",
        "learn",
        "be aware",
        "appreciate"
    ]

    strong_verbs = [
    "identify",
    "describe",
    "measure",
    "calculate",
    "compare",
    "solve",
    "explain",
    "analyse",
    "analyze",
    "evaluate",
    "create",
    "demonstrate",
    "apply",
    "classify",
    "construct",
    "justify"
]

    # --------------------------------------------------
    # Handle NEW extractor format
    # --------------------------------------------------

    if isinstance(objectives, dict):

        status = objectives.get(
            "status",
            "Missing"
        )

        content = objectives.get(
            "content",
            []
        )

    # --------------------------------------------------
    # Backward compatibility with old format
    # --------------------------------------------------

    else:

        status = "Present"

        content = objectives

    # --------------------------------------------------
    # Missing or empty objectives
    # --------------------------------------------------

    if status == "Missing":

        return 0, [
            "Learning Objectives section was not found.",
            "Add at least two clear learning objectives."
        ]

    if status == "Empty":

        return 0, [
            "Learning Objectives section is empty.",
            "Add at least two clear learning objectives.",
            "Use measurable action verbs such as calculate, "
            "identify, compare, explain, or solve."
        ]

    # --------------------------------------------------
    # Convert content into text
    # --------------------------------------------------

    if isinstance(content, list):

        objective_lines = [
            str(line).strip()
            for line in content
            if str(line).strip()
        ]

    else:

        objective_lines = [
            line.strip()
            for line in str(content).splitlines()
            if line.strip()
        ]

    objectives_text = " ".join(
        objective_lines
    ).lower()

    # --------------------------------------------------
    # Safety check
    # --------------------------------------------------

    if not objectives_text:

        return 0, [
            "Learning Objectives section is empty.",
            "Add at least two clear learning objectives."
        ]

    # --------------------------------------------------
    # Detect weak verbs
    # --------------------------------------------------

    detected_weak = []

    for verb in weak_verbs:

        pattern = r"\b" + re.escape(verb) + r"\b"

        if re.search(
            pattern,
            objectives_text
        ):

            detected_weak.append(
                verb
            )

    # --------------------------------------------------
    # Detect strong verbs
    # --------------------------------------------------

    detected_strong = []

    for verb in strong_verbs:

        pattern = r"\b" + re.escape(verb) + r"\b"

        if re.search(
            pattern,
            objectives_text
        ):

            detected_strong.append(
                verb
            )

    # --------------------------------------------------
    # Weak verb penalty
    # --------------------------------------------------

    for verb in detected_weak:

        score -= 2

        feedback.append(
            f"Avoid using '{verb}'. "
            "Use measurable action verbs."
        )

    # --------------------------------------------------
    # Strong verb check
    # --------------------------------------------------

    if detected_strong:

        feedback.append(
            "Excellent use of measurable action verbs."
        )

    else:

        score -= 2

        feedback.append(
            "No measurable action verbs detected."
        )

    # --------------------------------------------------
    # Number of objectives
    # --------------------------------------------------

    objective_count = len(
        objective_lines
    )

    if objective_count < 2:

        score -= 1

        feedback.append(
            "Consider writing at least two "
            "learning objectives."
        )

    # --------------------------------------------------
    # Application objective
    # --------------------------------------------------

    application_verbs = [
        "apply",
        "calculate",
        "solve",
        "construct",
        "create",
        "justify",
        "demonstrate"
    ]

    has_application = any(
        re.search(
            r"\b" + re.escape(verb) + r"\b",
            objectives_text
        )
        for verb in application_verbs
    )

    if not has_application:

        score -= 1

        feedback.append(
            "Include one application objective "
            "that requires learners to apply "
            "their knowledge."
        )

    # --------------------------------------------------
    # Keep score between 0 and 10
    # --------------------------------------------------

    score = max(
        0,
        min(score, 10)
    )

    return score, feedback