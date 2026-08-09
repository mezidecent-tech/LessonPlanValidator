def generate_section_recommendations(intelligent_analysis):
    """
    Generate specific recommendations for lesson-plan sections
    based on their intelligent quality analysis.

    Handles:
        - Missing sections
        - Empty sections
        - Sections needing improvement
    """

    recommendations = []

    recommendation_map = {

        "Learning Objectives": {

            "Empty":
                "The Learning Objectives heading is present but empty. "
                "Add clear, measurable learning objectives using action "
                "verbs such as identify, explain, calculate, compare, "
                "analyse, evaluate, create, or solve.",

            "Needs Improvement":
                "Make the learning objectives more specific and measurable. "
                "Use clear action verbs such as identify, explain, calculate, "
                "compare, analyse, evaluate, create, or solve.",

            "Missing":
                "Add clear learning objectives that describe what learners "
                "should know, understand, or be able to do by the end of the lesson."
        },


        "Success Criteria": {

            "Empty":
                "The Success Criteria heading is present but empty. "
                "Add learner-friendly and measurable success criteria, "
                "preferably using statements such as 'I can...'.",

            "Needs Improvement":
                "Make the success criteria learner-friendly and measurable. "
                "Consider using statements such as 'I can...' to show learners "
                "what successful learning looks like.",

            "Missing":
                "Add success criteria so learners can clearly understand "
                "what they need to achieve by the end of the lesson."
        },


        "Assessment": {

            "Empty":
                "The Assessment heading is present but empty. "
                "Add specific opportunities for checking learner understanding, "
                "such as questioning, observation, peer assessment, "
                "self-assessment, quizzes, or an exit ticket.",

            "Needs Improvement":
                "Strengthen assessment by including specific formative "
                "assessment strategies such as questioning, observation, "
                "peer assessment, self-assessment, quizzes, or an exit ticket.",

            "Missing":
                "Add assessment opportunities that allow the teacher to "
                "check whether learners have achieved the learning objectives."
        },


        "Differentiation": {

            "Empty":
                "The Differentiation heading is present but empty. "
                "Add specific strategies for supporting different learner "
                "needs, including scaffolding, SEN support, extension, "
                "challenge tasks, or targeted intervention.",

            "Needs Improvement":
                "Add specific differentiation strategies, such as scaffolding, "
                "additional support, extension activities, challenge tasks, "
                "or targeted support for learners who need it.",

            "Missing":
                "Add differentiation strategies showing how the lesson will "
                "support learners with different levels of ability and need."
        },


        "Resources": {

            "Empty":
                "The Resources heading is present but empty. "
                "List the resources required for the lesson, such as "
                "worksheets, textbooks, manipulatives, technology, "
                "visual aids, or presentation materials.",

            "Needs Improvement":
                "Specify the teaching and learning resources required for "
                "the lesson, such as worksheets, textbooks, manipulatives, "
                "technology, visual aids, or presentation materials.",

            "Missing":
                "Add a resources section identifying the materials and "
                "equipment needed to deliver the lesson."
        },


        "Starter": {

            "Missing":
                "Add a short starter activity that activates prior knowledge, "
                "engages learners, and prepares them for the main lesson."
        },


        "Main Activity": {

            "Missing":
                "Add a clear main learning activity explaining what the "
                "teacher and learners will do during the main part of the lesson."
        },


        "Plenary": {

            "Missing":
                "Add a short plenary or closing activity that allows learners "
                "to review, reflect on, or demonstrate what they have learned."
        },


        "Homework": {

            "Empty":
                "The Homework heading is present but empty. "
                "Add an appropriate homework or follow-up activity "
                "that reinforces the learning from the lesson.",

            "Missing":
                "Consider adding an appropriate homework or follow-up activity "
                "that reinforces the learning from the lesson."
        },


        "Topic": {

            "Missing":
                "Add the lesson topic or unit so the focus of the lesson "
                "is immediately clear."
        },


        "Subject": {

            "Missing":
                "Add the subject so the lesson can be clearly identified "
                "within the wider curriculum."
        },


        "Year": {

            "Missing":
                "Add the year group, grade, or class level so the lesson "
                "can be matched to the intended learners."
        }
    }


    # --------------------------------------------------
    # Generate recommendations
    # --------------------------------------------------

    for section, information in intelligent_analysis.items():

        status = information.get("status", "Missing")

        if section not in recommendation_map:
            continue

        section_rules = recommendation_map[section]

        if status in section_rules:

            recommendations.append(
                f"{section}: "
                f"{section_rules[status]}"
            )


    return recommendations