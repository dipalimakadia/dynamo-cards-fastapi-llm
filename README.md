# DynamoCards-LLM-FastAPI-Axios

## Task 1:  Set up a Google Cloud Account

Set up Google Cloud for your projects seamlessly! Follow steps to create an account, project, and service account with owner permissions. Then, securely configure your environment by placing the service account key in your workspace and setting up the environment variable.

step1: create gcloud

## Task 2: Create a Github repository

Set up your project with ease! Follow steps to create a GitHub repository, frontend, and backend directories. Initialize a React app in the frontend and a Python virtual environment in the backend. Install necessary dependencies and generate a requirements.txt file for smooth development.

step 1: create frontend, backend folder
step 2:  npm create vite@latest dynamocards
select react and javascript
step 3:  cd dynamocard then npm install 
backend
step 4: python -m venv env
step 5: touch main.py
step 5 : env\Scripts\activate
step 6: pip install langchain langchain-community langchain-google-vertexai youtube-transcript-api pytube tiktoken

## Task 3: Develop a FastAPI app

Build a robust FastAPI app for YouTube video analysis! Utilize pydantic to validate input fields, create an endpoint to analyze videos, and test it locally with uvicorn. Retrieve the full transcript of the video using langchain-community and return specific data from the endpoint response.

step 1: add fastapi
uvicorn
step 2: pip install -r requirements.txt
step3: uvicorn main:app --reloadcheck http://127.0.0.1:8000/docs

## Task 4: Allow cross-origin requests using CORSMiddleware

Enable seamless communication between frontend and backend!  Utilize CORSMiddleware to allow cross-origin requests and install Axios to handle video analysis requests. Create a route to send links to the backend endpoint and handle responses to display data in the frontend. Test the integration by enabling both servers and sending requests from the frontend.

created frontend
react and axios and connected frontend and backend

## Task 5: Organize Tools and Functions

Organize your generative AI tools and functions neatly! Create a 'services' folder and migrate video analysis functionalities into a class for processing YouTube videos. Configure logging for verbosity to enhance debugging. 

created genai.py

## Task 6:  Import Generative AI Classes

Enhance your generative AI tools with langchain integration! Create a GeminiProcessor class in genai.py, utilizing load_summarize_chain and VertexAI classes. Implement a generate_document_summary method to summarize documents with configurable verbosity. Integrate with the main.py file to utilize the GeminiProcessor class and test the integration by enabling both frontend and backend servers.

added vertex ai, llm, map reduce and gcloud

## Task 7: Enhance the YouTube Processing Class 

Enhance YouTube video analysis with key  concept identification! 📝 Add a find_key_concepts method to the YoutubeProcessor class, checking group size validity and splitting documents into groups. Create prompt templates to define key concepts, then use GeminiProcessor to extract concepts. Modify the endpoint to return key concepts and integrate genai_processor with YoutubeProcessor.

import tqdm

##Task 8: Billing Character Calculation Enhancement

Enhance cost tracking and verbosity in your AI tools!  Modify the count_total_tokens method in GeminiProcessor to calculate billable characters. Update YoutubeProcessor to log billable characters in retrieve_youtube_documents and find_key_concepts methods, providing cost insights with verbosity control.

##Task 9: Key Concept Refactoring and Output Formatting

Fine-tune key concept identification for improved usability! Rename group_size to sample_size and handle num_docs_per_group validations. Adjust defaults for sample_size and provide feedback on output quality. Modify prompt template for JSON response format. Convert JSON strings to Python Dicts before returning key concepts.

##Task 10: Frontend Integration and Flashcard Handling

Enhance frontend functionality for seamless interaction!  Update sendLink method in App.jsx to manage key_concepts state and handle response data variations. Implement a discardFlashcard function to remove flashcards, enhancing user control. Modify Flashcard component to include onDiscard functionality for efficient flashcard management.
