import streamlit as st
import openai
import os

# Streamlit app title
st.title("Welcome to Food Dish Description Expert")

# Fetch the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Error: OpenAI API key not found. Please set it as an environment variable.")
else:
    # User input: Dish name
    dish_name = st.text_input("Enter the name of the dish:")

    # Optional input: Dish ingredients or preparation method
    dish_details = st.text_input("Enter dish Ingredients/How to make (optional):")

    # Submit button
    if st.button("Submit"):
        if dish_name:
            # Function to generate food dish description
            def generate_dish_description(api_key, dish_name, dish_details):
                """
                Generates a concise and engaging description for the given dish.

                Parameters:
                    api_key (str): OpenAI API key.
                    dish_name (str): The name of the dish.
                    dish_details (str): Additional details about the dish (optional).

                Returns:
                    str: A formatted description for the dish.
                """
                openai.api_key = api_key

                prompt = (
                    "You are a Food Dish Description Expert. Your task is to generate concise, highly accurate descriptions of food dishes. "
                    "Descriptions should highlight the main ingredients, flavor profile, or cultural essence of the dish and be no longer than 250 characters. "
                    f"\nDish Name: {dish_name}"
                )

                if dish_details:
                    prompt += f"\nDish Details: {dish_details}"

                prompt += "\nWrite the description:"

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
            description = generate_dish_description(api_key, dish_name, dish_details)

            st.markdown("### **Dish Description**")
            st.markdown(f"**Dish Name:** {dish_name}")
            if dish_details:
                st.markdown(f"**Details Provided:** {dish_details}")
            st.markdown(f"**Description:** {description}")
        else:
            st.error("Dish name cannot be empty. Please enter a dish name.")
