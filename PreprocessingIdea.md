# Preprocessing


```mermaid
graph  TD;

A[Start: Upload Document]  -->  B{Detect File Type}

B  -->|DOCX/DOC|  C[Read file using python-docx]

B  -->|PDF|  D[Read file using pdfplumber]

  

D  -->  E[Analyze Content Type]

C  -->  E

  

E  -->|Text Found|  F[Store Extracted Text]

E  -->|Table Detected|  G{Is Table Recognizable as Text?}

E  -->|Image Found|  H[Extract Images]

  

G  -->|Yes|  I[Extract Table Directly]

G  -->|No|  J[Convert Table to Image & Apply OCR]

  

H  -->  K[Apply OCR on Images if Necessary]

  

I  -->  L[Organize the order]

J  -->  L

K  -->  L

F  -->  L

  

L  -->  M[Smart chunking technique]

M  -->  N[(Embedding, VectorDB)]
```

```mermaid
graph  TD;

A(start)  -->  C(Document Preprocessing);

subgraph  Chunking  Preprocessing

C  -->  D{Recursive Chunking?};

subgraph  Recursive  chunking

D  -->|Yes|  E(Split by Sections - Paragraphs - Sentences);

E  -->  H{Check Chunk Size};

H  -->|Too Large|  D;

H  -->|Optimal|  I(Store Initial Chunks + Attach Metadata);

end

  

subgraph  semantics  chunking

I  -->  J(Generate Embeddings: Sentence-BERT);

J  -->  K(Compute Cosine Similarity);

K  -->  L(Agglomerative Clustering);

L  -->  M{Merge Similar Chunks?};

M  -->|Yes|  N(Merge Chunks);

end

end

  

M  -->|No|  O(Store Final Chunks in VectorDB);

N  -->  O;

  

O  -->  Q(End Preprocessing step);

Q  -->  R(end)
```





## Usecase

-   **Use Cases**:
	-  ***Đã Xong***: Trả lời câu hỏi và trích đoạn được câu hỏi từ tài liệu nào. 
    -   ***Chắc chắn sẽ làm*** :
	    - Chatbot tích hợp vào website.
	    - CRUD được VectorDB: Cho các trường hợp cần thay đổi thông tin từ các tài liệu học. (preprocessing)
	    - History: Thread with multiple Gemini & multiple requests (xây dựng sau, cùng với web).
    - *** Đang đắn đo *** : 
	    -  Chatbot có thể tự tra mạng để trả lời các truy vấn(!?) 
	    -  Trích file ảnh 
	    - Trả lời: FAQs, courses, syllabus, prerequisite, giáo viên, học phần, ...), faculties, schedules,  tuyển sinh, Student Services,  hướng nghiệp khi **học viên** hỏi (Indentification) (UI + input data đa dạng)
	    - Trả các đường link truy cập TCU liên quan đến Users' req
		- Gọi các API để vẽ biểu đồ, flowchart trực quan visualisation tool(UI)
	-> Web_search, image_processing
		
