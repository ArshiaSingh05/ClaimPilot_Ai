import re

def parse_query(text):
    # Normalize
    text = text.lower()

    # Age
    age_match = re.search(r'(\d{2})[- ]?year[- ]?old', text)
    age = int(age_match.group(1)) if age_match else None

    # Gender
    if "male" in text or "m/" in text:
        gender = "male"
    elif "female" in text or "f/" in text:
        gender = "female"
    else:
        gender = None

    # Procedure
    procedures = ["knee surgery", "childbirth", "dental treatment", "eye surgery", "hip replacement"]
    found_procedure = next((p for p in procedures if p in text), None)

    # Location (optional, basic extraction from city list)
    cities = ["pune", "mumbai", "delhi", "bangalore", "chennai", "kolkata"]
    found_city = next((city.title() for city in cities if city in text), None)

    # Policy Duration
    dur_match = re.search(r'(\d+)[ -]?(month|months|year|years)', text)
    policy_duration = dur_match.group(0) if dur_match else None

    return {
        "age": age,
        "gender": gender,
        "procedure": found_procedure,
        "location": found_city,
        "policy_duration": policy_duration
    }

# Test
if __name__ == "__main__":
    sample = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
    parsed = parse_query(sample)

    print(" Parsed Query Output:")
    for key, value in parsed.items():
        print(f"{key}: {value}")
