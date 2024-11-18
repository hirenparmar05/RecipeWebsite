import pandas as pd
import random
import requests
import re  # Import the regular expressions module

API_KEY = 'FtiBqTvtyNcF7FrO5c3oSg==aLg0Iw2qa5daSY7e'
API_URL = 'https://api.calorieninjas.com/v1/nutrition?query='

# Load the dataset
def load_data():
    # Update the file path to your actual CSV file
    file_path = "/Users/hirenparmar/Downloads/foodDataset/Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
    data = pd.read_csv(file_path)
    # Ensure missing values are handled
    data['Ingredients'] = data['Ingredients'].fillna("No ingredients listed")
    data['Instructions'] = data['Instructions'].fillna("No instructions available")
    return data

# Load data
df = load_data()

def get_calories_and_macros(ingredient):
    headers = {
        'X-Api-Key': API_KEY
    }
    response = requests.get(f"{API_URL}{ingredient}", headers=headers)

    # Check the status code of the API response
    if response.status_code == 200:
        try:
            data = response.json()  # Parse JSON response
            # Check if the API returned items
            if 'items' in data and data['items']:
                # Extract calories and macronutrient information
                item = data['items'][0]
                calories = item.get('calories', 'Calories not found')
                protein = item.get('protein_g', 'Protein not found')
                total_fat = item.get('fat_total_g', 'Total fat not found')
                carbohydrates = item.get('carbohydrates_total_g', 'Carbohydrates not found')

                # Return the values as a dictionary
                return {
                    'calories': calories,
                    'protein': protein,
                    'total_fat': total_fat,
                    'carbohydrates': carbohydrates
                }
            else:
                return f"No nutritional data found for '{ingredient}'."
        except Exception as e:
            return f"Error parsing the response: {e}"
    else:
        return f"Error fetching data for {ingredient}: {response.status_code}"


def grams_to_calories(grams, calories_per_100g):
    calories = (grams / 100) * calories_per_100g
    return calories

# Function to search by title with a limit and show more functionality
def search_by_title(title):
    filtered_title = df[df['Title'].str.contains(title, case=False, na=False)]
    if not filtered_title.empty:
        print("\nResults:")
        max_results = 5  # Initial results to display
        displayed = 0

        while displayed < len(filtered_title):
            # Display a batch of results
            batch = filtered_title.iloc[displayed: displayed + max_results]
            for _, row in batch.iterrows():
                print(f"\n{row['Title']}")
                #print(f"Ingredients: {row['Ingredients']}")
                #print(f"Instructions: {row['Instructions']}")

                # Give the user the choice to see more details or exit
                while True:
                    action = input("\nDo you want to see the ingredients (i), instructions (u), or next (n), or exit (e)? ").strip().lower()
                    if action == 'i':
                        print(f"\nIngredients: {row['Ingredients']}")
                    elif action == 'u':
                        print(f"\nInstructions: {row['Instructions']}")
                    elif action == 'n':
                        break  # Exit to the main menu
                    elif action == 'e':
                        return False# Exit the program
                    else:
                        print("Invalid choice, please try again.")
            displayed += max_results
            # Ask if the user wants to see more results
            if displayed < len(filtered_title):
                show_more = input("\nDo you want to see more results? (y/n): ").strip().lower()
                if show_more != 'y':
                    break
            else:
                print("\nNo more results to show.")
    else:
        print("No recipes found with that title.")


# Function to search by multiple ingredients


def search_by_ingredients(ingredients):
    # Split the input string by commas, strip extra spaces and remove empty ingredients
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(",") if ingredient.strip()]

    if not ingredients_list:
        print("No ingredients provided.")
        return

    # Filter the recipes that contain all the ingredients (full word match)
    filtered_ingredient = df
    for ingredient in ingredients_list:
        # Use word boundary `\b` to match full words, case insensitive
        regex = rf'\b{re.escape(ingredient)}\b'
        filtered_ingredient = filtered_ingredient[filtered_ingredient['Ingredients'].str.contains(regex, case=False, na=False, regex=True)]

    if not filtered_ingredient.empty:
        print("\nResults:")
        max_results = 5  # Initial results to display
        displayed = 0

        while displayed < len(filtered_ingredient):
            # Display a batch of results
            batch = filtered_ingredient.iloc[displayed: displayed + max_results]
            for _, row in batch.iterrows():
                print(f"\n{row['Title']}")
                #print(f"Ingredients: {row['Ingredients']}")

                # Give the user the choice to see more details or exit
                while True:
                    action = input("\nDo you want to see the ingredients (i), instructions (u), or next (n), or exit (e)? ").strip().lower()
                    if action == 'i':
                        print(f"\nIngredients: {row['Ingredients']}")
                    elif action == 'u':
                        print(f"\nInstructions: {row['Instructions']}")
                    elif action == 'n':
                        break  # Exit to the main menu
                    elif action == 'e':
                        return False  # Exit the program
                    else:
                        print("Invalid choice, please try again.")

            displayed += max_results
            # Ask if the user wants to see more results
            if displayed < len(filtered_ingredient):
                show_more = input("\nDo you want to see more results? (y/n): ").strip().lower()
                if show_more != 'y':
                    break
            else:
                print("\nNo more results to show.")
    else:
        print("No recipes found with those ingredients.")


# Function to show a random recipe
def show_random_recipe():
    random_recipe = df.sample()  # Pick a random row
    recipe = random_recipe.iloc[0]  # Extract the random recipe data
    print(f"\nRandom Recipe: {recipe['Title']}")
    print(f"Ingredients: {recipe['Ingredients']}")
    print(f"Instructions: {recipe['Instructions']}")

def main_menu():
    while True:
        print("\nRecipe Finder Menu:")
        print("1. Search by Title")
        print("2. Search by Ingredient")
        print("3. Show Random Recipe")
        print("4. Get Calories and Macronutrients per 100g")
        print("5. Get Calories and Macronutrients for Specific Grams")
        print("6. Exit")

        choice = input("\nChoose an option (1/2/3/4/5/6): ")

        if choice == "1":
            title = input("\nEnter a recipe title to search: ")
            search_by_title(title)
        elif choice == "2":
            ingredient = input("\nEnter an ingredient or multiple seperated by commas to search: ")
            search_by_ingredients(ingredient)
        elif choice == "3":
            show_random_recipe()
        elif choice == "4":
            ingredient = input("\nEnter a food item to get calories and macronutrients per 100g: ")
            result = get_calories_and_macros(ingredient)
            if isinstance(result, dict):
                print(f"\nNutritional Information for {ingredient} per 100g:")
                print(f"Calories: {result['calories']}")
                print(f"Protein: {result['protein']} g")
                print(f"Total Fat: {result['total_fat']} g")
                print(f"Carbohydrates: {result['carbohydrates']} g")
            else:
                print(result)

        elif choice == "5":
            ingredient = input("\nEnter a food item to get nutritional information for specific grams: ")
            grams = float(input("Enter the number of grams: "))
            result = get_calories_and_macros(ingredient)
            if isinstance(result, dict):
                # Scale macronutrients based on the grams input
                calories = grams_to_calories(grams, result['calories'])
                protein = (grams / 100) * result['protein']
                total_fat = (grams / 100) * result['total_fat']
                carbohydrates = (grams / 100) * result['carbohydrates']

                print(f"\nNutritional Information for {grams} grams of {ingredient}:")
                print(f"Calories: {calories:.2f}")
                print(f"Protein: {protein:.2f} g")
                print(f"Total Fat: {total_fat:.2f} g")
                print(f"Carbohydrates: {carbohydrates:.2f} g")

            else:
                print(result)

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()




    #CookingCat