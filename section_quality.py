def analyze_section_quality(results):
    """
    Analyze the structural and basic content quality
    of lesson-plan sections.

    The validator distinguishes between:
        - Present
        - Empty
        - Missing
        - Needs Improvement

    Special handling:
        - Assessment containing only AFL is considered
          present but needs improvement.

    Parameters:
        results (dict):
            Dictionary containing section names and their
            validation information.

    Returns:
        dict:
            Section-by-section quality information.
    """

    analysis = {}

    for section, section_data in results.items():

        # --------------------------------------------------
        # Get status and content
        # --------------------------------------------------

        if isinstance(section_data, dict):

            status = section_data.get(
                "status",
                "Missing"
            )

            content = section_data.get(
                "content",
                ""
            )

        # --------------------------------------------------
        # Backward compatibility with old True/False format
        # --------------------------------------------------

        else:

            if section_data:

                status = "Present"
                content = ""

            else:

                status = "Missing"
                content = ""

        # --------------------------------------------------
        # Convert content to text
        # --------------------------------------------------

        if isinstance(content, list):

            content_text = " ".join(
                str(item) for item in content
            )

        else:

            content_text = str(content)

        content_text = content_text.strip()

        # --------------------------------------------------
        # ASSESSMENT SPECIAL CHECK
        # --------------------------------------------------

        if section.lower() == "assessment":

            # Empty assessment
            if status == "Empty":

                analysis[section] = {
                    "status": "Empty",
                    "score": 0
                }

                continue

            # Missing assessment
            if status == "Missing":

                analysis[section] = {
                    "status": "Missing",
                    "score": 0
                }

                continue

            # Check whether assessment contains only AFL
            assessment_text = content_text.lower()

            afl_only = (
                assessment_text in [
                    "afl",
                    "assessment for learning",
                    "a.f.l.",
                    "a.f.l"
                ]
            )

            if afl_only:

                analysis[section] = {
                    "status": "Needs Improvement",
                    "score": 60,
                    "reason": (
                        "Assessment for Learning (AFL) is mentioned, "
                        "but no specific assessment strategy or "
                        "evidence of learning is provided."
                    )
                }

                continue

            # Assessment has actual content
            if status == "Present":

                analysis[section] = {
                    "status": "Strong",
                    "score": 100
                }

                continue

        # --------------------------------------------------
        # PRESENT
        # --------------------------------------------------

        if status == "Present":

            analysis[section] = {
                "status": "Present",
                "score": 100
            }

        # --------------------------------------------------
        # EMPTY
        # --------------------------------------------------

        elif status == "Empty":

            analysis[section] = {
                "status": "Empty",
                "score": 0
            }

        # --------------------------------------------------
        # MISSING
        # --------------------------------------------------

        else:

            analysis[section] = {
                "status": "Missing",
                "score": 0
            }

    return analysis