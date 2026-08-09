from section_extractor import extract_section


def check_learning_objectives(text):

    # --------------------------------------------------
    # Extract the Learning Objectives section
    # --------------------------------------------------

    objectives = extract_section(
        text,
        [
            "learning objectives",
            "learning objective",
            "learning intention"
        ],
        [
            "success criteria",
            "starter",
            "main activity"
        ]
    )

    # --------------------------------------------------
    # Handle the new extractor format
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
    # Backward compatibility
    # --------------------------------------------------

    else:

        if objectives:

            status = "Present"
            content = objectives

        else:

            status = "Missing"
            content = []

    # --------------------------------------------------
    # Missing
    # --------------------------------------------------

    if status == "Missing":

        print("\nChecking Learning Objectives...\n")

        print(
            "❌ Learning Objectives section not found."
        )

        return

    # --------------------------------------------------
    # Empty
    # --------------------------------------------------

    if status == "Empty":

        print("\nChecking Learning Objectives...\n")

        print(
            "⚠ Learning Objectives section is empty."
        )

        print(
            "Add clear, measurable learning objectives "
            "using action verbs."
        )

        return

    # --------------------------------------------------
    # Convert content to text
    # --------------------------------------------------

    if isinstance(content, list):

        objectives_text = " ".join(
            str(item)
            for item in content
        ).lower()

    else:

        objectives_text = str(
            content
        ).lower()

    # --------------------------------------------------
    # Make sure content actually exists
    # --------------------------------------------------

    if not objectives_text.strip():

        print("\nChecking Learning Objectives...\n")

        print(
            "⚠ Learning Objectives section is empty."
        )

        print(
            "Add clear, measurable learning objectives "
            "using action verbs."
        )

        return

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
        "compare",
        "calculate",
        "solve",
        "explain",
        "analyse",
        "analyze",
        "evaluate",
        "create",
        "describe",
        "demonstrate",
        "apply",
        "classify",
        "construct",
        "justify"
    ]

    # --------------------------------------------------
    # Check for weak verbs
    # --------------------------------------------------

    found_weak_verbs = []

    for verb in weak_verbs:

        if verb in objectives_text:

            found_weak_verbs.append(
                verb
            )

    # --------------------------------------------------
    # Check for strong verbs
    # --------------------------------------------------

    found_strong_verbs = []

    for verb in strong_verbs:

        if verb in objectives_text:

            found_strong_verbs.append(
                verb
            )

    # --------------------------------------------------
    # Count objectives
    # --------------------------------------------------

    objective_count = 0

    for line in content if isinstance(content, list) else [content]:

        line = str(line).strip()

        if line:
            objective_count += 1

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    print("\nChecking Learning Objectives...\n")

    # Weak verbs

    if found_weak_verbs:

        for verb in found_weak_verbs:

            print(
                f"⚠ Weak action verb detected: "
                f"'{verb}'"
            )

    # Strong verbs

    if found_strong_verbs:

        print(
            "✅ Measurable action verbs detected:"
        )

        for verb in found_strong_verbs:

            print(
                f"   • {verb.title()}"
            )

    # No measurable verbs

    if not found_strong_verbs:

        print(
            "⚠ No measurable action verbs detected."
        )

    # --------------------------------------------------
    # Objective count
    # --------------------------------------------------

    if objective_count >= 2:

        print(
            f"✅ {objective_count} learning objectives detected."
        )

    else:

        print(
            "⚠ Consider writing at least two "
            "learning objectives."
        )

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    if found_weak_verbs:

        print(
            "\nRecommendation:"
        )

        print(
            "• Rewrite weak objectives using "
            "measurable action verbs."
        )

    if not found_strong_verbs:

        print(
            "• Avoid vague verbs such as "
            "'understand', 'know', and 'learn'."
        )

    print(
        "\nSuggested strong action verbs:"
    )

    for verb in strong_verbs:

        print(
            f"• {verb.title()}"
        )