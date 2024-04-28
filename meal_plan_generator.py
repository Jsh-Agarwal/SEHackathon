import google.generativeai as genai
from typing import List, Dict
from fpdf import FPDF
import json
import io
import re
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate

def get_user_preferences():
    preferences = {}
    preferences["diets"] = input("Enter your dietary preferences (comma-separated, e.g., vegan, vegetarian, keto): ").lower().split(",")
    preferences["allergies"] = input("Enter any food allergies or intolerances (comma-separated): ").lower().split(",")
    preferences["calorie_goal"] = input("Enter your daily calorie goal: ")
    preferences["include_items"] = input("Enter any specific items you want to include (comma-separated): ").lower().split(",")
    preferences["exclude_items"] = input("Enter any specific items you want to exclude (comma-separated): ").lower().split(",")
    preferences["activity_level"] = input("Enter your activity level (low, moderate, high): ").lower()
    preferences["specific_wishes"] = input("Enter any specific dietary wishes (e.g., include a cup of tea, incorporate mango): ").lower()
    print("User preferences collected:", preferences)
    return preferences

def create_gemini_prompt(preferences):
    prompt = f"Generate a personalized daily meal plan for {preferences['name']} ({preferences['age']} years old, {preferences['gender']}, {preferences['weight']} kg) based on the following preferences:"
    prompt += f"\nDietary preferences: {', '.join(preferences['diets'])}"
    prompt += f"\nFood allergies or intolerances: {', '.join(preferences['allergies'])}"
    prompt += f"\nDaily calorie goal: {preferences['calorie_goal']}"
    prompt += f"\nItems to include: {', '.join(preferences['include_items'])}"
    prompt += f"\nItems to exclude: {', '.join(preferences['exclude_items'])}"
    prompt += f"\nActivity level: {preferences['activity_level']}"
    prompt += f"\nSpecific dietary wishes: {preferences['specific_wishes']}"
    prompt += "\n\nThe meal plan should be according to the eating habits and practices of Indian culture, include breakfast, lunch, evening snacks, dinner, with a balanced distribution of micronutrients and macronutrients. Consider the user's age, gender, and weight while creating the meal plan. Provide detailed meal descriptions, nutrition information, and a daily water intake recommendation based on the user's activity level and other relevant factors. The output should be in a user-friendly text format, with each meal type followed by its description, ingredients, and nutrition details. For example:"
    prompt += """

Water Intake: 3.5 liters

Breakfast:
Oats Upma with Mango and Curd
Ingredients: Rolled oats, mixed vegetables (carrots, peas, beans), green chilies, ginger, curry leaves, mustard seeds, lemon juice, mango pieces, curd
Calories: 400, Protein: 15g, Carbs: 60g, Fat: 10g

Lunch:
Palak Paneer with Brown Rice and Raita
Ingredients: Paneer (Indian cottage cheese), spinach, tomatoes, onions, garlic, ginger, spices, brown rice, cucumber raita with curd
Calories: 600, Protein: 30g, Carbs: 70g, Fat: 20g

Evening Snack:
Fruit and Nut Mix with Curd
Ingredients: Mango pieces, mixed nuts (almonds, cashews, pistachios), curd
Calories: 250, Protein: 10g, Carbs: 30g, Fat: 15g

Dinner:
Vegetable Biryani with Raita
Ingredients: Basmati rice, mixed vegetables (cauliflower, carrots, peas, beans), spices, curd raita
Calories: 550, Protein: 20g, Carbs: 80g, Fat: 15g
"""
    print("Gemini prompt created:", prompt)
    return prompt

def generate_gemini_prompt(prompt):
    try:
        genai.configure(api_key="AIzaSyAZHH_un-_Utn_FGqui86KBC9g6Xyerc14")
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        gemini_prompt = convo.last.text
        lines = gemini_prompt.splitlines()
        trimmed_lines = lines[1:-1]  # Remove the first and last lines
        gemini_prompt = '\n'.join(trimmed_lines)
        
        
        return gemini_prompt
        
        # # Clean up and make the Gemini prompt a valid JSON string
        # gemini_prompt = re.sub(r'[^\{\}\[\]\,\:\"\'\w\s]', '', gemini_prompt)
        # gemini_prompt = ''.join(char for char in gemini_prompt if char.isascii())
        # gemini_prompt = '{' + gemini_prompt.strip() + '}'
        # gemini_prompt_dict = convo.last.text

        # # Convert the Gemini prompt to a valid JSON string
        # gemini_prompt_json = json.dumps(gemini_prompt_dict)
        # return gemini_prompt_json
        

    except genai.exceptions.GenerationError as e:
        print(f"Generation Error: {e}")
    except genai.exceptions.APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error generating Gemini API prompt: {e}")

    return None

def generate_pdf_report(gemini_prompt):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Daily Meal Plan Report", ln=1, align="C")

        pdf.set_font("Arial", size=12)
        for line in gemini_prompt.splitlines():
            pdf.multi_cell(0, 10, txt=line)

        # Create an in-memory buffer to store the PDF
        pdf_bytes = io.BytesIO()
        pdf.output(pdf_bytes, 'S')

    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return None

    return pdf_bytes


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_meal_plan_email(recipient_email, pdf_output):
    sender_email = "jsh.agarwal15@gmail.com"
    sender_password = "15122004@Kio#"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Your Meal Plan'

    part = MIMEBase('application', "octet-stream")
    part.set_payload(pdf_output)
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="meal_plan.pdf"')
    msg.attach(part)

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with the appropriate SMTP server and port for your email provider
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)
        smtp_server.send_message(msg)
        smtp_server.quit()
        print("Successfully sent email")
    except Exception as e:
        print(f"Error: unable to send email: {e}")

        
def generate_meal_plans():
    for email in emails:
        # Retrieve user preferences (you'll need to store and retrieve these)
        preferences = {
            'name': 'John Doe',
            'age': '30',
            'gender': 'male',
            'weight': '75',
            'diets': ['vegetarian'],
            'allergies': [],
            'calorie_goal': '2000',
            'include_items': [],
            'exclude_items': [],
            'activity_level': 'moderate',
            'specific_wishes': ''
        }

        initial_prompt = create_gemini_prompt(preferences)
        gemini_prompt = generate_gemini_prompt(initial_prompt)

        if gemini_prompt:
            pdf_output = generate_pdf_report(gemini_prompt)
            if pdf_output:
                send_meal_plan_email(email, pdf_output)

scheduler = BackgroundScheduler()
scheduler.add_job(generate_meal_plans, 'cron', hour=8)
scheduler.start()  
if __name__ == "__main__":
    main()
