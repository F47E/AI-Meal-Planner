# Meal Planner

## Description

Meal Planner is a Python application that uses the Google Gemini 1.5 Flash model to generate meal ideas and create weekly meal plans based on the ingredients you have on hand. This tool helps you make the most of your available ingredients and plan your meals efficiently.

## Features

- User-friendly graphical interface
- Input your available ingredients
- Generate meal ideas based on your ingredients
- Create a weekly meal plan (3 meals a day for 7 days)
- Save meal ideas and meal plans as text files

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- A Google Gemini API key

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/F47E/ai-meal-planner.git
   cd ai-meal-planner
   ```

2. Install the required packages:
   ```sh
   pip install google-generativeai tkinter
   ```

3. Set up your Google Gemini API key:
   - Obtain an API key from the [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace `'YOUR_API_KEY_HERE'` in the `meal_planner.py` file with your actual API key

## Usage

1. Run the application:
   ```sh
   python meal_planner.py
   ```

2. In the application window:
   - Enter your available ingredients, separated by commas
   - Click the "Generate Meal Plan" button
   - View the generated meal ideas and weekly meal plan in the application window

3. The results will be automatically saved in the `meal_planner_output` folder:
   - `meal_ideas.txt`: List of generated meal ideas
   - `meal_plan.txt`: Weekly meal plan

