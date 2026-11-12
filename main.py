
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Connect to Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def collect_profile():
    print("\n--- Let's Get to Know You ---")

    name = input("What is your name? ")
    role = input("What is your current job role? ")
    experience = input("How many years of experience do you have? ")
    career_interest = input("What are your professional growth interests? ")
    personal_interest = input("What personal areas would you like to improve? ")
    available_time = input("How many hours per week can you dedicate to growth? ")

    return {
        "name": name,
        "role": role,
        "experience": experience,
        "career_interest": career_interest,
        "personal_interest": personal_interest,
        "available_time": available_time
    }


def generate_growth_plan(profile):
    
    prompt = f"""
    You are GrowthMate AI, an intelligent personal and professional
    growth coach.

    Create a personalized SIX-MONTH growth roadmap using this profile:

    Name: {profile['name']}
    Current Role: {profile['role']}
    Experience: {profile['experience']}
    Professional Interests: {profile['career_interest']}
    Personal Interests: {profile['personal_interest']}
    Available Time Per Week: {profile['available_time']}

    REQUIREMENTS:

    1. Start with a brief assessment of the user's current position.

    2. Create a six-month roadmap, with a separate section for
    each month (Month 1 to Month 6).

    3. For EVERY month, include:
    - Monthly theme
    - 2-3 professional goals
    - 1-2 personal development goals
    - Specific actionable tasks
    - Measurable milestones
    - Expected outcomes
    - Estimated time commitment

    4. Make the roadmap progressive. Each month should build
    upon the skills and achievements of previous months.

    5. Ensure goals are SMART:
    Specific, Measurable, Achievable, Relevant and Time-bound.

    6. Consider the user's actual experience and available time.
    Do not overload the user with unrealistic tasks.

    7. Include a monthly progress review with questions
    the user can answer to evaluate their development.

    8. End with the expected achievements after six months.

    FORMATTING RULES:

    - Use clear headings and subheadings.
    - Use bullet points instead of Markdown tables.
    - Keep explanations concise and practical.
    - Separate professional and personal goals.
    - Make the roadmap easy to read.

    Your recommendations must be personalized, realistic,
    and actionable.
    """


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are GrowthMate AI, an expert personal and professional growth coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def main():
    print("=" * 45)
    print("Welcome to GrowthMate AI!")
    print("Your Personal AI Growth Coach")
    print("=" * 45)

    profile = collect_profile()

    print("\nGenerating your personalized growth plan...")
    
    growth_plan = generate_growth_plan(profile)

    print("\n" + "=" * 45)
    print("YOUR PERSONALIZED GROWTH PLAN")
    print("=" * 45)
    print(growth_plan)


if __name__ == "__main__":
    main()
