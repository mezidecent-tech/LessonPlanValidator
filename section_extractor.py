import re


def extract_section(text, headings, stop_headings=None):

    if stop_headings is None:
        stop_headings = []

    lines = text.splitlines()

    # --------------------------------------------------
    # Clean headings
    # --------------------------------------------------

    headings = [
        heading.strip().lower()
        for heading in headings
    ]

    stop_headings = [
        heading.strip().lower()
        for heading in stop_headings
    ]

    # --------------------------------------------------
    # Check whether a line is a heading
    # --------------------------------------------------

    def match_heading(line, heading_list):

        clean = line.strip()

        for heading in heading_list:

            # Heading only
            if clean.lower() == heading:

                return True, ""

            # Heading followed by :
            pattern = (
                r"^"
                + re.escape(heading)
                + r"\s*[:\-–—]\s*(.*)$"
            )

            match = re.match(
                pattern,
                clean,
                re.IGNORECASE
            )

            if match:

                return True, match.group(1).strip()

        return False, None

    # --------------------------------------------------
    # Find the requested section
    # --------------------------------------------------

    for index, line in enumerate(lines):

        found, inline_content = match_heading(
            line,
            headings
        )

        if not found:
            continue

        # --------------------------------------------------
        # Heading contains content on same line
        # Example:
        #
        # Learning Objectives: Calculate perimeter
        # --------------------------------------------------

        if inline_content:

            return {
                "status": "Present",
                "content": [
                    inline_content
                ]
            }

        # --------------------------------------------------
        # Heading is empty.
        # Collect following lines.
        # --------------------------------------------------

        collected = []

        for next_line in lines[index + 1:]:

            clean = next_line.strip()

            # Ignore blank lines
            if not clean:
                continue

            # --------------------------------------------------
            # Stop at another lesson-plan heading
            # --------------------------------------------------

            is_stop = False

            found_stop, stop_content = match_heading(
                clean,
                stop_headings
            )

            if found_stop:

                is_stop = True

            if is_stop:
                break

            # --------------------------------------------------
            # Also stop at common lesson headings
            # --------------------------------------------------

            common_headings = [
                "subject",
                "topic",
                "unit",
                "year",
                "date",
                "teacher",
                "ta",
                "resources",
                "starter",
                "main activity",
                "plenary",
                "assessment",
                "homework",
                "differentiation",
                "success criteria",
                "learning objectives",
                "learning objective",
                "learning intention"
            ]

            found_common, common_content = match_heading(
                clean,
                common_headings
            )

            if found_common:
                break

            # --------------------------------------------------
            # Add actual content
            # --------------------------------------------------

            collected.append(clean)

        # --------------------------------------------------
        # Return extracted content
        # --------------------------------------------------

        if collected:

            return {
                "status": "Present",
                "content": collected
            }

        return {
            "status": "Empty",
            "content": []
        }

    # --------------------------------------------------
    # Section not found
    # --------------------------------------------------

    return {
        "status": "Missing",
        "content": []
    }