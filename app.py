
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="GrowthMate AI",
    page_icon="🌱",
    layout="wide"
)

# Get configuration from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# Connect to Groq
client = Groq(
    api_key=GROQ_API_KEY
)


def generate_growth_plan(profile):

    prompt = f"""
    You are GrowthMate AI, an expert personal and professional growth coach.

    Create a COMPLETE SIX-MONTH growth roadmap for this user.

    USER PROFILE:
    Name: {profile['name']}
    Current Role: {profile['role']}
    Experience: {profile['experience']}
    Professional Interests: {profile['career_interest']}
    Personal Interests: {profile['personal_interest']}
    Available Time Per Week: {profile['available_time']}

    IMPORTANT: THE ROADMAP MUST CONTAIN EXACTLY SIX MONTHS.

    You MUST generate all six sections using these exact headings:

    ## MONTH 1
    ## MONTH 2
    ## MONTH 3
    ## MONTH 4
    ## MONTH 5
    ## MONTH 6

    Do not skip, combine, or shorten any month.
    Do not finish the response before completing MONTH 6.

    FOR EACH MONTH, INCLUDE:

    1. Monthly Theme
    2. Professional Goals (2-3 goals)
    3. Personal Development Goals (1-2 goals)
    4. Action Items (specific tasks)
    5. Measurable Milestones
    6. Expected Outcomes
    7. Estimated Time Commitment

    ROADMAP REQUIREMENTS:

    - Month 1 should establish the foundation.
    - Month 2 should build fundamental skills and habits.
    - Month 3 should focus on practical application.
    - Month 4 should introduce more advanced development.
    - Month 5 should focus on projects and measurable achievements.
    - Month 6 should focus on completing goals and evaluating progress.

    Make every month progressively build on the previous month.

    Ensure all goals are SMART:
    Specific, Measurable, Achievable, Relevant and Time-bound.

    Consider the user's available time and experience.
    Avoid unrealistic workloads.

    FORMATTING:
    - Use clear headings and bullet points.
    - Do not use Markdown tables.
    - Keep explanations concise.
    - Separate professional and personal goals.

    FINAL VALIDATION:
    Before responding, verify that MONTH 1, MONTH 2, MONTH 3,
    MONTH 4, MONTH 5 and MONTH 6 are all included.

    Return the complete six-month roadmap.
    """


    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are GrowthMate AI, a supportive and practical growth coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# -------------------------------
# APPLICATION INTERFACE
# -------------------------------

st.title("🌱 GrowthMate AI")
st.subheader("Your Personal AI Growth Coach")

st.write(
    "Build a personalized six-month roadmap "
    "for your professional and personal growth."
)

st.divider()

st.header("Let's get to know you")

with st.form("profile_form"):

    name = st.text_input("Your name")

    role = st.text_input(
        "What is your current job role?"
    )

    experience = st.text_input(
        "How many years of experience do you have?"
    )

    career_interest = st.text_area(
        "What are your professional growth interests?",
        placeholder="Example: AI testing, automation, leadership..."
    )

    personal_interest = st.text_area(
        "What personal areas would you like to improve?",
        placeholder="Example: Fitness, communication, time management..."
    )

    available_time = st.selectbox(
        "How much time can you dedicate to growth per week?",
        [
            "1-2 hours",
            "3-5 hours",
            "6-8 hours",
            "9-12 hours",
            "More than 12 hours"
        ]
    )

    submitted = st.form_submit_button(
        "Generate My 6-Month Growth Plan",
        use_container_width=True
    )


if submitted:

    if not all([
        name.strip(),
        role.strip(),
        experience.strip(),
        career_interest.strip(),
        personal_interest.strip()
    ]):
        st.warning("Please complete all profile fields.")

    elif not os.getenv("GROQ_API_KEY"):
        st.error("Groq API key not found. Please check your .env file.")

    else:

        profile = {
            "name": name,
            "role": role,
            "experience": experience,
            "career_interest": career_interest,
            "personal_interest": personal_interest,
            "available_time": available_time
        }

        try:
            with st.spinner(
                "GrowthMate AI is building your personalized roadmap..."
            ):
                growth_plan = generate_growth_plan(profile)

            st.session_state["growth_plan"] = growth_plan
            st.session_state["user_name"] = name

        except Exception as error:
            st.error(f"Something went wrong: {error}")


# Display the generated roadmap
if "growth_plan" in st.session_state:

    st.divider()

    st.header(
        f"Your Growth Roadmap, {st.session_state['user_name']}! 🚀"
    )

    st.markdown(st.session_state["growth_plan"])
