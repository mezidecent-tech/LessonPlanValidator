def recommend_learning_objectives(score):

    if score >= 9:

        return [
            "Excellent learning objectives.",
            "Consider adding one higher-order thinking objective using verbs like 'analyse' or 'evaluate'."
        ]

    elif score >= 7:

        return [
            "Good learning objectives.",
            "Consider making every objective measurable.",
            "Include one application objective."
        ]

    elif score >= 5:

        return [
            "Rewrite weak objectives using measurable action verbs.",
            "Avoid vague verbs such as 'understand' and 'know'.",
            "Add at least two learning objectives."
        ]

    else:

        return [
            "Learning objectives require significant improvement.",
            "Rewrite every objective using Bloom's measurable verbs.",
            "Ensure objectives align with the lesson activities."
        ]