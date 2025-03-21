# Vietnamese SchoolChatbot
Chatbot feeded by school's information

## Usecase

-   **Use Cases**:
	-  ***Đã Xong***: Trả lời câu hỏi và trích đoạn được câu hỏi từ tài liệu nào. 
    -   ***Chắc chắn sẽ làm*** :
	    - Chatbot tích hợp vào website. (UI)
     - History: Thread with multiple Gemini & multiple requests (xây dựng sau, cùng với web). (UI)
	    - CRUD được VectorDB: Cho các trường hợp cần thay đổi thông tin từ các tài liệu học. (preprocessing)
    - *** Đang đắn đo *** : 
	    -  Chatbot có thể tự tra mạng để trả lời các truy vấn(!?) 
	    -  Trích file ảnh 
	    - Trả lời: FAQs, courses, syllabus, prerequisite, giáo viên, học phần, ...), faculties, schedules,  tuyển sinh, Student Services,  hướng nghiệp khi **học viên** hỏi (Indentification) (UI + input data đa dạng)
	    - Trả các đường link truy cập TCU liên quan đến Users' req
		- Gọi các API để vẽ biểu đồ, flowchart trực quan visualisation tool(UI)
	-> Web_search, image_processing

```mermaid
sequenceDiagram

participant  User  as  User

participant  Sys  as  System

participant  VecDB as  DBSystem(Faiss)

participant  LLM  as  Large  Language  Model (Gemini 2.0)

participant RR as ReRanker(PhoRanker)

loop  when  CRUD  knowledge  base:

Sys  ->> VecDB: Upload / Modify / Delete PDF

VecDB ->> VecDB: Preprocess PDF using PyMuPDF

VecDB ->> VecDB: Segment & Chunk Text

VecDB ->> VecDB: Convert Text to Embeddings (vietnamese-document-embedding)

VecDB ->> VecDB: Update VectorDB 

VecDB ->> Sys: Return VectorDB 

end

loop  when  query  appear:

User  ->> Sys: Submit Query

Sys ->> VecDB: Send Query

Sys ->> VecDB: Call VecDB

VecDB ->> VecDB: Perform Similarity Search(Query)

VecDB ->> RR: send to ranker top nth(20 trunks)

Sys ->> RR: Send Query

RR ->> RR: Cross-encoder computation(Query + trunk)

RR ->> LLM: Top kth(3-4 trunks) best retriever


LLM  -->> Sys: Return Generated Response

Sys ->>  User: Display Response

end
 ```
