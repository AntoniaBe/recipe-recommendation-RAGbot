# Recipe Recommendation RAGbot
A simple recipe recommendation RAGbot using OpenAI's models and LlamaIndex for document indexing and retrieval. The RAGbot analyzes an uploaded picture containing food, identifies the ingredients and recommends recipes. It can process recipe files in various formats (JSON, DOCX, PDF, CSV), transforms the text data into embeddings and stores them in a Pinecone vector database. Additionally, it generates a picture of the recommended dish using DALL·E. Streamlit is used for a simple user-friendly interface.


## Key Features

- Ingredient Extraction from Images: Utilizes OpenAI's GPT-4o with vision capabilities to extract ingredients from uploaded food pictures.
- Recipe Recommendations: Recommends recipes based on identified ingredients.
- Document Handling: Supports recipes in JSON, DOCX, PDF, and CSV formats.
- Embeddings Storage: Transforms recipe text data into embeddings and stores them in Pinecone.
- Image Generation: Creates images of recommended dishes using DALL·E.
- Streamlit Web App: User-friendly web interface for uploading images and viewing recommendations.

## Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.12.4 or higher
- OpenAI API key
- Pinecone API key

### Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/AntoniaBe/recipe-recommendation-RAGbot.git
cd recipe-recommendation-RAGbot
```

Set up a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application: 

```bash
python3 -m streamlit run ui.py
```

### Configuration
Export your API keys as an environment variable in constants.py :

- OPENAI_API_KEY= "your-openai-api-key"
- PINECONE_API_KEY = "your-pinecone-api-key"

---

Fridge images for testing are published by Freepik:
 - <a href="https://www.freepik.com/free-photo/assortment-healthy-food-fridge_15716207.htm#query=open%20fridge&position=10&from_view=keyword&track=ais_user&uuid=2459dac2-e209-47d6-bcff-33a2fc65094b">assortment-healthy-food-fridge</a>
 - <a href="https://www.freepik.com/free-photo/arrangement-different-foods-organized-fridge_18392053.htm#query=open%20fridge&position=3&from_view=keyword&track=ais_user&uuid=2459dac2-e209-47d6-bcff-33a2fc65094b">arrangement-different-foods-organized-fridge</a>