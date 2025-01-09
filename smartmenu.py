import streamlit as st
import openai
import os

# Streamlit app title
st.title("Welcome to Food Dish Description Expert")

# Introduction and examples
st.write(
    """This GPT is a Food Dish Description Expert, providing concise and highly accurate descriptions of food dishes. 
    Descriptions are limited to 250 characters and highlight the main ingredients, flavor profile, or cultural essence of the dish.

    ### Examples:
    **Dish Name:** Paneer Butter Masala  
    **Description:** A creamy North Indian curry featuring soft paneer cubes simmered in a rich, velvety tomato-based gravy infused with butter, aromatic spices, and a hint of sweetness. Perfect with naan or basmati rice for a flavorful, comforting meal.

    **Dish Name:** Sushi  
    **Description:** Delicate Japanese dish featuring vinegared rice paired with fresh seafood, vegetables, or egg, often wrapped in seaweed. Balanced flavors and textures celebrate the art of simplicity.

    Use this tool to create engaging menu descriptions, enhance food blogs, or craft mouthwatering food captions. Provide the dish name and optional ingredients below, then click "Generate Description" to get started!
    """
)

# Fetch the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Error: OpenAI API key not found. Please set it as an environment variable.")
else:
    # User input: Dish name
    dish_name = st.text_input("Enter the name of the dish:")

    # User input: Ingredients (optional)
    ingredients = st.text_area("Enter the list of ingredients (optional):", height=100)

    # Generate description button
    if st.button("Generate Description"):
        if dish_name.strip():
            # Function to generate food dish description
            def generate_dish_description(api_key, dish_name, ingredients):
                """
                Generates a concise and engaging description for the given dish.

                Parameters:
                    api_key (str): OpenAI API key.
                    dish_name (str): The name of the dish.
                    ingredients (str): Optional ingredients list.

                Returns:
                    str: A formatted description for the dish.
                """
                openai.api_key = api_key

                prompt = (
                    "You are a Food Dish Description Expert. Your task is to generate concise, highly accurate descriptions of food dishes. "
                    "Descriptions should highlight the main ingredients, flavor profile, or cultural essence of the dish and be no longer than 250 characters. "
                    "Responses must be formatted as follows: \n"
                    "**Dish Name:** followed by the name, and **Description:** followed by the text. \n"
                    f"Dish Name: {dish_name}\n"
                )

                if ingredients.strip():
                    prompt += f"Ingredients: {ingredients}\n"

                prompt += "Write the description:"

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert at generating food dish descriptions."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=150
                    )

                    description = response.choices[0].message.content.strip()
                    return description

                except openai.error.OpenAIError as e:
                    return f"Error generating description: {str(e)}"

            # Generate and display the description
            description = generate_dish_description(api_key, dish_name, ingredients)
            st.subheader("Generated Description:")
            st.write(description)
        else:
            st.error("Dish name cannot be empty. Please enter a dish name.")
