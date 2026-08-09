from metadata_extractor import extract_metadata

sample = """
Teacher: Chukwuemeka Emmanuel
Subject: Mathematics
Topic: Equivalent Fractions
Year: 4
Date: 07/08/2026
"""

metadata = extract_metadata(sample)

print("=" * 40)

print("LESSON PLAN METADATA")

print("=" * 40)

for key, value in metadata.items():

    print(f"{key}: {value}")