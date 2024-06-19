import streamlit as st
from vision import VisionClient
from dalle import DALLEClient
from ragbot import RagBot
import asyncio
import json

st.set_page_config(page_title="Recipe recommendations, powered by LlamaIndex", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)


bot = RagBot()
bot.load()

index = bot.index


async def format_recipes(recipes_data, dc):
    formatted_recipes = []
    for recipe in recipes_data:
        generated_recipe_image = await dc.generate_image({recipe['recipe_name']})     
        #generated_recipe_image = "https://dummyimage.com/600x400/000/fff"
        #print("recipe formatted", recipe)

        formatted_recipe = f"**Recipe Name:** {recipe["recipe_name"]}\n\n"
        formatted_recipe += "**Ingredients:**\n"
        for ingredient in recipe["recipe_ingredients"]:
            formatted_recipe += f"- {ingredient}\n"
        formatted_recipe += "\n**Instructions:**\n"
        for instruction in recipe["recipe_instructions"]:
            formatted_recipe += f"{instruction}\n"
        formatted_recipe += "\n"  # Newline for better readability
        formatted_recipes.append({
            "text": formatted_recipe,
            "image_url": generated_recipe_image
        })
    return formatted_recipes

async def build_response(image):

    vc = VisionClient()
    dc = DALLEClient()

    with st.spinner(text="Getting ingredients  – hang tight!"):
         
        data =  await vc.describe_image(vc.base64_image(image))
        
        data_json = json.loads(data)
        ingredients = data_json["ingredients"]
        recipes = data_json["recipes"]
         
        ingredientsList = '\n'.join(f"- {ingredient}" for ingredient in ingredients)

        # Add the ingredients to the session state messages
        st.session_state.messages.append({"role": "assistant", "content": f"Those are the ingredients:\n{ingredientsList}\n"})
    
        formatted_recipes = await format_recipes(recipes, dc)
        for recipe in formatted_recipes:
            st.session_state.messages.append({"role": "assistant", "content": recipe["text"]})
            st.session_state.messages.append({"type": "image", "url": recipe["image_url"]})


def uploader_callback():
    image =  st.session_state.file_uploader
    st.session_state.messages.append({"type": "image", "url": image})
    asyncio.run(build_response(image))

        
st.markdown("""
<style>
    h1 {
     font-size: 2.3rem;   
    }
    .exotz4b0 {
    white-space: unset;
    }
    [data-testid='stVerticalBlockBorderWrapper']:has([data-testid="stFileUploader"]){
    position: sticky;
    top: 40px;
    z-index: 99;
    background-color: rgb(14, 17, 23);
    width: 100%;
    padding-bottom: 20px;
    }
    }
            
</style>     
    """, unsafe_allow_html=True)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Let me find delicious recipes for you!"}
    ]

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(llm=bot.llm, chat_mode="condense_question", verbose=True)

# Erzeuge einen Container für den "Chat"
chat_container = st.container()

with chat_container: 
    st.title("RECIPE RECOMMENDATIONS RAGBOT 🥪")    
    st.text("Please upload an image containing ingredients. These will be analyzed to provide you with personalized recipe recommendations based on the ingredients detected.")
    st.text("Let's get started!")
    st.file_uploader(label="Choose an image!", on_change=uploader_callback, key="file_uploader", label_visibility='collapsed')
    #prompt = st.chat_input("Your question")# Prompt for user input and save to chat history


#if prompt: st.session_state.messages.append({"role": "user", "content": prompt})
# Display all the messages in the list
for message in st.session_state.messages:
    if "type" in message and message["type"] == "image":
        st.image(message["url"])
    elif "role" in message:
        with st.chat_message(message["role"]):
            st.write(message["content"])

#Check if there are any messages in the list before accessing the latest message
if st.session_state.messages and "role" in st.session_state.messages[-1] and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
elif not st.session_state.messages:
    # If there are no messages in the list, assume the user is starting a new conversation
    with st.chat_message("assistant"):
        st.write("Hi there! How can I help you today?")
        message = {"role": "assistant", "content": "Hi there! How can I help you today?"}
        st.session_state.messages.append(message) # Add greeting to message history
