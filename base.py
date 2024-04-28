# import google.generativeai as genai
# from typing import List, Dict
# from fpdf import FPDF
# import json

# def get_user_preferences():
#     preferences = {}
#     preferences["diets"] = input("Enter your dietary preferences (comma-separated, e.g., vegan, vegetarian, keto): ").lower().split(",")
#     preferences["allergies"] = input("Enter any food allergies or intolerances (comma-separated): ").lower().split(",")
#     preferences["calorie_goal"] = input("Enter your daily calorie goal: ")
#     preferences["include_items"] = input("Enter any specific items you want to include (comma-separated): ").lower().split(",")
#     preferences["exclude_items"] = input("Enter any specific items you want to exclude (comma-separated): ").lower().split(",")
#     preferences["activity_level"] = input("Enter your activity level (low, moderate, high): ").lower()
#     preferences["specific_wishes"] = input("Enter any specific dietary wishes (e.g., include a cup of tea, incorporate mango): ").lower()
#     print("User preferences collected:", preferences)
#     return preferences

# def create_gemini_prompt(preferences):
#     prompt = "Generate a personalized daily meal plan based on the following user preferences:"
#     prompt += f"\nDietary preferences: {', '.join(preferences['diets'])}"
#     prompt += f"\nFood allergies or intolerances: {', '.join(preferences['allergies'])}"
#     prompt += f"\nDaily calorie goal: {preferences['calorie_goal']}"
#     prompt += f"\nItems to include: {', '.join(preferences['include_items'])}"
#     prompt += f"\nItems to exclude: {', '.join(preferences['exclude_items'])}"
#     prompt += f"\nActivity level: {preferences['activity_level']}"
#     prompt += f"\nSpecific dietary wishes: {preferences['specific_wishes']}"
#     prompt += "\n\nThe meal plan should be according to the eating habits and practices of Indian culture, include breakfast, lunch, evening snacks, dinner, with a balanced distribution of micronutrients and macronutrients. Provide detailed meal descriptions, nutrition information, and a daily water intake recommendation based on the user's activity level and other relevant factors. The output should be a JSON object with variables for each meal type, description, ingredients, calories, required protein, carbs, and fat content. The output must be in a strict JSON Format no line must be out of sync to any JSON format For example:"
#     prompt += """
# {
# "water_intake": "3.5 liters",
# "breakfast": {
#     "description": "Oats Upma with Mango and Curd",
#     "ingredients": "Rolled oats, mixed vegetables (carrots, peas, beans), green chilies, ginger, curry leaves, mustard seeds, lemon juice, mango pieces, curd",
#     "calories": 400,
#     "protein": 15,
#     "carbs": 60,
#     "fat": 10
# },
# "lunch": {
#     "description": "Palak Paneer with Brown Rice and Raita",
#     "ingredients": "Paneer (Indian cottage cheese), spinach, tomatoes, onions, garlic, ginger, spices, brown rice, cucumber raita with curd",
#     "calories": 600,
#     "protein": 30,
#     "carbs": 70,
#     "fat": 20
# },
# "evening_snack": {
#     "description": "Fruit and Nut Mix with Curd",
#     "ingredients": "Mango pieces, mixed nuts (almonds, cashews, pistachios), curd",
#     "calories": 250,
#     "protein": 10,
#     "carbs": 30,
#     "fat": 15
# },
# "dinner": {
#     "description": "Vegetable Biryani with Raita",
#     "ingredients": "Basmati rice, mixed vegetables (cauliflower, carrots, peas, beans), spices, curd raita",
#     "calories": 550,
#     "protein": 20,
#     "carbs": 80,
#     "fat": 15
# }
# }
# """
#     print("Gemini prompt created:", prompt)
#     return prompt

# def generate_gemini_prompt(prompt):
#     try:
#         genai.configure(api_key="AIzaSyAZHH_un-_Utn_FGqui86KBC9g6Xyerc14")
#         generation_config = {
#             "temperature": 1,
#             "top_p": 0.95,
#             "top_k": 0,
#             "max_output_tokens": 8192,
#         }
#         safety_settings = [
#             {
#                 "category": "HARM_CATEGORY_HARASSMENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_HATE_SPEECH",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#         ]

#         model = genai.GenerativeModel(
#             model_name="gemini-1.5-pro-latest",
#             generation_config=generation_config,
#             safety_settings=safety_settings
#         )

#         convo = model.start_chat(history=[])
#         convo.send_message(prompt)
#         gemini_prompt = convo.last.text
        

#         # # Split the string into lines
#         # lines = gemini_prompt.splitlines()

#         # # Only keep lines that are valid JSON
#         # lines = [line for line in lines if is_valid_json(line)]

#         # # Join the lines back into a string
#         # gemini_prompt = "\n".join(lines)

#         # def is_valid_json(line):
#         #     try:
#         #         json.loads(line)
#         #         return True
#         #     except json.JSONDecodeError:
#         #         return False
        
#         # print("Gemini prompt generated:", gemini_prompt)
        
#         return gemini_prompt

#     except genai.exceptions.GenerationError as e:
#         print(f"Generation Error: {e}")
#     except genai.exceptions.APIError as e:
#         print(f"API Error: {e}")
#     except Exception as e:
#         print(f"Error generating Gemini API prompt: {e}")

#     return None

# # def parse_meal_plan(gemini_prompt):
# #     try:
# #         meal_plan = json.loads(gemini_prompt)
# #         print("Meal plan parsed:", meal_plan)
# #         return meal_plan
# #     except json.JSONDecodeError:
# #         print("Error: Invalid JSON in Gemini API output.")
# #         return {}
# #     except Exception as e:
# #         print(f"Unexpected error parsing Gemini API output: {e}")
# #         return {}

# # def get_substitute_item(original_item, preferences):
# #     allergies = preferences["allergies"]
# #     restricted_items = preferences["exclude_items"] + allergies
# #     diets = preferences["diets"]
    
# #     substitute_items = []
# #     for diet in diets:
# #         if diet == "vegan":
# #             substitute_items.extend(["tofu", "tempeh", "seitan", "lentils", "chickpeas", "quinoa", "nuts", "seeds"])
# #         elif diet == "vegetarian":
# #             substitute_items.extend([ "cheese", "yogurt", "lentils", "chickpeas", "quinoa", "nuts", "seeds"])
# #         else:
# #             substitute_items.extend(["chicken", "turkey", "lean beef", "fish", "eggs", "cheese", "yogurt", "lentils", "chickpeas", "quinoa", "nuts", "seeds"])
    
# #     for item in substitute_items:
# #         if item.lower() not in original_item.lower() and all(restricted.strip() not in item.lower() for restricted in restricted_items):
# #             print("Substitute item found:", item)
# #             return item
    
# #     return "No suitable substitute found"

# # def calculate_water_intake(activity_level):
# #     if activity_level == "low":
# #         water_intake = 2.7  # liters
# #     elif activity_level == "moderate":
# #         water_intake = 3.7  # liters
# #     else:
# #         water_intake = 4.7  # liters
# #     print("Water intake calculated:", water_intake)
# #     return water_intake

# # def filter_meal_plan(meal_plan, preferences):
# #     filtered_plan = []
# #     allergies = preferences["allergies"]
# #     restricted_items = preferences["exclude_items"]

# #     for meal_type, meal in meal_plan.items():
# #         if meal_type != "water_intake":
# #             meal_description = meal["meal_description"].lower()
# #             if all(allergy.strip() not in meal_description for allergy in allergies) and all(item.strip() not in meal_description for item in restricted_items):
# #                 filtered_plan.append(meal)

# #     print("Meal plan filtered:", filtered_plan)
# #     return filtered_plan

# # def generate_pdf_report(filtered_plan, preferences, water_intake):
# #     try:
# #         pdf = FPDF()
# #         pdf.add_page()
# #         pdf.set_font("Arial", size=16)
# #         pdf.cell(200, 10, txt="Daily Meal Plan Report", ln=1, align="C")

# #         pdf.set_font("Arial", size=12)
# #         pdf.cell(0, 10, txt=f"Dietary Preferences: {', '.join(preferences['diets'])}", ln=1)
# #         pdf.cell(0, 10, txt=f"Food Allergies/Intolerances: {', '.join(preferences['allergies'])}", ln=1)
# #         pdf.cell(0, 10, txt=f"Daily Calorie Goal: {preferences['calorie_goal']}", ln=1)
# #         pdf.cell(0, 10, txt=f"Items to Include: {', '.join(preferences['include_items'])}", ln=1)
# #         pdf.cell(0, 10, txt=f"Items to Exclude: {', '.join(preferences['exclude_items'])}", ln=1)
# #         pdf.cell(0, 10, txt=f"Activity Level: {preferences['activity_level']}", ln=1)
# #         pdf.cell(0, 10, txt=f"Specific Dietary Wishes: {preferences['specific_wishes']}", ln=1)

# #         pdf.cell(0, 10, txt="Meal Plan:", ln=1)
# #         for meal in filtered_plan:
# #             pdf.set_font("Arial", style="B")
# #             pdf.cell(0, 10, txt=meal["meal_type"].capitalize(), ln=1)
# #             pdf.set_font("Arial", style="")
# #             pdf.multi_cell(0, 10, txt=meal["meal_description"])
# #             pdf.cell(0, 10, txt=f"Calories: {meal['calories']} | Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fat: {meal['fat']}g", ln=1)

# #         pdf.cell(0, 10, txt=f"Recommended Daily Water Intake: {water_intake} liters", ln=1)
# #         pdf.output("meal_plan_report.pdf")
# #         print("PDF report generated successfully: meal_plan_report.pdf")
# #     except ImportError:
# #         print("fpdf library is required to generate PDF reports. Please install it using 'pip install fpdf'.")
# #     except Exception as e:
# #         print(f"Error generating PDF report: {e}")

# # def main():
# #     preferences = get_user_preferences()
# #     initial_prompt = create_gemini_prompt(preferences)
# #     gemini_prompt = generate_gemini_prompt(initial_prompt)

# #     if not gemini_prompt:
# #         print("Error: Failed to generate prompt. Please try again with different preferences.")
# #         return

#     # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#     # print("Gemini Output:")
#     # print(gemini_prompt.toJson())
#     # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
#     # meal_plan = parse_meal_plan(gemini_prompt)

#     # if not isinstance(meal_plan, dict) or "meals" not in meal_plan:
#     #     print("Error: Failed to generate meal plan. Please try again with different preferences.")
#     #     return

#     # filtered_plan = filter_meal_plan(meal_plan, preferences)

#     # print("\nFiltered Meal Plan:")
#     # for meal in filtered_plan:
#     #     print(meal)
#     #     if input(f"Do you want to substitute any items in {meal['meal_type']}? (y/n) ").lower() == "y":
#     #         item_to_substitute = input(f"Enter the item you want to substitute: ").lower()
#     #         if item_to_substitute in meal["meal_description"].lower():
#     #             substitute_item = get_substitute_item(item_to_substitute, preferences)
#     #             meal["meal_description"] = meal["meal_description"].replace(item_to_substitute, substitute_item)
#     #             print(f"Substituted {item_to_substitute} with {substitute_item}.")
#     #             print(meal)

#     # water_intake = calculate_water_intake(preferences["activity_level"])
#     # print(f"\nRecommended daily water intake: {water_intake} liters")

# #     generate_pdf_report(gemini_prompt)

# # if __name__ == "__main__":
# #     main()        


# def main():
#     preferences = get_user_preferences()
#     initial_prompt = create_gemini_prompt(preferences)
#     gemini_prompt = generate_gemini_prompt(initial_prompt)

#     if not gemini_prompt:
#         print("Error: Failed to generate prompt. Please try again with different preferences.")
#         return

#     # Print the Gemini output to a PDF file
#     generate_pdf_report(gemini_prompt)

# def generate_pdf_report(meal_plan):
#     try:
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=16)
#         pdf.cell(200, 10, txt="Daily Meal Plan Report", ln=1, align="C")

#         pdf.set_font("Arial", size=12)
#         for meal_type, meals in meal_plan.items():
#             pdf.cell(200, 10, txt=f"{meal_type}:", ln=1)
#             for meal in meals:
#                 pdf.cell(200, 10, txt=f"  - {meal}", ln=1)

#         pdf.output("meal_plan_report.pdf")
#         print("PDF report generated successfully: meal_plan_report.pdf")
#     except ImportError:
#         print("fpdf library is required to generate PDF reports. Please install it using 'pip install fpdf'.")
#     except Exception as e:
#         print(f"Error generating PDF report: {e}")

# if __name__ == "__main__":
#     main()
