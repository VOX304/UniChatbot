import os
import IntentClassifer_QueryParaphrasing as icqp
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import Retrieval

# Load environment variables
load_dotenv()
GOOGLE_API_KEY_1 = os.getenv("GOOGLE_API_KEY_1")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY_1,
    model="gemini-2.0-flash-lite",
    temperature=0.2
)

def process_query(query: str) -> str:
    """
    Process the user query by classifying intent and handling response based on intent.
    """
    # Classify the intent
    intent = icqp.classify_intent(query, llm)
    print(f"Classified Intent: {intent}")
    
    # Handle non-vital intents directly
    if intent in ["chit_chat", "greetings", "ambiguous"]:
        return icqp.handle_non_vital_intents(intent, llm)
    
    elif intent == "general_info":
        return icqp.handle_general_questions(llm)
    # For information retrieval intents, generate paraphrases
    
    elif intent in ["school_admission", "school_infrastructure", "school_contact", "health_check", "school_major"]:
        response = Retrieval.handle_information_retrieval("Thông tin tuyển sinh của trường là gì?")
        return response
    
    return "Intent not recognized."

# Example usage
if __name__ == "__main__":
    test_query = "Bạn có thể cho tôi biết thông tin về tuyển sinh trường Thông tin không?"
    response = process_query(test_query)
    print(response)
