import re


# --------------------------------------------------
# Additional headings that may appear in a lesson
# plan but are not currently scored as main sections.
# They are used as boundaries so one section does
# not accidentally absorb the next section.
# --------------------------------------------------

BOUNDARY_HEADINGS = [
    "vocabulary",
    "use of ta",
    "use of ta (or other adults)",
    "cross-curricular links",
    "evaluation",
    "key questions",
    "time",
    "lesson structure",
    "targeted students",
    "day",
    "lesson duration"
]


# --------------------------------------------------
# Equivalent headings
#
# These headings should count as one of the
# required/scored sections.
# --------------------------------------------------

SECTION_EQUIVALENTS = {

    "Assessment": [
        "afl",
        "afl strategies",
        "assessment opportunities",
        "formative assessment",
        "assessment for learning",
        "checking understanding",
        "checking for understanding",
        "evidence of learning"
    ]
}


def validate_structure(text, sections):

    results = {}
    score = 0

    print("\nChecking Lesson Plan...\n")

    lines = text.splitlines()

    # --------------------------------------------------
    # Clean a line
    # --------------------------------------------------

    def clean_line(line):

        return line.strip()

    # --------------------------------------------------
    # Get all candidates for a section
    #
    # This includes:
    # - normal section keywords
    # - equivalent headings
    # --------------------------------------------------

    def get_candidates(heading, keywords):

        candidates = [heading]

        candidates.extend(keywords)

        equivalents = SECTION_EQUIVALENTS.get(
            heading,
            []
        )

        candidates.extend(equivalents)

        # Remove duplicates
        candidates = list(
            dict.fromkeys(
                candidate.lower().strip()
                for candidate in candidates
            )
        )

        return candidates

    # --------------------------------------------------
    # Check whether a line matches a scored heading
    # --------------------------------------------------

    def match_scored_heading(
        line,
        heading,
        keywords
    ):

        clean = clean_line(line)

        if not clean:

            return None

        candidates = get_candidates(
            heading,
            keywords
        )

        for candidate_clean in candidates:

            # ------------------------------------------
            # Heading only
            #
            # Example:
            # Resources:
            # ------------------------------------------

            empty_pattern = (
                r"^\s*"
                + re.escape(candidate_clean)
                + r"\s*[:\-–—]\s*$"
            )

            if re.match(
                empty_pattern,
                clean,
                re.IGNORECASE
            ):

                return {
                    "matched": True,
                    "matched_heading": candidate_clean,
                    "inline_content": ""
                }

            # ------------------------------------------
            # Heading + content
            #
            # Example:
            # Assessment:
            # Students answer questions.
            # ------------------------------------------

            inline_pattern = (
                r"^\s*"
                + re.escape(candidate_clean)
                + r"\s*[:\-–—]\s*(.+?)\s*$"
            )

            match = re.match(
                inline_pattern,
                clean,
                re.IGNORECASE
            )

            if match:

                return {
                    "matched": True,
                    "matched_heading": candidate_clean,
                    "inline_content": match.group(1).strip()
                }

            # ------------------------------------------
            # Standalone heading
            # ------------------------------------------

            if clean.lower() == candidate_clean.lower():

                return {
                    "matched": True,
                    "matched_heading": candidate_clean,
                    "inline_content": ""
                }

        return None

    # --------------------------------------------------
    # Check whether a line is an additional boundary
    # --------------------------------------------------

    def is_boundary_heading(line):

        clean = clean_line(line)

        if not clean:

            return False

        for boundary in BOUNDARY_HEADINGS:

            boundary = boundary.strip()

            # ------------------------------------------
            # Heading only
            # ------------------------------------------

            empty_pattern = (
                r"^\s*"
                + re.escape(boundary)
                + r"\s*[:\-–—]\s*$"
            )

            if re.match(
                empty_pattern,
                clean,
                re.IGNORECASE
            ):

                return True

            # ------------------------------------------
            # Heading with content
            # ------------------------------------------

            inline_pattern = (
                r"^\s*"
                + re.escape(boundary)
                + r"\s*[:\-–—]\s*.+$"
            )

            if re.match(
                inline_pattern,
                clean,
                re.IGNORECASE
            ):

                return True

            # ------------------------------------------
            # Standalone heading
            # ------------------------------------------

            if clean.lower() == boundary.lower():

                return True

        return False

    # --------------------------------------------------
    # Determine whether a line begins another section
    # --------------------------------------------------

    def is_any_heading(line):

        # ------------------------------------------
        # First check scored sections
        # ------------------------------------------

        for section_heading, section_keywords in sections.items():

            if match_scored_heading(
                line,
                section_heading,
                section_keywords
            ):

                return True

        # ------------------------------------------
        # Then check non-scored boundaries
        # ------------------------------------------

        if is_boundary_heading(line):

            return True

        return False

    # --------------------------------------------------
    # Extract a section
    # --------------------------------------------------

    def extract_section(
        heading,
        keywords
    ):

        for index, line in enumerate(lines):

            match = match_scored_heading(
                line,
                heading,
                keywords
            )

            if not match:

                continue

            # ------------------------------------------
            # Inline content
            # ------------------------------------------

            if match["inline_content"]:

                return {
                    "status": "Present",
                    "content": [
                        match["inline_content"]
                    ]
                }

            # ------------------------------------------
            # Heading exists but no inline content.
            # Look at following lines.
            # ------------------------------------------

            collected_content = []

            for next_line in lines[index + 1:]:

                next_clean = clean_line(next_line)

                # Ignore blank lines
                if not next_clean:

                    continue

                # Stop when another heading is reached
                if is_any_heading(next_clean):

                    break

                collected_content.append(
                    next_clean
                )

            # ------------------------------------------
            # Heading exists and has content
            # ------------------------------------------

            if collected_content:

                return {
                    "status": "Present",
                    "content": collected_content
                }

            # ------------------------------------------
            # Heading exists but has no content
            # ------------------------------------------

            return {
                "status": "Empty",
                "content": []
            }

        # ----------------------------------------------
        # Heading doesn't exist
        # ----------------------------------------------

        return {
            "status": "Missing",
            "content": []
        }

    # --------------------------------------------------
    # Validate all required/scored sections
    # --------------------------------------------------

    for heading, keywords in sections.items():

        section_data = extract_section(
            heading,
            keywords
        )

        status = section_data["status"]

        results[heading] = section_data

        # ------------------------------------------
        # Missing
        # ------------------------------------------

        if status == "Missing":

            print(
                f"❌ {heading}: Missing"
            )

        # ------------------------------------------
        # Empty
        # ------------------------------------------

        elif status == "Empty":

            print(
                f"⚠️ {heading}: Empty"
            )

        # ------------------------------------------
        # Present
        # ------------------------------------------

        elif status == "Present":

            print(
                f"✅ {heading}: Present"
            )

            score += 1

    # --------------------------------------------------
    # Calculate overall structure score
    # --------------------------------------------------

    if sections:

        percentage = round(
            (score / len(sections)) * 100
        )

    else:

        percentage = 0

    print(
        f"\nOverall Structure Score: "
        f"{percentage}%"
    )

    return results, percentage