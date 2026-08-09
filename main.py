from recommendations import recommend_learning_objectives
from strengths import identify_strengths
from section_quality import analyze_section_quality
from intelligent_quality import analyze_intelligent_quality
from section_recommendations import generate_section_recommendations
from section_extractor import extract_section
from scoring import score_learning_objectives
from reader import read_document
from validator import validate_structure
from report import generate_report
from template_manager import load_template
from metadata_extractor import extract_metadata

# Version 1 Alignment System
from alignment import (
    check_lesson_alignment,
    print_alignment_report
)


# ==================================================
# HELPER FUNCTION
# ==================================================

def extract_alignment_section(
    lesson_text,
    start_headings,
    end_headings
):
    """
    Extract a lesson-plan section for the alignment system.

    The section extractor returns a dictionary containing:
        status
        content

    This function keeps that structure intact so the
    alignment system can work with Present, Empty and
    Missing sections safely.
    """

    return extract_section(
        lesson_text,
        start_headings,
        end_headings
    )


# ==================================================
# PROGRAM HEADER
# ==================================================

print("=" * 50)
print("      AI LESSON PLAN VALIDATOR PRO")
print("=" * 50)


# ==================================================
# TEMPLATE SELECTION
# ==================================================

print("\nAvailable Templates")
print("1. Cambridge")

choice = input("\nChoose template (1): ")

if choice == "1":
    template = "cambridge"
else:
    print("Invalid choice.")
    exit()


sections = load_template(template)


# ==================================================
# LESSON PLAN
# ==================================================

filename = "sample_lesson.docx"

lesson_text = read_document(
    f"uploads/{filename}"
)


# ==================================================
# EXTRACT METADATA
# ==================================================

metadata = extract_metadata(
    lesson_text
)


# ==================================================
# EXTRACT LEARNING OBJECTIVES
# ==================================================

learning_objectives = extract_section(
    lesson_text,
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


# ==================================================
# DEBUG LEARNING OBJECTIVES
# ==================================================

print("\n========== DEBUG OBJECTIVES ==========")
print(learning_objectives)
print("======================================")


# ==================================================
# SCORE LEARNING OBJECTIVES
# ==================================================

objective_score, objective_feedback = (
    score_learning_objectives(
        learning_objectives
    )
)


print("\n" + "=" * 40)
print("LEARNING OBJECTIVE SCORE")
print("=" * 40)

print(
    f"Score: {objective_score}/10"
)

print("\nFeedback:")

for item in objective_feedback:
    print(
        f"• {item}"
    )


# ==================================================
# VALIDATE LESSON STRUCTURE
# ==================================================

results, structure_score = validate_structure(
    lesson_text,
    sections
)


# ==================================================
# BASIC SECTION QUALITY
# ==================================================

section_analysis = analyze_section_quality(
    results
)


# ==================================================
# INTELLIGENT SECTION QUALITY
# ==================================================

intelligent_analysis = analyze_intelligent_quality(
    lesson_text,
    results
)


print("\n" + "=" * 40)
print("INTELLIGENT SECTION QUALITY")
print("=" * 40)


for section, information in intelligent_analysis.items():

    status = information["status"]
    score = information["score"]

    if status == "Strong":
        symbol = "🟢"

    elif status == "Needs Improvement":
        symbol = "🟡"

    elif status == "Missing":
        symbol = "🔴"

    elif status == "Empty":
        symbol = "🟡"

    else:
        symbol = "🔵"

    print(
        f"{symbol} {section}: "
        f"{status} ({score}%)"
    )

    print(
        f"   {information['feedback']}"
    )


# ==================================================
# OBJECTIVE ALIGNMENT SECTIONS
# ==================================================

success_criteria = extract_alignment_section(
    lesson_text,
    [
        "success criteria",
        "success criterion",
        "success criteria:"
    ],
    [
        "starter",
        "main activity",
        "plenary",
        "resources",
        "assessment",
        "afl",
        "assessment for learning",
        "homework",
        "differentiation"
    ]
)


main_activity = extract_alignment_section(
    lesson_text,
    [
        "main activity",
        "main activities",
        "development",
        "lesson development"
    ],
    [
        "plenary",
        "resources",
        "assessment",
        "assessment / afl",
        "afl",
        "assessment for learning",
        "homework",
        "differentiation"
    ]
)


assessment = extract_alignment_section(
    lesson_text,
    [
        "assessment",
        "assessment:",
        "formal assessment",
        "summative assessment"
    ],
    [
        "afl",
        "assessment for learning",
        "assessment for learning (afl)",
        "homework",
        "differentiation",
        "reflection"
    ]
)


afl = extract_alignment_section(
    lesson_text,
    [
        "afl",
        "afl:",
        "assessment for learning",
        "assessment for learning (afl)"
    ],
    [
        "homework",
        "differentiation",
        "reflection",
        "teacher reflection",
        "resources"
    ]
)


# ==================================================
# DEBUG ALIGNMENT SECTIONS
# ==================================================

print("\n========== DEBUG ALIGNMENT SECTIONS ==========")

print("\nLearning Objectives:")
print(learning_objectives)

print("\nSuccess Criteria:")
print(success_criteria)

print("\nMain Activity:")
print(main_activity)

print("\nAssessment:")
print(assessment)

print("\nAFL:")
print(afl)

print("==============================================")


# ==================================================
# OBJECTIVE ALIGNMENT
# ==================================================

alignment_results, alignment_score = (
    check_lesson_alignment(
        learning_objectives,
        success_criteria,
        main_activity,
        assessment,
        afl
    )
)


# ==================================================
# PRINT ALIGNMENT REPORT
# ==================================================

print_alignment_report(
    alignment_results,
    alignment_score
)


# ==================================================
# IDENTIFY STRENGTHS
# ==================================================

strengths = identify_strengths(
    structure_score,
    objective_score
)


print("\n" + "=" * 40)
print("LESSON STRENGTHS")
print("=" * 40)


for strength in strengths:
    print(
        f"✔ {strength}"
    )


# ==================================================
# LESSON PLAN INFORMATION
# ==================================================

print("\n" + "=" * 40)
print("LESSON PLAN INFORMATION")
print("=" * 40)


for key, value in metadata.items():
    print(
        f"{key}: {value}"
    )


# ==================================================
# GENERAL RECOMMENDATIONS
# ==================================================

recommendations = recommend_learning_objectives(
    objective_score
)


# ==================================================
# SECTION-SPECIFIC RECOMMENDATIONS
# ==================================================

section_recommendations = (
    generate_section_recommendations(
        intelligent_analysis
    )
)


# ==================================================
# AI RECOMMENDATIONS
# ==================================================

print("\n" + "=" * 40)
print("AI RECOMMENDATIONS")
print("=" * 40)


if recommendations:

    for recommendation in recommendations:

        print(
            f"• {recommendation}"
        )

else:

    print(
        "No general recommendations."
    )


# ==================================================
# SECTION-SPECIFIC IMPROVEMENT PLAN
# ==================================================

print("\n" + "=" * 40)
print("SECTION-SPECIFIC IMPROVEMENT PLAN")
print("=" * 40)


if section_recommendations:

    for recommendation in section_recommendations:

        print(
            f"• {recommendation}"
        )

else:

    print(
        "No section-specific improvements required."
    )


# ==================================================
# GENERATE PROFESSIONAL REPORT
# ==================================================

generate_report(
    metadata,
    structure_score,
    objective_score,
    strengths,
    recommendations,
    section_analysis,
    intelligent_analysis,
    section_recommendations,
    filename
)


# ==================================================
# COMPLETION
# ==================================================

print("\n" + "=" * 50)
print("Validation Completed Successfully!")
print("=" * 50)