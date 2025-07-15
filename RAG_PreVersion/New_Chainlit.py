import os
import re
import chainlit as cl
import asyncio
import itertools
from dotenv import load_dotenv
import IntentClassifer_QueryParaphrasing as icqp
import Retrieval
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()
GOOGLE_API_KEYS = [
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2")
]

# Initialize Gemini Models for load balancing
gemini_models = itertools.cycle([
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[0], model="gemini-2.0-flash-lite", temperature=0.2),
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[1], model="gemini-2.0-flash-lite", temperature=0.2)
])

# User conversation history
user_histories = {}

@cl.on_chat_start
async def start_chat():
    """
    Triggered when a new chat starts.
    """
    await cl.Message(content="🎓 Chào bạn! Tôi là Chatbot trường Sĩ quan Thông tin, tôi có thể giúp gì cho bạn hôm nay?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """
    Handles incoming messages from the user.
    """
    user_id = message.author
    query = message.content.strip()

    # Initialize user history if not present
    if user_id not in user_histories:
        user_histories[user_id] = []

    # Append user query to history
    user_histories[user_id].append({"role": "user", "content": query})

    # Select Gemini model
    gemini = next(gemini_models)

    try:
        # Process query using the unified logic
        response = await process_query(query, gemini)

        # Send response
        msg = cl.Message(content="")
        await msg.send()

        # Stream response
        async for chunk in stream_response(response):
            await msg.stream_token(chunk)

        # Save assistant response to history
        user_histories[user_id].append({"role": "assistant", "content": response})

    except Exception as e:
        print(f"Error: {e}")
        await cl.Message(content="Đã xảy ra lỗi trong quá trình xử lý yêu cầu.").send()

async def process_query(query: str, llm) -> str:
    """
    Process the user query by classifying intent and handling response based on intent.
    """
    # Classify the intent
    intent = icqp.classify_intent(query, llm)
    print(f"Classified Intent: {intent}")

    # Handle non-vital intents directly
    if intent in ["chit_chat", "greetings", "ambiguous"]:
        return icqp.handle_non_vital_intents(intent, query, llm)

    elif intent == "general_info":
        return icqp.handle_general_questions(llm)

    # Handle information retrieval intents
    elif intent in ["school_admission", "school_infrastructure", "school_contact", "health_check", "school_major"]:
        # Ensure that the coroutine is awaited properly
        response = await Retrieval.handle_information_retrieval(query)
        return response

    return "Intent not recognized."

async def stream_response(response_text: str):
    # pattern (\s+) sẽ bắt giữ cả spaces và newlines
    parts = re.split(r'(\s+)', response_text)
    for part in parts:
        await asyncio.sleep(0.02)
        yield part

# Run the Chainlit app
if __name__ == "__main__":
    cl.run(port=8000)
