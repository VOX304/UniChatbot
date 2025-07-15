from langchain.schema import HumanMessage
from typing import List

# Function to classify intent using Gemini LLM
def classify_intent(query: str, llm) -> str:
    """
    Classify the user query into one of the predefined intent categories using the Gemini LLM.
    Intents:
    - admission
    - school_contact
    - health_check
    - school_major
    - chit&chat
    - greetings
    
    Args:
        query (str): The user query in Vietnamese.
        llm: The LLM object (e.g., ChatGoogleGenerativeAI).

    Returns:
        str: The predicted intent.
    """
    # Prompt template for intent classification
    prompt = f"""
    Bạn là trợ lý ảo của trường Sĩ Quan Thông Tin. 
    Hãy phân loại câu hỏi sau thành một trong các ý định sau: 
    - general_info: Câu hỏi về thông tin chung, bạn có thông tin gì, bạn có thể giúp gì, trường cung cấp những thông tin gì
    - school_admission: Câu hỏi về tuyển sinh, đăng ký, thủ tục nhập học
    - school_infrastructure: Câu hỏi về cơ sở vật chất, trang thiết bị của trường
    - school_contact: Câu hỏi về thông tin liên hệ, địa chỉ, số điện thoại, trang mạng của trường
    - health_check: Câu hỏi về kiểm tra sức khỏe, y tế
    - school_major: Câu hỏi về ngành học, chương trình đào tạo
    - chit_chat: Câu hỏi mang tính chất trò chuyện, tán gẫu, không liên quan đến thông tin trường
    - greetings: Câu hỏi chào hỏi, cảm ơn, chê trách, tạm biệt
    - ambiguous: Câu hỏi không rõ ý định, cần người dùng làm rõ
    
    Câu hỏi: "{query}"
    
    Nếu không xác định rõ ý định, trả về nhãn 'ambiguous'.
    Hãy chỉ trả về đúng 1 nhãn ý định từ danh sách trên.
    """

    # Send the prompt to Gemini
    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.strip()
    
    return intent

def handle_non_vital_intents(intent: str, query: str, llm) -> str:
    """
    Handle non-vital intents (chit_chat, greetings, ambiguous).
    """
        # Define the prompt for Gemini to handle non-vital intents
    prompt = f"""
    Bạn là trợ lý ảo của trường Sĩ Quan Thông Tin. 
    Hãy phản hồi phù hợp với ý định sau đây:
    - chit_chat: Trả lời một cách tự nhiên theo tình huống.
    - greetings: Đáp lại lời chào hỏi và hỏi thăm.
    - ambiguous: Yêu cầu người dùng làm rõ câu hỏi để có thể trả lời chính xác.

    Hãy nhớ bạn là trợ lý ảo của trường Sĩ Quan Thông Tin. 
    Khi người dùng hỏi những gì khác ngoài thông tin mà bạn có thể cung cấp dưới đây:

    - Tuyển sinh
    - Liên hệ
    - Cơ sở vật chất
    - Kiểm tra sức khỏe
    - Ngành học

    Hãy trả lời ngắn gọn và tự nhiên, và khuyến khích người dùng hỏi những gì liên quan đến trường. 

    Ý định: {intent}
    Câu hỏi: "{query}"
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def handle_general_questions(llm) -> str:
    """
    Provide an overview of the information and services the chatbot can assist with.
    """
    response = """
    Chào bạn! Tôi là trợ lý ảo của Trường Sĩ quan Thông tin. Rất vui được hỗ trợ bạn!
    Tôi có thể cung cấp cho bạn những thông tin sau:

    - Tuyển sinh: Điều kiện, quy trình đăng ký, các ngành học
    - Liên hệ: Địa chỉ, số điện thoại, email của trường
    - Cơ sở vật chất: Ký túc xá, thư viện, phòng thí nghiệm
    - Kiểm tra sức khỏe: Các quy định và thủ tục kiểm tra sức khỏe
    - Ngành học: Thông tin về các ngành đào tạo, chương trình học
    - Hỗ trợ trò chuyện: Giao tiếp thân thiện, hỏi đáp thông tin chung

    Bạn quan tâm đến thông tin nào nhất? Hãy cứ hỏi, tôi sẽ cố gắng cung cấp thông tin chi tiết nhất có thể!
    """
    return response

#sẽ bổ sung thêm tìm kiếm từ khóa + tìm kiếm câu có cùng ý nghĩa
def generate_paraphrases(query: str, llm, num_variants: int = 3) -> List[str]:
    """
    Use Gemini to produce num_variants paraphrases of the input Vietnamese query.
    """
    prompt = f"""
    Bạn là mô hình hệ thống hiểu ngôn ngữ tự nhiên của trường Sĩ Quan Thông Tin. 
    Hãy tạo {num_variants} câu hỏi khác diễn đạt cùng ý nghĩa với câu sau, 
    mỗi câu đánh số từ 1 đến {num_variants} và dùng cấu trúc khác nhau, sao cho rõ các từ khóa và ý nghĩa của câu hỏi:
    "{query}"
    """
    # Invoke Gemini via LangChain
    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content.strip().split("\n")
    
    # Parse lines like "1. …", "2. …"
    paraphrases = []
    for line in raw:
        if line and (line[0].isdigit() and line[1] in {".", ")"}):
            paraphrases.append(line.split(maxsplit=1)[1])
    return paraphrases
