import chainlit as cl
import os
import itertools
from Retrieval import augment_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import asyncio

# Load API keys từ biến môi trường
GOOGLE_API_KEYS = [
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2"),
]

gemini_models = itertools.cycle([
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[0], model="gemini-2.0-flash-thinking-exp-01-21", temperature=0.7),
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[1], model="gemini-2.0-pro-exp-02-05", temperature=0.7),
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[0], model="gemini-2.0-flash-thinking-exp-01-21", temperature=0.7),
    ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEYS[1], model="gemini-2.0-pro-exp-02-05", temperature=0.7),
])

# Lưu lịch sử hội thoại của người dùng
user_histories = {}

@cl.on_chat_start
async def main():
    await cl.Message(content="🎓 Xin chào! Tôi là Uni-chatbot của Trường Sĩ Quan Thông Tin. Bạn cần giúp gì?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_id = message.author  
    query = message.content.strip().lower()

    # Xử lý yêu cầu thoát
    if query in ['bye', 'tạm biệt', 'exit']:
        res = await cl.AskActionMessage(
            content="📊 Bạn có hài lòng với câu trả lời của tôi không?",
            actions=[
                cl.Action(name="YES", value="YES", label="👍 Có"),
                cl.Action(name="NO", value="NO", label="👎 Không")
            ]
        )
        if res:
            await cl.Message(content=f"🙏 Cảm ơn phản hồi của bạn: {res['value']}!").send()
        return

    # Lưu lịch sử tin nhắn
    if user_id not in user_histories:
        user_histories[user_id] = []
    user_histories[user_id].append({"role": "user", "content": query})

    # 🔹 Gọi `augment_prompt()` với lịch sử hội thoại
    augmented_prompt, source_map = augment_prompt(query, user_histories[user_id])

    # Chọn mô hình Gemini (luân phiên)
    gemini = next(gemini_models)

    # Tạo prompt cho Gemini
    prompt = HumanMessage(content=augmented_prompt)

    # Gửi tin nhắn rỗng trước để chuẩn bị streaming
    msg = cl.Message(content="")
    await msg.send()

    # 🔹 Streaming phản hồi từ Gemini
    response_text = ""
    async for chunk in gemini.astream([prompt]):
        if chunk.content:
            await msg.stream_token(chunk.content)
            response_text += chunk.content  

    # Lưu phản hồi vào lịch sử hội thoại
    user_histories[user_id].append({"role": "assistant", "content": response_text})

    # 🔹 Hiển thị nguồn tài liệu sau khi hoàn tất câu trả lời
    sources = [f"{source} (Trang {page+1})" for text, (source, page) in source_map.items()]
    sources_text = "\n".join(sources) if sources else "Không có tài liệu phù hợp."
    await cl.Message(content=f"**📚 Nguồn tài liệu:**\n{sources_text}").send()
    
    # Cập nhật sidebar với lịch sử hội thoại mới nhất
    await update_sidebar(user_id)

async def update_sidebar(user_id):
    """
    Cập nhật lịch sử hội thoại trong sidebar.
    """
    sidebar_content = ""
    for message in user_histories[user_id]:
        role = "👨‍🎓 Sinh viên" if message["role"] == "user" else "🤖 Uni-chatbot"
        sidebar_content += f"**{role}:** {message['content']}\n\n"

    await cl.Sidebar(content=sidebar_content).send()

# Chạy Chainlit app
if __name__ == "__main__":
    cl.run(port=8000)  # ✅ Sử dụng `cl.run()` thay vì `cl.main()`
