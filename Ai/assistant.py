import requests
from backend.database import get_connection


def get_business_info():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM business_info
        ORDER BY id DESC
        LIMIT 1
    """)

    business = cursor.fetchone()

    connection.close()

    if business is None:
        return None

    return {
        "business_name": business["business_name"],
        "phone": business["phone"],
        "email": business["email"],
        "location": business["location"],
        "courses": business["courses"],
        "fees": business["fees"],
        "timings": business["timings"],
        "additional": business["additional"]
    }


def get_response(message):

    business = get_business_info()

    if business is None:
        return "Business information is not available right now."

    business_data = f"""
Business Name: {business['business_name']}
Phone: {business['phone']}
Email: {business['email']}
Location: {business['location']}
Courses: {business['courses']}
Fees: {business['fees']}
Batch Timings: {business['timings']}
Additional Information: {business['additional']}
"""

    print("\n========== BUSINESS DATA ==========")
    print(business_data)
    print("===================================\n")

    prompt = f"""
You are Nuvexa AI, a business assistant.

Answer the customer's question using ONLY the business information below.

BUSINESS INFORMATION:
{business_data}

STRICT RULES:
1. If the customer asks about fees, give the exact fee from the BUSINESS INFORMATION.
2. If the customer asks about courses, give the courses from the BUSINESS INFORMATION.
3. If the customer asks about timings, give the exact timings.
4. If the customer asks for contact information, give the phone or email.
5. NEVER use placeholders such as [insert actual fee here].
6. NEVER invent information.
7. Do not mention Python, database, API, SQLite or internal systems.
8. Give a short, natural and professional answer.

CUSTOMER QUESTION:
{message}

ANSWER:
"""

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()

    except requests.exceptions.ConnectionError:
        return "Sorry, Nuvexa AI cannot connect to the AI server right now."

    except requests.exceptions.Timeout:
        return "Sorry, the AI is taking too long to respond."

    except Exception as error:
        print("Nuvexa AI Error:", error)
        return "Sorry, something went wrong while processing your message."








