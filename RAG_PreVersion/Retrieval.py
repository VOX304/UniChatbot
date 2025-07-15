import os
import numpy as np
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from langchain.schema import HumanMessage
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder  # ✅ NEW
import torch
from typing import List, Dict
import numpy as np
from IntentClassifer_QueryParaphrasing import generate_paraphrases



#print(f"Using device: {device}")


# Load environment variables
load_dotenv('.env')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY_1")


# Load FAISS VectorDB
faiss_db_path = "faiss_index"
embedding_model = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-document-embedding",
    model_kwargs={"trust_remote_code": True}  # ✅ Enable remote code execution
)
vector_db = FAISS.load_local(faiss_db_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

# Load PhoRanker model
cross_encoder = CrossEncoder("itdainb/PhoRanker")
tokenizer = AutoTokenizer.from_pretrained("itdainb/PhoRanker")

#device = torch.device("gpu")  # Force CPU usage
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSequenceClassification.from_pretrained("itdainb/PhoRanker").to(device)


# Example tensor
example_tensor = torch.tensor([1.0, 2.0, 3.0]).to(device)


# Load Gemini Model
chat_model = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY,
    model="gemini-2.0-flash-thinking-exp-01-21",
    temperature=0.7
)

def rerank_documents(query, docs):
    """Rerank retrieved documents using PhoRanker"""
    scored_docs = []
    for doc in docs:
        inputs = tokenizer(query, doc.page_content, return_tensors="pt", truncation=True, padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        score = outputs.logits[0][0].item()
        scored_docs.append((doc, score))

    # Sort documents by relevance score
    return [doc for doc, score in sorted(scored_docs, key=lambda x: x[1], reverse=True)][:4]


def augment_prompt(query, history):
    """Retrieve and rerank documents, then generate an augmented prompt including history."""
    candidates = vector_db.similarity_search(query, k=15)
    top_docs = rerank_documents(query, candidates)

    source_map = {}
    formatted_sources = []
    for idx, doc in enumerate(top_docs, start=1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")
        source_map[doc.page_content] = (source, page)
        formatted_sources.append(f"[{idx}] {source} - Trang {page}")

    source_knowledge = "\n\n".join(f"({i+1}) {doc.page_content}" for i, doc in enumerate(top_docs))
    citation_info = "\n".join(formatted_sources)

    # Format chat history
    history_text = "\n".join(f"👤 Người dùng: {h['content']}" if h["role"] == "user" else f"🤖 Trợ lý: {h['content']}" for h in history)

    # Construct the augmented prompt
    augmented_prompt = f"""Bạn là tư vấn viên của trường Sĩ Quan Thông Tin. Hãy trả lời câu hỏi một cách chính xác, thân thiện, và trích dẫn nguồn gốc thông tin, nếu cần thiết và có liên quan.
Bạn chỉ được sử dụng thông tin từ tài liệu dưới đây, không thêm nội dung không có trong tài liệu. Nếu không tìm thấy câu trả lời, chỉ cần nói rằng bạn không biết.

📝 **Lịch sử hội thoại**:
{history_text}

📌 **Nội dung tài liệu**:
{source_knowledge}

❓ **Câu hỏi hiện tại**:
{query}

📖 **Nguồn tài liệu**:
{citation_info}
"""
    return augmented_prompt, source_map


def answer_query(query, user_history):
    """Generate an answer using Gemini and extract relevant sources"""
    context, source_map = augment_prompt(query, user_history)
    prompt = HumanMessage(content=context)
    res = chat_model.invoke([prompt])
    response_text = res.content

    return {"response": response_text, "sources": source_map}


### ADD-ON FUNCTION: handle_information_retrieval

async def handle_information_retrieval(query: str) -> str:
    """
    Handle information retrieval and response generation using only the query parameter.

    Args:
        query (str): The user query in Vietnamese.

    Returns:
        str: The generated response from the LLM.
    """
    # Access the global instances of llm, vector_db, and rerank_fn
    llm = chat_model
    vector_db_instance = vector_db
    rerank_fn = rerank_documents

    # 1. Generate paraphrases
    variants = [query] + generate_paraphrases(query, llm, num_variants=3)

    # 2. Multi-query FAISS retrieval
    all_docs = []
    for q in variants:
        all_docs.extend(vector_db_instance.similarity_search(q, k=5))

    # 3. Deduplicate documents by content
    seen = set()
    unique_docs = []
    for doc in all_docs:
        key = doc.page_content.strip()[:200]
        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    # 4. Rerank with PhoRanker
    top_docs = rerank_fn(query, unique_docs)

    # 5. Construct document content
    source_knowledge = "\n\n".join(
        f"({i+1}) {doc.page_content}"
        for i, doc in enumerate(top_docs)
    )

    # 6. Construct prompt
    prompt = f"""Bạn là tư vấn viên của trường Sĩ Quan Thông Tin.
Hãy trả lời câu hỏi một cách chính xác và không thêm nội dung ngoài tài liệu.

📌 **Nội dung tài liệu**:
{source_knowledge}

❓ **Câu hỏi hiện tại**:
{query}
"""

    # 7. Generate response using Gemini
    res = await llm.ainvoke([HumanMessage(content=prompt)])
    return res.content.strip()


#-------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Example query
    response = handle_information_retrieval("Thông tin tuyển sinh của trường là gì?")
    print(f"\nResponse:\n{response}")
