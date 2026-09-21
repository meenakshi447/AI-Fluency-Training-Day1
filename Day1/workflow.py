import re

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}

question = input("Ask a question: ").strip()

if re.search(r"\bCS101\b", question, re.IGNORECASE) and "total" in question.lower():
    print("CS101 fee is ₹12,000.")

elif re.search(r"\bAI202\b", question, re.IGNORECASE) and "fee" in question.lower():
    print("AI202 fee is ₹18,000.")

elif (
    re.search(r"\bCS101\b", question, re.IGNORECASE)
    and re.search(r"\bAI202\b", question, re.IGNORECASE)
    and "total" in question.lower()
):
    total = COURSE_FEES["CS101"] + COURSE_FEES["AI202"]
    scholarship_total = total * 0.9
    print(f"Total after 10% scholarship: ₹{scholarship_total:.0f}.")

else:
    print("Sorry, I don't have a rule for that question.")