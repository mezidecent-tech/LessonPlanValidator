from recommendations import recommend_learning_objectives

score = 6

recommendations = recommend_learning_objectives(score)

print("=" * 40)
print("AI RECOMMENDATIONS")
print("=" * 40)

for recommendation in recommendations:

    print(f"• {recommendation}")