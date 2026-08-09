import re


# ============================================================
# VERSION 1
# LESSON PLAN OBJECTIVE ALIGNMENT
# ============================================================
#
# This module checks alignment between:
#
# Learning Objectives
#        ↓
# Success Criteria
#        ↓
# Main Activity
#        ↓
# Assessment
#
# AFL is checked separately.
#
# ============================================================


# ============================================================
# KEY CONCEPT GROUPS
# ============================================================

CONCEPT_GROUPS = {

    "perimeter": [
        "perimeter",
        "boundary",
        "distance around",
        "around the shape"
    ],

    "measure": [
        "measure",
        "measuring",
        "measurement",
        "length",
        "width",
        "side",
        "sides"
    ],

    "calculate": [
        "calculate",
        "calculation",
        "work out",
        "find",
        "solve",
        "add",
        "addition"
    ],

    "rectangle": [
        "rectangle",
        "rectangles"
    ],

    "square": [
        "square",
        "squares"
    ],

    "area": [
        "area",
        "surface"
    ],

    "fraction": [
        "fraction",
        "fractions"
    ],

    "decimal": [
        "decimal",
        "decimals"
    ],

    "multiplication": [
        "multiply",
        "multiplication",
        "times"
    ],

    "division": [
        "divide",
        "division",
        "sharing"
    ]
}


# ============================================================
# ASSESSMENT STRATEGIES
# ============================================================

ASSESSMENT_STRATEGIES = {

    "worksheet": [
        "worksheet",
        "worksheets"
    ],

    "quiz": [
        "quiz",
        "quizzes"
    ],

    "test": [
        "test",
        "tests"
    ],

    "exercise": [
        "exercise",
        "exercises"
    ],

    "written task": [
        "written task",
        "written tasks"
    ],

    "classwork": [
        "classwork",
        "class work"
    ],

    "independent task": [
        "independent task",
        "independent work"
    ],

    "problem solving task": [
        "problem solving",
        "problem-solving"
    ],

    "exit ticket": [
        "exit ticket",
        "exit tickets"
    ],

    "practical task": [
        "practical task",
        "practical activity"
    ]
}


# ============================================================
# AFL STRATEGIES
# ============================================================

AFL_STRATEGIES = {

    "questioning": [
        "questioning",
        "question",
        "questions",
        "oral questions"
    ],

    "observation": [
        "observation",
        "observe",
        "observing"
    ],

    "checking understanding": [
        "checking understanding",
        "check understanding",
        "check for understanding",
        "checking for understanding"
    ],

    "discussion": [
        "discussion",
        "class discussion",
        "group discussion"
    ],

    "peer assessment": [
        "peer assessment",
        "peer-assessment",
        "peer review"
    ],

    "self assessment": [
        "self assessment",
        "self-assessment",
        "self assessment"
    ],

    "thumbs up/down": [
        "thumbs up",
        "thumbs down",
        "thumbs up/down"
    ],

    "mini whiteboards": [
        "mini whiteboard",
        "mini whiteboards",
        "whiteboard responses"
    ],

    "traffic lights": [
        "traffic light",
        "traffic lights"
    ]
}


# ============================================================
# FIND CONCEPTS IN TEXT
# ============================================================

def find_concepts(text):

    if not text:
        return set()

    # Handle dictionaries returned by section extractor
    if isinstance(text, dict):

        status = text.get("status", "")

        content = text.get("content", [])

        if status in ["Empty", "Missing"]:

            return set()

        if isinstance(content, list):

            text = " ".join(
                str(item)
                for item in content
            )

        else:

            text = str(content)

    # Handle lists
    elif isinstance(text, list):

        text = " ".join(
            str(item)
            for item in text
        )

    else:

        text = str(text)

    text = text.lower()

    found = set()

    for concept, keywords in CONCEPT_GROUPS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                found.add(concept)

                break

    return found


# ============================================================
# FIND ASSESSMENT STRATEGIES
# ============================================================

def find_assessment_strategies(text):

    if not text:
        return []

    if isinstance(text, dict):

        content = text.get("content", [])

        if isinstance(content, list):

            text = " ".join(
                str(item)
                for item in content
            )

        else:

            text = str(content)

    elif isinstance(text, list):

        text = " ".join(
            str(item)
            for item in text
        )

    else:

        text = str(text)

    text = text.lower()

    found = []

    for strategy, keywords in ASSESSMENT_STRATEGIES.items():

        for keyword in keywords:

            if keyword.lower() in text:

                found.append(strategy)

                break

    return sorted(set(found))


# ============================================================
# FIND AFL STRATEGIES
# ============================================================

def find_afl_strategies(text):

    if not text:
        return []

    if isinstance(text, dict):

        content = text.get("content", [])

        if isinstance(content, list):

            text = " ".join(
                str(item)
                for item in content
            )

        else:

            text = str(content)

    elif isinstance(text, list):

        text = " ".join(
            str(item)
            for item in text
        )

    else:

        text = str(text)

    text = text.lower()

    found = []

    for strategy, keywords in AFL_STRATEGIES.items():

        for keyword in keywords:

            if keyword.lower() in text:

                found.append(strategy)

                break

    return sorted(set(found))


# ============================================================
# GET TEXT FROM SECTION
# ============================================================

def get_section_text(section):

    if not section:
        return ""

    if isinstance(section, dict):

        status = section.get("status", "")

        if status in ["Empty", "Missing"]:

            return ""

        content = section.get("content", [])

        if isinstance(content, list):

            return " ".join(
                str(item)
                for item in content
            )

        return str(content)

    if isinstance(section, list):

        return " ".join(
            str(item)
            for item in section
        )

    return str(section)


# ============================================================
# CHECK IF SECTION IS EMPTY OR MISSING
# ============================================================

def section_is_empty(section):

    if not section:
        return True

    if isinstance(section, dict):

        status = section.get("status", "")

        if status in ["Empty", "Missing"]:
            return True

        content = section.get("content", [])

        if not content:
            return True

        if isinstance(content, list):

            return not any(
                str(item).strip()
                for item in content
            )

        return not str(content).strip()

    if isinstance(section, list):

        return not any(
            str(item).strip()
            for item in section
        )

    return not str(section).strip()


# ============================================================
# CHECK ALIGNMENT BETWEEN TWO SECTIONS
# ============================================================

def check_alignment(
    objectives,
    target_section,
    section_name=""
):

    objective_concepts = find_concepts(
        objectives
    )

    target_concepts = find_concepts(
        target_section
    )

    # --------------------------------------------------------
    # OBJECTIVES NOT FOUND
    # --------------------------------------------------------

    if not objective_concepts:

        return {

            "status": "Unable to assess",

            "score": 0,

            "matched": [],

            "missing": [],

            "strategies": [],

            "quality": "Learning objectives could not be identified."

        }

    # --------------------------------------------------------
    # TARGET SECTION EMPTY OR MISSING
    # --------------------------------------------------------

    if section_is_empty(target_section):

        return {

            "status": "Missing",

            "score": 0,

            "matched": [],

            "missing": sorted(objective_concepts),

            "strategies": [],

            "quality": (
                f"{section_name} is empty or missing."
            )

        }

    # --------------------------------------------------------
    # MATCH CONCEPTS
    # --------------------------------------------------------

    matched = objective_concepts.intersection(
        target_concepts
    )

    missing = objective_concepts.difference(
        target_concepts
    )

    percentage = round(
        (
            len(matched)
            /
            len(objective_concepts)
        ) * 100
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if percentage >= 70:

        status = "Strong"

    elif percentage >= 40:

        status = "Needs Improvement"

    else:

        status = "Weak"

    return {

        "status": status,

        "score": percentage,

        "matched": sorted(matched),

        "missing": sorted(missing),

        "strategies": [],

        "quality": (
            f"{section_name} contains "
            f"sufficiently relevant content."
        )

    }


# ============================================================
# ASSESSMENT QUALITY CHECK
# ============================================================

def check_assessment_quality(
    assessment,
    objectives
):

    # --------------------------------------------------------
    # EMPTY ASSESSMENT
    # --------------------------------------------------------

    if section_is_empty(assessment):

        return {

            "quality_status": "Missing",

            "quality_score": 0,

            "strategies": [],

            "feedback": (
                "Assessment is empty or missing."
            )

        }

    assessment_text = get_section_text(
        assessment
    )

    strategies = find_assessment_strategies(
        assessment_text
    )

    objective_concepts = find_concepts(
        objectives
    )

    assessment_concepts = find_concepts(
        assessment_text
    )

    # --------------------------------------------------------
    # CHECK OBJECTIVE COVERAGE
    # --------------------------------------------------------

    if objective_concepts:

        matched = objective_concepts.intersection(
            assessment_concepts
        )

        coverage = round(
            (
                len(matched)
                /
                len(objective_concepts)
            ) * 100
        )

    else:

        coverage = 0

    # --------------------------------------------------------
    # SPECIFICITY INDICATORS
    # --------------------------------------------------------

    specificity_words = [

        "complete",
        "calculate",
        "measure",
        "identify",
        "solve",
        "compare",
        "explain",
        "demonstrate",
        "write",
        "draw",
        "show",
        "answer",
        "record",
        "submit"
    ]

    lower_text = assessment_text.lower()

    specificity_count = sum(

        1
        for word in specificity_words
        if word in lower_text

    )

    # --------------------------------------------------------
    # SCORE QUALITY
    # --------------------------------------------------------

    quality_score = 0

    if strategies:

        quality_score += 30

    if coverage >= 70:

        quality_score += 50

    elif coverage >= 40:

        quality_score += 30

    elif coverage > 0:

        quality_score += 15

    if specificity_count >= 2:

        quality_score += 20

    elif specificity_count == 1:

        quality_score += 10

    quality_score = min(
        quality_score,
        100
    )

    # --------------------------------------------------------
    # QUALITY STATUS
    # --------------------------------------------------------

    if quality_score >= 80:

        quality_status = "Strong"

        feedback = (
            "Assessment is specific, measurable "
            "and aligned with the learning objectives."
        )

    elif quality_score >= 50:

        quality_status = "Needs Improvement"

        feedback = (
            "Assessment is present but could be "
            "more specific and better aligned with "
            "the learning objectives."
        )

    else:

        quality_status = "Weak"

        feedback = (
            "Assessment is too vague or does not "
            "clearly measure the learning objectives."
        )

    return {

        "quality_status": quality_status,

        "quality_score": quality_score,

        "strategies": strategies,

        "feedback": feedback

    }


# ============================================================
# CHECK AFL SEPARATELY
# ============================================================

def check_afl(afl):

    # --------------------------------------------------------
    # AFL MISSING
    # --------------------------------------------------------

    if section_is_empty(afl):

        return {

            "status": "Missing",

            "score": 0,

            "strategies": [],

            "feedback": (
                "AFL is empty or missing."
            )

        }

    strategies = find_afl_strategies(
        afl
    )

    # --------------------------------------------------------
    # AFL STRATEGIES FOUND
    # --------------------------------------------------------

    if strategies:

        if len(strategies) >= 2:

            status = "Strong"

            score = 100

            feedback = (
                "AFL strategies identified successfully."
            )

        else:

            status = "Needs Improvement"

            score = 70

            feedback = (
                "AFL is present but could include "
                "more specific formative assessment strategies."
            )

    # --------------------------------------------------------
    # AFL PRESENT BUT NOT RECOGNIZED
    # --------------------------------------------------------

    else:

        status = "Needs Improvement"

        score = 40

        feedback = (
            "AFL is present, but no recognised "
            "AFL strategy was identified."
        )

    return {

        "status": status,

        "score": score,

        "strategies": strategies,

        "feedback": feedback

    }


# ============================================================
# COMPLETE LESSON ALIGNMENT
# ============================================================

def check_lesson_alignment(
    learning_objectives,
    success_criteria,
    main_activity,
    assessment,
    afl
):

    results = {}

    # --------------------------------------------------------
    # SUCCESS CRITERIA
    # --------------------------------------------------------

    results["Success Criteria"] = check_alignment(

        learning_objectives,

        success_criteria,

        "Success Criteria"

    )

    # --------------------------------------------------------
    # MAIN ACTIVITY
    # --------------------------------------------------------

    results["Main Activity"] = check_alignment(

        learning_objectives,

        main_activity,

        "Main Activity"

    )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    assessment_result = check_alignment(

        learning_objectives,

        assessment,

        "Assessment"

    )

    assessment_quality = check_assessment_quality(

        assessment,

        learning_objectives

    )

    assessment_result["strategies"] = (
        assessment_quality["strategies"]
    )

    assessment_result["quality_status"] = (
        assessment_quality["quality_status"]
    )

    assessment_result["quality_score"] = (
        assessment_quality["quality_score"]
    )

    assessment_result["quality_feedback"] = (
        assessment_quality["feedback"]
    )

    results["Assessment"] = assessment_result

    # --------------------------------------------------------
    # AFL
    # --------------------------------------------------------

    results["AFL"] = check_afl(
        afl
    )

    # --------------------------------------------------------
    # OVERALL ALIGNMENT SCORE
    #
    # AFL is NOT included in this calculation.
    #
    # This prevents AFL from lowering the objective
    # alignment score because AFL is formative support,
    # not the same thing as objective assessment.
    # --------------------------------------------------------

    alignment_scores = [

        result["score"]

        for section, result in results.items()

        if section != "AFL"

        and result["status"] != "Unable to assess"

    ]

    if alignment_scores:

        overall_score = round(

            sum(alignment_scores)
            /
            len(alignment_scores)

        )

    else:

        overall_score = 0

    return results, overall_score


# ============================================================
# DISPLAY ALIGNMENT REPORT
# ============================================================

def print_alignment_report(
    results,
    overall_score
):

    print("\n")

    print("=" * 40)

    print("OBJECTIVE ALIGNMENT")

    print("=" * 40)

    # --------------------------------------------------------
    # OBJECTIVE ALIGNMENT RESULTS
    # --------------------------------------------------------

    for section, result in results.items():

        status = result.get(
            "status",
            "Unable to assess"
        )

        score = result.get(
            "score",
            0
        )

        # ----------------------------------------------------
        # AFL
        # ----------------------------------------------------

        if section == "AFL":

            if status == "Strong":

                icon = "🟢"

            elif status == "Needs Improvement":

                icon = "🟡"

            elif status == "Missing":

                icon = "🔴"

            else:

                icon = "⚪"

            print()

            print(
                f"{icon} AFL: "
                f"{status} ({score}%)"
            )

            print(
                "   "
                + result.get(
                    "feedback",
                    ""
                )
            )

            strategies = result.get(
                "strategies",
                []
            )

            if strategies:

                print(
                    "   AFL strategies identified: "
                    +
                    ", ".join(strategies)
                )

            continue

        # ----------------------------------------------------
        # STANDARD ALIGNMENT
        # ----------------------------------------------------

        if status == "Strong":

            icon = "🟢"

        elif status == "Needs Improvement":

            icon = "🟡"

        elif status == "Weak":

            icon = "🔴"

        elif status == "Missing":

            icon = "⚪"

        else:

            icon = "⚪"

        print()

        print(
            f"{icon} Learning Objectives ↔ "
            f"{section}: "
            f"{status} ({score}%)"
        )

        # ----------------------------------------------------
        # MATCHED CONCEPTS
        # ----------------------------------------------------

        matched = result.get(
            "matched",
            []
        )

        if matched:

            print(
                "   Matched concepts: "
                +
                ", ".join(matched)
            )

        # ----------------------------------------------------
        # MISSING CONCEPTS
        # ----------------------------------------------------

        missing = result.get(
            "missing",
            []
        )

        if missing:

            print(
                "   Missing concepts: "
                +
                ", ".join(missing)
            )

        # ----------------------------------------------------
        # ASSESSMENT STRATEGIES
        # ----------------------------------------------------

        if section == "Assessment":

            strategies = result.get(
                "strategies",
                []
            )

            if strategies:

                print(
                    "   Assessment strategies identified: "
                    +
                    ", ".join(strategies)
                )

            # ------------------------------------------------
            # ASSESSMENT QUALITY
            # ------------------------------------------------

            quality_status = result.get(
                "quality_status"
            )

            quality_score = result.get(
                "quality_score"
            )

            quality_feedback = result.get(
                "quality_feedback"
            )

            if quality_status:

                print(
                    "   Assessment quality: "
                    f"{quality_status} "
                    f"({quality_score}%)"
                )

                if quality_feedback:

                    print(
                        "   "
                        +
                        quality_feedback
                    )

        # ----------------------------------------------------
        # MISSING SECTION MESSAGE
        # ----------------------------------------------------

        quality = result.get(
            "quality"
        )

        if quality:

            if status in [
                "Missing",
                "Unable to assess"
            ]:

                print(
                    "   "
                    +
                    quality
                )

    # --------------------------------------------------------
    # OVERALL SCORE
    # --------------------------------------------------------

    print()

    print(
        f"Overall Alignment Score: "
        f"{overall_score}%"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    objectives = """
    To measure and calculate the perimeter
    of a rectangle and square.
    """

    success_criteria = """
    I can calculate the perimeter of a rectangle
    and square by counting the sides on a grid.

    I can calculate the perimeter by adding
    the length of the sides.

    I can find the perimeter of a rectangle systematically.
    """

    main_activity = """
    Learners measure the sides of rectangles
    and squares and calculate their perimeter.
    """

    assessment = """
    Learners complete a worksheet where they
    measure side lengths and calculate the
    perimeter of rectangles and squares.
    """

    afl = """
    Teacher uses questioning, observation and
    checking understanding throughout the lesson.
    """

    results, overall_score = check_lesson_alignment(

        objectives,

        success_criteria,

        main_activity,

        assessment,

        afl

    )

    print_alignment_report(

        results,

        overall_score

    )