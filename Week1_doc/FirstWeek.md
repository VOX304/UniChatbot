
# Nhật ký thực tập

## Ngày 1 (Thứ Sáu, 07/03)

-   Chuẩn bị các project để thuyết trình cho anh Trung và team R&D .
-   Cài đặt lại con chatbot cũ (xây dựng đơn giản với API chatbot Gemini + prompt các câu giới thiệu thành phần sản phẩm + Chainlit).

## Ngày 2 -> 4 (Thứ Hai - Thứ Tư)

### Ý tưởng chatbot cho trường SQTT

-   **Input** các file liên quan đến tư vấn tuyển sinh thuộc các định dạng: `.pdf`, `.doc`, `.docx`, `.md`, `.csv`, ...
-   **Non-functional Requirements**:
    -   Có khả năng scalability với số lượng các doc cho chatbot học càng ngày càng tăng.
    -   Fast: Phù hợp với server nhà trường.
    -   Có khả năng ghi nhớ.
-   **Mô hình RAG** (sau khi tổng hợp được ý tưởng và đã thực hành ít nhiều).
-   **Use Cases**:
    -   Chatbot tích hợp vào website.
    -   Trả lời câu hỏi và trích đoạn được câu hỏi từ tài liệu nào.
    -   CRUD được VectorDB: Cho các trường hợp cần thay đổi thông tin từ các tài liệu học.
    -   History: Thread + async (xây dựng sau, cùng với web).

### Xây dựng phương án

-   **Chatbot chỉ feed các Doc (không hỗ trợ Retrieve)**: Không khả thi -> Tốn quá nhiều token, và tài liệu feed cho chatbot có giới hạn.
-   **Được anh Trung gợi ý**: VectorDB + LLM --> **RAG (Retrieval Augmented Generation)**:
    -   Hiệu quả, chi phí token thấp.
    -   VectorDB có thể xây dựng sẵn và tách rời với LLM (chi phí cây nhà lá vườn -> không cao).
-   **Chốt phương án**.

### Mô hình và các kiến thức xoay quanh phương án đã chọn

-   **RAG**: Mô hình tăng cường trích xuất, hỗ trợ các thông tin trích xuất {knowledge base} để cho mô hình LLM có thể nhanh chóng tìm được các thông tin liên quan đến câu hỏi của người dùng {Query} mà không phải đưa raw_data cho LLM tự xử lý.
-   **Mối quan hệ giữa Reranker, VectorDB và LLM**:  (Phần Reranker hiện vẫn chưa được áp dụng, sẽ khảo sát tính khả thi)
- ![Simplest Method to improve RAG pipeline: Re-Ranking](https://blog.lancedb.com/content/images/2024/02/1_u4wm-Jn1ZnGhSxxhBLx_CA.webp)
-   **Các kiến thức xoay quanh chatbot**:
    -   Token limitation.
    -   Embeddings (numerical representations - relating to meaning and relationship of a specific context).
    -   Prompting.
    -   Temperature (randomness, creativity).

### Bước đầu bắt tay xây dựng chatbot

-   Được anh Nhân cho xem ké code -> Xây dựng **RAG_SQTT** dựa trên công thức thập cẩm (code a Nhân + hướng dẫn LangChain `augment_prompt` function + GitHub).
-   Bắt đầu triển khai chatbot.

## Code RAG: https://colab.research.google.com/drive/1ADCm-zZQSXmbMmWUl-_EBcHF3eSCQB8-?usp=sharing


# Ngày 5 - 6 (Thứ Năm - Thứ Sáu)

## Pipeline của code RAG: vẽ sơ flowchart

Doc (.pdf) → PyMuPDF (preprocessing) → Chungking + GGtxtEmbedding 4 → Faiss (VectorDB) ↔ LLM (user's query)
```mermaid
sequenceDiagram

participant  User  as  User

participant  Admin  as  Admin

participant  System  as  DBSystem

participant  LLM  as  Large  Language  Model (LLM)

loop  when  CRUD  knowledge  base:

Admin  ->>  System: Upload / Modify / Delete PDF

System  ->>  System: Preprocess PDF using PyMuPDF

System  ->>  System: Segment & Chunk Text

System  ->>  System: Convert Text to Embeddings (Google Text-embedding-004)

System  ->>  System: Update VectorDB (Store / Modify / Delete Embeddings)

end

loop  when  query  appear:

User  ->>  System: Submit Query

System  ->>  System: Perform Similarity Search in VectorDB

System  ->>  LLM: Generate Response using LLM

LLM  -->>  System: Return Generated Response

System  ->>  User: Display Response

end
 ```


## Các vấn đề đặt ra

- **Preprocessing**: Xử lý được đầu vào các file (.pdf) để trích xuất dữ liệu trọn vẹn nhất. Xử lý file Tiếng Việt -> cần các model đã đc huấn luyện TV 
- **Tạo từng file testcases (bằng chatbot)** để kiểm tra knowledge base có sẵn.
  - Lưu ý thêm cho testcases: Đã thử tìm kiếm nhưng không kiếm được các testcase có sẵn cho việc questioning và answering của chatbot.

Sau khi hoàn thành được 1 pipeline hoàn chỉnh: tối ưu hóa từng phần bằng cách thử nghiệm các Model khác nhau (trong Preprocessing, Embedding, (Ranker), VectorDB, LLMs)

### Các kiến thức lượm lặt trong quá trình phát hiện vấn đề:
- **Embeddings**: n-dimensional space để lưu trữ các vector dữ liệu, vector là các dữ liệu được số hóa theo n-dimension.
  - Các dạng Embedding: 
    - `Freq`: thông tin và mức độ quan trọng dựa trên số lần xuất hiện.
    - `Contextual`: các ngữ nghĩa khác nhau của 1 context.
    - `Prediction`: mức độ liên quan giữa các context với nhau.
- **VectorDB**: Indexing (đánh dấu) và Storing (lưu trữ) các vector embeddings -> fast retrieval + similarity search.
- **Transformer**: mô hình xử lý các bài toán NLP (natural language processing), semi-supervised learning.
- **Sentence Transformer**: fine-tuned embedding model.

### Xử lý vấn đề với các file .pdf (pdf-preprocessing):
Các file cho chatbot SQTT thường sẽ có các văn bản hành chính tiếng Việt. Trong trường hợp các file lưu dưới định dạng image hoặc các định dạng của pdf mà MarkItDown, PyMuPDF hay PDFPlumber không xử lý được -> mất chữ, thiếu dấu -> mất thông tin. Pipeline dưới đây nhằm giải quyết vấn đề đó:

```mermaid
graph TD;
    A["Start"] -->|Load PDF| B{"PDF Type?"};
    B -->|Text-based - Plaintext and Tables| C["Extract Text using PyMuPDF"];
    B -->|Image-based - Scanned/Embedded Images| G["Extract Images using PyMuPDF"];
    C --> D{"Contains Tables?"};
    D -->|Yes| E["Extract Tables using PDFPlumber or Camelot"];
    D -->|No| F["Save Structured Text"];
    E --> F;
    G --> H["Apply OCR with PaddleOCR"];
    H --> I["Refine Text with VietOCR"];
    I --> F;
    F --> M["Merge & Format Data"];
    M --> N["Text embedding"];
    N --> O["..."]; 
```
## RAG-PDF-Preprocessing.ipynb: https://colab.research.google.com/drive/1u_jdrmb-HF2MwJFkmWfSA-oitjhUgJHM?usp=sharing