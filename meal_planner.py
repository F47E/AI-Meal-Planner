import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import ast
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='YOUR_API_KEY_HERE')  # Replace with your actual API key

class MealPlannerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Meal Planner")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Enter your ingredients (comma-separated):").pack(side=tk.LEFT)
        self.ingredients_entry = ttk.Entry(input_frame, width=50)
        self.ingredients_entry.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Button(input_frame, text="Generate Meal Plan", command=self.generate_meal_plan).pack(side=tk.LEFT, padx=(5, 0))

        # Output section
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        # Meal ideas output
        ttk.Label(output_frame, text="Meal Ideas:").pack(anchor=tk.W)
        self.meal_ideas_text = scrolledtext.ScrolledText(output_frame, height=10, width=80, wrap=tk.WORD)
        self.meal_ideas_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Meal plan output
        ttk.Label(output_frame, text="Weekly Meal Plan:").pack(anchor=tk.W)
        self.meal_plan_text = scrolledtext.ScrolledText(output_frame, height=10, width=80, wrap=tk.WORD)
        self.meal_plan_text.pack(fill=tk.BOTH, expand=True)

    def generate_meal_plan(self):
        ingredients = self.ingredients_entry.get().split(',')
        ingredients = [ingredient.strip() for ingredient in ingredients]

        try:
            meal_ideas = self.get_gemini_meal_ideas(ingredients)
            meal_plan = self.get_gemini_meal_plan(meal_ideas)

            # Display results
            self.display_results(meal_ideas, meal_plan)

            # Save results
            self.save_results(meal_ideas, meal_plan)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_gemini_meal_ideas(self, ingredients):
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Based on the following ingredients: {', '.join(ingredients)}
        Please provide a list of 10 meal ideas that can be made using these ingredients.
        Format the response as a Python list of strings, like this:
        ["Meal 1", "Meal 2", "Meal 3", ...]"""

        response = model.generate_content(prompt)
        try:
            # Remove any markdown formatting
            clean_response = response.text.strip('`').strip()
            if clean_response.startswith('python'):
                clean_response = clean_response[6:].strip()
            
            meal_ideas = ast.literal_eval(clean_response)
            if not isinstance(meal_ideas, list):
                raise ValueError("Response is not a list")
            return meal_ideas
        except Exception as e:
            print(f"Error parsing meal ideas: {e}")
            print(f"Raw response: {response.text}")
            return ["Error: Couldn't parse meal ideas. Please try again."]

    def get_gemini_meal_plan(self, meal_ideas):
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Create a weekly meal plan (3 meals a day for 7 days) using the following meal ideas:
        {meal_ideas}
        Format the response as a Python dictionary where keys are days of the week,
        and values are dictionaries with 'Breakfast', 'Lunch', and 'Dinner' as keys.
        Return only the Python dictionary, without any additional text or formatting."""

        response = model.generate_content(prompt)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        try:
            clean_response = response.text.strip('`')
            if clean_response.startswith('python\n'):
                clean_response = clean_response[7:]
            
            dict_start = clean_response.find('{')
            if dict_start != -1:
                clean_response = clean_response[dict_start:]
            
            meal_plan = ast.literal_eval(clean_response)
            
            if not isinstance(meal_plan, dict):
                raise ValueError("Response is not a dictionary")
            
            for day in days:
                if day not in meal_plan or not isinstance(meal_plan[day], dict):
                    meal_plan[day] = {'Breakfast': 'Not specified', 'Lunch': 'Not specified', 'Dinner': 'Not specified'}
                else:
                    for meal in ['Breakfast', 'Lunch', 'Dinner']:
                        if meal not in meal_plan[day] or meal_plan[day][meal] is None:
                            meal_plan[day][meal] = 'Not specified'
            return meal_plan
        except Exception as e:
            print(f"Error parsing meal plan: {e}")
            print(f"Raw response: {response.text}")
            return {day: {'Breakfast': 'Error', 'Lunch': 'Error', 'Dinner': 'Error'} for day in days}

    def display_results(self, meal_ideas, meal_plan):
        # Display meal ideas
        self.meal_ideas_text.delete('1.0', tk.END)
        for idea in meal_ideas:
            self.meal_ideas_text.insert(tk.END, f"- {idea}\n")

        # Display meal plan
        self.meal_plan_text.delete('1.0', tk.END)
        for day, meals in meal_plan.items():
            self.meal_plan_text.insert(tk.END, f"{day}:\n")
            for meal_type, meal in meals.items():
                self.meal_plan_text.insert(tk.END, f"  {meal_type}: {meal}\n")
            self.meal_plan_text.insert(tk.END, "\n")

    def save_results(self, meal_ideas, meal_plan):
        if not os.path.exists("meal_planner_output"):
            os.makedirs("meal_planner_output")

        with open("meal_planner_output/meal_ideas.txt", "w") as f:
            for idea in meal_ideas:
                f.write(f"- {idea}\n")

        with open("meal_planner_output/meal_plan.txt", "w") as f:
            for day, meals in meal_plan.items():
                f.write(f"{day}:\n")
                for meal_type, meal in meals.items():
                    f.write(f"  {meal_type}: {meal}\n")
                f.write("\n")

        print("Results saved to 'meal_planner_output' folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()
