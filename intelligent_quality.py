def analyze_intelligent_quality(text, results):
    """
    Provides an intelligent quality assessment for lesson-plan sections.

    The function uses the structural validation results to determine
    whether a section is Missing, Empty, or Present.

    For Present sections, it evaluates the actual content belonging
    to that section rather than searching the entire document.

    Returns:
        dict containing section status, score, and feedback.
    """

    analysis = {}

    # --------------------------------------------------
    # General quality keywords
    # --------------------------------------------------

    quality_keywords = {

        "Learning Objectives": [
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
        ],

        "Success Criteria": [
          "i can",
          "i will",
          "can",
          "success",
          "able to",
          "will be able to",
          "calculate",
          "identify",
          "measure",
          "find",
          "solve",
          "explain",
          "compare",
         "describe"
        ],

        "Assessment": [
            "question",
            "quiz",
            "observation",
            "assessment",
            "exit ticket",
            "peer assessment",
            "self assessment",
            "afl"
        ],

        "Resources": [
         "book",
         "textbook",
         "cambridge",
         "hodder",
         "worksheet",
         "whiteboard",
         "interactive whiteboard",
         "board",
         "projector",
         "computer",
         "laptop",
         "online materials",
         "online material",
         "video",
         "flashcard",
         "manipulative",
         "maker",
         "ruler",
         "measuring tape",
         "grid",
         "marker",
         "squared paper"


        ]
    }

    # --------------------------------------------------
    # Differentiation-specific indicators
    # --------------------------------------------------

    differentiation_indicators = [

        "support",
        "challenge",
        "extension",
        "sen",
        "scaffold",
        "scaffolding",
        "higher ability",
        "lower ability",
        "more able",
        "less able",
        "targeted support",
        "adult intervention",
        "adult support",
        "teacher support",
        "ta support",
        "teaching assistant",
        "simplify",
        "simplified",
        "easier questions",
        "easy questions",
        "more complex questions",
        "complex questions",
        "challenging questions",
        "challenge questions",
        "different levels",
        "different ability",
        "ability group",
        "grouping",
        "scholar",
        "builder",
        "explorer",
        "visuals",
        "visual support",
        "additional support",
        "individual support"
    ]

    # --------------------------------------------------
    # Process each validated section
    # --------------------------------------------------

    for section, section_data in results.items():

        # --------------------------------------------------
        # New validator format
        # --------------------------------------------------

        if isinstance(section_data, dict):

            structural_status = section_data.get(
                "status",
                "Missing"
            )

            section_content = section_data.get(
                "content",
                []
            )

        # --------------------------------------------------
        # Backward compatibility
        # --------------------------------------------------

        else:

            if section_data:

                structural_status = "Present"

            else:

                structural_status = "Missing"

            section_content = []

        # --------------------------------------------------
        # MISSING
        # --------------------------------------------------

        if structural_status == "Missing":

            analysis[section] = {
                "status": "Missing",
                "score": 0,
                "feedback": (
                    f"{section} is not clearly identified."
                )
            }

            continue

        # --------------------------------------------------
        # EMPTY
        # --------------------------------------------------

        if structural_status == "Empty":

            analysis[section] = {
                "status": "Empty",
                "score": 0,
                "feedback": (
                    f"{section} heading is present, "
                    "but no meaningful content was provided."
                )
            }

            continue

        # --------------------------------------------------
        # Convert section content into text
        # --------------------------------------------------

        if isinstance(section_content, list):

            section_text = " ".join(
                str(item)
                for item in section_content
            ).lower()

        else:

            section_text = str(
                section_content
            ).lower()

        # ==================================================
        # SPECIAL RULE: DIFFERENTIATION
        # ==================================================

        if section == "Differentiation":

            matched_indicators = []

            for indicator in differentiation_indicators:

                if indicator.lower() in section_text:

                    matched_indicators.append(
                        indicator
                    )

            # Remove duplicates while preserving order
            matched_indicators = list(
                dict.fromkeys(
                    matched_indicators
                )
            )

            indicator_count = len(
                matched_indicators
            )

            # ----------------------------------------------
            # Strong differentiation
            # ----------------------------------------------

            if indicator_count >= 3:

                analysis[section] = {
                    "status": "Strong",
                    "score": 100,
                    "feedback": (
                        "Differentiation contains several "
                        "specific strategies for supporting "
                        "different learner needs."
                    )
                }

            # ----------------------------------------------
            # Good differentiation
            # ----------------------------------------------

            elif indicator_count == 2:

                analysis[section] = {
                    "status": "Strong",
                    "score": 85,
                    "feedback": (
                        "Differentiation includes specific "
                        "support or challenge strategies."
                    )
                }

            # ----------------------------------------------
            # Limited differentiation
            # ----------------------------------------------

            elif indicator_count == 1:

                analysis[section] = {
                    "status": "Needs Improvement",
                    "score": 60,
                    "feedback": (
                        "Differentiation is present but "
                        "could include more specific "
                        "support and challenge strategies."
                    )
                }

            # ----------------------------------------------
            # No useful differentiation indicators
            # ----------------------------------------------

            else:

                analysis[section] = {
                    "status": "Needs Improvement",
                    "score": 40,
                    "feedback": (
                        "Differentiation is present but "
                        "does not contain enough specific "
                        "strategies."
                    )
                }

            continue

        # ==================================================
        # STANDARD QUALITY CHECK
        # ==================================================

        keywords = quality_keywords.get(
            section,
            []
        )

        matched_keywords = []

        for keyword in keywords:

            if keyword.lower() in section_text:

                matched_keywords.append(
                    keyword
                )

        # --------------------------------------------------
        # Sections without specific quality rules
        # --------------------------------------------------

        if not keywords:

            analysis[section] = {
                "status": "Present",
                "score": 100,
                "feedback": (
                    f"{section} is present in "
                    "the lesson plan."
                )
            }

            continue

        # --------------------------------------------------
        # Strong
        # --------------------------------------------------

        if len(matched_keywords) >= 2:

            analysis[section] = {
                "status": "Strong",
                "score": 100,
                "feedback": (
                    f"{section} is present and contains "
                    "useful indicators of quality."
                )
            }

        # --------------------------------------------------
        # Needs Improvement
        # --------------------------------------------------

        elif len(matched_keywords) == 1:

            analysis[section] = {
                "status": "Needs Improvement",
                "score": 60,
                "feedback": (
                    f"{section} is present but could "
                    "contain more specific detail."
                )
            }

        # --------------------------------------------------
        # Present but weak
        # --------------------------------------------------

        else:

            analysis[section] = {
                "status": "Needs Improvement",
                "score": 40,
                "feedback": (
                    f"{section} is present but appears "
                    "to require more specific detail."
                )
            }

    return analysis