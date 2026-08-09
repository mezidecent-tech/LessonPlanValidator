def calculate_grade(score):
    """
    Calculates lesson grade and teaching readiness.
    """

    if score >= 90:
        return (
            "A+",
            "★★★★★",
            "Ready for Classroom Delivery"
        )

    elif score >= 80:
        return (
            "A",
            "★★★★☆",
            "Ready for Classroom Delivery"
        )

    elif score >= 70:
        return (
            "B",
            "★★★★☆",
            "Ready with Minor Improvements"
        )

    elif score >= 60:
        return (
            "C",
            "★★★☆☆",
            "Needs Improvement Before Delivery"
        )

    elif score >= 50:
        return (
            "D",
            "★★☆☆☆",
            "Requires Significant Improvement"
        )

    else:
        return (
            "F",
            "★☆☆☆☆",
            "Not Ready for Classroom Delivery"
        )