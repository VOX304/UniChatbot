# 🧠 Vietnamese SchoolChatbot

> **Rasa RAG-powered Chatbot giúp sinh viên, giảng viên, cán bộ truy vấn thông tin nhà trường một cách thông minh, nhanh chóng, chính xác**

---

## 📘 Mô tả bài toán

Trong các trường đại học, việc tra cứu thông tin như chương trình học, lịch thi, biểu mẫu hành chính, thông tin tuyển sinh,... thường gây khó khăn cho cả **sinh viên** và **cán bộ, giảng viên** do:

- Cấu trúc website không trực quan
- Dữ liệu phân tán, thiếu liên kết
- Không phải ai cũng biết rõ nơi tra cứu đúng
- Văn bản mới, quy trình mới thường không cập nhật kịp đến người dùng

**Giải pháp đề xuất**: xây dựng một chatbot AI sử dụng mô hình Retrieval-Augmented Generation (RAG) kết hợp với Rasa để:

- Tự động trả lời thông minh bằng ngôn ngữ tự nhiên
- Truy xuất đúng thông tin gốc từ tài liệu của trường
- Cập nhật nhanh các quy trình, biểu mẫu, văn bản
- Không bị giới hạn bởi hiểu biết về cấu trúc trang web hay kỹ năng tìm kiếm

---

## ❓ Vấn đề & Yêu cầu

### 🔧 Non-Functional Requirements:
- **Độ chính xác cao**: Đảm bảo thông tin nhất quán, tối thiểu sai sót  
  → Cần kiểm thử kỹ & chuẩn hóa thông tin đầu vào
- **Tốc độ phản hồi nhanh**: <3s có phản hồi đầu tiên  
  → RAG + streaming output
- **Thông minh**: Trả lời linh hoạt các câu hỏi về tuyển sinh, lịch học, ngành học, giảng viên, dịch vụ sinh viên,...
- **Dễ duy trì**: Thiết kế dễ cập nhật, tương thích hệ thống hiện tại
- **Bảo mật**: Chưa xác định rõ – cần thiết kế bổ sung sau

### ✅ Functional Requirements:

#### 📄 Preprocessing
- Xử lý nhiều định dạng:
  - Structured: `.json`, `.csv`, `.xml`, `.md`
  - Unstructured: `.docx`, `.pdf`, `.txt`, ảnh (OCR)
- Trích xuất & chuyển đổi nội dung thành markdown có cấu trúc
- Chunking theo hierarchy + semantics
- VectorDB hỗ trợ CRUD (update khi thay đổi tài liệu)

#### ⚙️ Processing
- VectorDB: FAISS hoặc Chroma
- Re-Ranker: PhoRanker (cross-encoder)
- LLM: Gemini 2.0 Flash Lite (Google Generative AI)
- Tích hợp Rasa Pro:
  - Command Generator
  - FlowPolicy, IntentlessPolicy
  - Flow & Pattern YAML

---

## 📌 Use Cases

| Trạng thái       | Tính năng                                                                 |
|------------------|---------------------------------------------------------------------------|
| ✅ Đã hoàn thành | Trả lời câu hỏi + truy nguồn tài liệu                                     |
| 🔜 Sẽ làm        | Giao diện website, lịch sử hội thoại, CRUD VectorDB, gợi ý câu hỏi        |
| 🤔 Đắn đo        | Web search, trích ảnh, trả lời chuyên sâu, vẽ biểu đồ, trả link TCU,...   |

---

## 🔁 Quy trình xử lý chính

```mermaid
sequenceDiagram

participant User as User
participant Sys as System
participant VecDB as DBSystem(Faiss)
participant LLM as Large Language Model (Gemini 2.0)
participant RR as ReRanker(PhoRanker)

loop when CRUD knowledge base:
  Sys ->> VecDB: Upload / Modify / Delete PDF
  VecDB ->> VecDB: Preprocess PDF using PyMuPDF
  VecDB ->> VecDB: Segment & Chunk Text
  VecDB ->> VecDB: Convert Text to Embeddings (vietnamese-document-embedding)
  VecDB ->> VecDB: Update VectorDB
  VecDB ->> Sys: Return VectorDB
end

loop when query appear:
  User ->> Sys: Submit Query
  Sys ->> VecDB: Send Query
  Sys ->> VecDB: Call VecDB
  VecDB ->> VecDB: Perform Similarity Search(Query)
  VecDB ->> RR: send to ranker top nth(20 trunks)
  Sys ->> RR: Send Query
  RR ->> RR: Cross-encoder computation(Query + trunk)
  RR ->> LLM: Top kth(3-4 trunks) best retriever
  LLM -->> Sys: Return Generated Response
  Sys ->> User: Display Response
end
