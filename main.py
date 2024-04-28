from flask import Flask, render_template, request, send_file
import io
from io import BytesIO
import json
import csv

app = Flask(__name__, template_folder='templates')

# Import the necessary functions from the `meal_plan_generator` module
from meal_plan_generator import get_user_preferences, create_gemini_prompt, generate_gemini_prompt, generate_pdf_report

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    # Get user preferences from the form data
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    email = request.form.get('email')
    diets = request.form.getlist('diets')
    allergies = request.form.getlist('allergies')
    calorie_goal = request.form.get('calorie_goal')
    include_items = request.form.getlist('include_items')
    exclude_items = request.form.getlist('exclude_items')
    activity_level = request.form.get('activity_level')
    specific_wishes = request.form.get('specific_wishes')

    preferences = {
        'name': name,
        'age': age,
        'gender': gender,
        'weight': weight,
        'email': email,
        'diets': diets,
        'allergies': allergies,
        'calorie_goal': calorie_goal,
        'include_items': include_items,
        'exclude_items': exclude_items,
        'activity_level': activity_level,
        'specific_wishes': specific_wishes
    }

    # Create the Gemini prompt
    initial_prompt = create_gemini_prompt(preferences)

    # Generate the Gemini prompt
    gemini_prompt = generate_gemini_prompt(initial_prompt)

    # if not gemini_prompt:
    #     return "Error: Failed to generate prompt. Please try again with different preferences."

    # # Check if the Gemini prompt is not empty or None
    # try:
    #     gemini_prompt_dict = json.loads(gemini_prompt)
    # except json.JSONDecodeError:
    #     return "Error: Invalid JSON format in Gemini prompt."
    
    if not gemini_prompt:
      return "Error: Failed to generate prompt. Please try again with different preferences."
        # Store the user's email address (if provided)
    # Check if the user wants to receive the report via email
    receive_email = request.form.get('receive_email') == 'yes'

    if receive_email:
        # Generate the PDF report
        pdf_output = generate_pdf_report(gemini_prompt)

        if pdf_output:
            # Send the PDF report via email
            send_meal_plan_email(preferences['email'], pdf_output.getvalue())
            return "Meal plan report sent to your email."
        else:
            return "Error: Failed to generate PDF report."

   # Pass the raw Gemini output to the template
    return render_template('gemini_output.html', gemini_output=gemini_prompt)
    # # Generate the PDF report
    # pdf_output = generate_pdf_report(gemini_prompt)

    # if not pdf_output:
    #     return "Error: Failed to generate PDF report."
    # # Convert the PDF output to a file-like object
    # pdf_file = BytesIO(pdf_output.getvalue())

    # # Send the PDF file for download
    # return send_file(
    #     pdf_file,
    #     mimetype='application/pdf',
    #     as_attachment=True,
    #     download_name='meal_plan_report.pdf'
    # )
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        # Store the email address (e.g., in a CSV file or a database)
        with open('users.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([email])
        return 'Thank you for signing up!'
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)