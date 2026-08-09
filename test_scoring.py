from scoring import score_learning_objectives

sample_objectives = """
To understand fraction.
"""

score, feedback = score_learning_objectives(sample_objectives)

print("=" * 40)
print("LEARNING OBJECTIVE SCORE")
print("=" * 40)

print(f"Score: {score}/10")

print("\nFeedback:")

for item in feedback:
    print(f"• {item}")