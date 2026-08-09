import streamlit as st
import os
import tempfile

from reader import read_document
from validator import validate_structure
from template_manager import load_template
from metadata_extractor import extract_metadata
from section_extractor import extract_section
from scoring import score_learning_objectives
from section_quality import analyze_section_quality
from intelligent_quality import analyze_intelligent_quality
from strengths import identify_strengths
from recommendations import recommend_learning_objectives
from section_recommendations import generate_section_recommendations
from alignment import check_lesson_alignment
from report import generate_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Lesson Plan Validator",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📚 AI Lesson Plan Validator")
st.subheader("Teacher Review Interface")

st.write(
    "Upload your lesson plan to check its structure, "
    "learning objectives, alignment, assessment, AFL, "
    "and areas for improvement."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Lesson Plan Settings")

    template_choice = st.selectbox(
        "Select Curriculum Template",
        ["Cambridge"]
    )

    st.info(
        "This version uses the existing V1 validation engine."
    )


# ============================================================
# FILE UPLOAD
# ============================================================

st.header("📄 Upload Lesson Plan")

uploaded_file = st.file_uploader(
    "Choose a Word document (.docx)",
    type=["docx"]
)


# ============================================================
# VALIDATION
# ============================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Validate Lesson Plan",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Analysing lesson plan..."
        ):

            try:

                # ------------------------------------------------
                # CREATE TEMPORARY FILE
                # ------------------------------------------------

                temp_dir = tempfile.mkdtemp()

                temp_path = os.path.join(
                    temp_dir,
                    uploaded_file.name
                )

                with open(
                    temp_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                # ------------------------------------------------
                # LOAD TEMPLATE
                # ------------------------------------------------

                template = load_template(
                    template_choice.lower()
                )

                # ------------------------------------------------
                # READ DOCUMENT
                # ------------------------------------------------

                lesson_text = read_document(
                    temp_path
                )

                # ------------------------------------------------
                # METADATA
                # ------------------------------------------------

                metadata = extract_metadata(
                    lesson_text
                )

                # ------------------------------------------------
                # LEARNING OBJECTIVES
                # ------------------------------------------------

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

                # ------------------------------------------------
                # SCORE OBJECTIVES
                # ------------------------------------------------

                (
                    objective_score,
                    objective_feedback
                ) = score_learning_objectives(
                    learning_objectives
                )

                # ------------------------------------------------
                # VALIDATE STRUCTURE
                # ------------------------------------------------

                results, structure_score = (
                    validate_structure(
                        lesson_text,
                        template
                    )
                )

                # ------------------------------------------------
                # SECTION QUALITY
                # ------------------------------------------------

                section_analysis = (
                    analyze_section_quality(
                        results
                    )
                )

                # ------------------------------------------------
                # INTELLIGENT QUALITY
                # ------------------------------------------------

                intelligent_analysis = (
                    analyze_intelligent_quality(
                        lesson_text,
                        results
                    )
                )

                # ------------------------------------------------
                # STRENGTHS
                # ------------------------------------------------

                strengths = identify_strengths(
                    structure_score,
                    objective_score
                )

                # ------------------------------------------------
                # RECOMMENDATIONS
                # ------------------------------------------------

                recommendations = (
                    recommend_learning_objectives(
                        objective_score
                    )
                )

                # ------------------------------------------------
                # SECTION RECOMMENDATIONS
                # ------------------------------------------------

                section_recommendations = (
                    generate_section_recommendations(
                        intelligent_analysis
                    )
                )

                # ------------------------------------------------
                # ALIGNMENT SECTIONS
                # ------------------------------------------------

                success_criteria = extract_section(
                    lesson_text,
                    ["success criteria"],
                    ["starter", "main activity"]
                )

                main_activity = extract_section(
                    lesson_text,
                    ["main activity"],
                    ["plenary", "resources", "assessment", "afl"]
                )

                assessment = extract_section(
                    lesson_text,
                    ["assessment"],
                    [
                        "afl",
                        "assessment for learning",
                        "homework",
                        "differentiation"
                    ]
                )

                afl = extract_section(
                    lesson_text,
                    [
                        "afl",
                        "assessment for learning",
                        "assessment for learning (afl)"
                    ],
                    [
                        "homework",
                        "differentiation",
                        "resources"
                    ]
                )

                # ------------------------------------------------
                # ALIGNMENT
                # ------------------------------------------------

                (
                    alignment_results,
                    alignment_score
                ) = check_lesson_alignment(
                    learning_objectives,
                    success_criteria,
                    main_activity,
                    assessment,
                    afl
                )

                # ------------------------------------------------
                # STORE RESULTS
                # ------------------------------------------------

                st.session_state["validated"] = True

                st.session_state["metadata"] = metadata

                st.session_state["structure_score"] = (
                    structure_score
                )

                st.session_state["objective_score"] = (
                    objective_score
                )

                st.session_state["objective_feedback"] = (
                    objective_feedback
                )

                st.session_state["intelligent_analysis"] = (
                    intelligent_analysis
                )

                st.session_state["strengths"] = strengths

                st.session_state["recommendations"] = (
                    recommendations
                )

                st.session_state[
                    "section_recommendations"
                ] = section_recommendations

                st.session_state[
                    "alignment_results"
                ] = alignment_results

                st.session_state[
                    "alignment_score"
                ] = alignment_score

                st.session_state[
                    "section_analysis"
                ] = section_analysis

                st.session_state[
                    "lesson_filename"
                ] = uploaded_file.name

                st.session_state[
                    "lesson_text"
                ] = lesson_text

                st.success(
                    "Lesson plan validated successfully!"
                )

            except Exception as error:

                st.error(
                    "An error occurred while validating "
                    "the lesson plan."
                )

                st.exception(error)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.get(
    "validated",
    False
):

    st.divider()

    st.header("📊 Validation Results")

    # --------------------------------------------------------
    # SCORE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Structure Score",
            f"{st.session_state['structure_score']}%"
        )

    with col2:

        st.metric(
            "Learning Objective Score",
            f"{st.session_state['objective_score']}/10"
        )

    with col3:

        st.metric(
            "Overall Alignment",
            f"{st.session_state['alignment_score']}%"
        )

    # ========================================================
    # LESSON INFORMATION
    # ========================================================

    st.divider()

    st.header("📋 Lesson Plan Information")

    metadata = st.session_state["metadata"]

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write(
            f"**Teacher:** {metadata.get('Teacher', 'Not Found')}"
        )

        st.write(
            f"**Subject:** {metadata.get('Subject', 'Not Found')}"
        )

        st.write(
            f"**Topic:** {metadata.get('Topic', 'Not Found')}"
        )

    with info_col2:

        st.write(
            f"**Year:** {metadata.get('Year', 'Not Found')}"
        )

        st.write(
            f"**Date:** {metadata.get('Date', 'Not Found')}"
        )

        st.write(
            f"**School:** {metadata.get('School', 'Not Found')}"
        )

    # ========================================================
    # SECTION QUALITY
    # ========================================================

    st.divider()

    st.header("📝 Section Quality")

    intelligent_analysis = (
        st.session_state[
            "intelligent_analysis"
        ]
    )

    for section, information in (
        intelligent_analysis.items()
    ):

        status = information["status"]

        score = information["score"]

        if status == "Strong":

            icon = "🟢"

        elif status == "Needs Improvement":

            icon = "🟡"

        elif status == "Empty":

            icon = "🟡"

        elif status == "Missing":

            icon = "🔴"

        else:

            icon = "🔵"

        st.write(
            f"{icon} **{section}:** "
            f"{status} ({score}%)"
        )

        st.caption(
            information["feedback"]
        )

    # ========================================================
    # OBJECTIVE FEEDBACK
    # ========================================================

    st.divider()

    st.header("🎯 Learning Objective Feedback")

    for feedback in (
        st.session_state[
            "objective_feedback"
        ]
    ):

        st.write(
            f"• {feedback}"
        )

    # ========================================================
    # OBJECTIVE ALIGNMENT
    # ========================================================

    st.divider()

    st.header("🔗 Objective Alignment")

    alignment_results = (
        st.session_state[
            "alignment_results"
        ]
    )

    for section, result in (
        alignment_results.items()
    ):

        status = result["status"]

        score = result["score"]

        if status == "Strong":

            icon = "🟢"

        elif status == "Needs Improvement":

            icon = "🟡"

        elif status == "Weak":

            icon = "🔴"

        elif status == "Missing":

            icon = "🔴"

        else:

            icon = "⚪"

        st.write(
            f"{icon} **Learning Objectives ↔ "
            f"{section}:** "
            f"{status} ({score}%)"
        )

        if result.get("matched"):

            st.caption(
                "Matched concepts: "
                + ", ".join(
                    result["matched"]
                )
            )

        if result.get("missing"):

            st.caption(
                "Missing concepts: "
                + ", ".join(
                    result["missing"]
                )
            )

        if result.get(
            "assessment_strategies"
        ):

            st.caption(
                "Assessment strategies: "
                + ", ".join(
                    result[
                        "assessment_strategies"
                    ]
                )
            )

        if result.get(
            "afl_strategies"
        ):

            st.caption(
                "AFL strategies: "
                + ", ".join(
                    result[
                        "afl_strategies"
                    ]
                )
            )

        if result.get(
            "quality_score"
        ) is not None:

            st.caption(
                f"Assessment quality: "
                f"{result['quality_score']}%"
            )

    # ========================================================
    # STRENGTHS
    # ========================================================

    st.divider()

    st.header("💪 Lesson Strengths")

    for strength in (
        st.session_state["strengths"]
    ):

        st.success(
            strength
        )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header("💡 Recommendations")

    recommendations = (
        st.session_state[
            "recommendations"
        ]
    )

    if recommendations:

        for recommendation in recommendations:

            st.warning(
                recommendation
            )

    else:

        st.success(
            "No major general recommendations."
        )

    # ========================================================
    # SECTION IMPROVEMENTS
    # ========================================================

    section_recommendations = (
        st.session_state[
            "section_recommendations"
        ]
    )

    if section_recommendations:

        st.divider()

        st.header(
            "🛠️ Section Improvement Plan"
        )

        for recommendation in (
            section_recommendations
        ):

            st.info(
                recommendation
            )

    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.divider()

    st.header("📥 Professional Report")

    st.write(
        "Your validated lesson plan can now be "
        "saved as a professional review report."
    )

    report_filename = (
        "Teacher_Review_"
        + os.path.splitext(
            st.session_state[
                "lesson_filename"
            ]
        )[0]
        + ".docx"
    )

    if st.button(
        "📄 Generate Professional Report",
        use_container_width=True
    ):

        try:

            # Create report directory

            report_dir = "reports"

            os.makedirs(
                report_dir,
                exist_ok=True
            )

            report_path = os.path.join(
                report_dir,
                report_filename
            )

            # Existing report generator

            generate_report(
                st.session_state["metadata"],
                st.session_state[
                    "structure_score"
                ],
                st.session_state[
                    "objective_score"
                ],
                st.session_state[
                    "strengths"
                ],
                st.session_state[
                    "recommendations"
                ],
                st.session_state[
                    "section_analysis"
                ],
                st.session_state[
                    "intelligent_analysis"
                ],
                st.session_state[
                    "section_recommendations"
                ],
                st.session_state[
                    "lesson_filename"
                ]
            )

            # Find generated report

            generated_path = os.path.join(
                report_dir,
                "Review_"
                + st.session_state[
                    "lesson_filename"
                ].replace(
                    ".docx",
                    ""
                )
                + ".docx"
            )

            if os.path.exists(
                generated_path
            ):

                with open(
                    generated_path,
                    "rb"
                ) as report_file:

                    st.download_button(
                        "⬇️ Download Report",
                        report_file,
                        file_name=report_filename,
                        mime=(
                            "application/"
                            "vnd.openxmlformats-officedocument"
                            ".wordprocessingml.document"
                        ),
                        use_container_width=True
                    )

            else:

                st.warning(
                    "The report was generated, but "
                    "the expected report file could "
                    "not be located."
                )

        except Exception as error:

            st.error(
                "Unable to generate the report."
            )

            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Lesson Plan Validator — Version 1 "
    "Teacher Interface"
)