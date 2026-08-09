def identify_strengths(structure_score, objective_score):
    """
    Identifies strengths in a lesson plan based on
    structure and learning objective scores.
    """

    strengths = []

    # Structure strengths
    if structure_score >= 90:
        strengths.append(
            "Excellent lesson structure with all or nearly all "
            "key sections included."
        )

    elif structure_score >= 70:
        strengths.append(
            "Good overall lesson structure with most key sections present."
        )

    # Learning objective strengths
    if objective_score >= 9:
        strengths.append(
            "Learning objectives are clear, measurable and well focused."
        )

    elif objective_score >= 7:
        strengths.append(
            "Learning objectives are generally clear and appropriate."
        )

    # Strong performance across both areas
    if structure_score >= 80 and objective_score >= 8:
        strengths.append(
            "The lesson demonstrates good alignment between its "
            "structure and learning objectives."
        )

    # If no strong areas were identified
    if not strengths:
        strengths.append(
            "The lesson provides a foundation that can be developed "
            "further through improvements to structure and objectives."
        )

    return strengths