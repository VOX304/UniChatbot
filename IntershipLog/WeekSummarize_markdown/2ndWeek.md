
# Nhật ký thực tập tuần 2

## Kiến thức mới: 

### Encoder
	- Encoders: Transform text to (Numerical representation = Semantic meaning to System)
	- 2 loại 
		+ Bi-encoder (Encoding các câu vào trong vector
		space của Embeddings) 
		+ Cross encoder(Encoding từng câu theo cặp, để so
		sánh kĩ lưỡng giá trị tương đồng của từng cặp)
	- Bi-end: Fast Retrieval -> Embeddings
	- Cross-end: High accuracy -> Reranker
-> Quyết định thêm Reranker, O(n*d): n = input token, d =vector dimension, chi phí vừa phải và tăng độ chính cao

### Các kiến thức về RAG
1. RAG:  Tăng cường truy xuất, 2 thành phần chính: Retriever + LLM 
2. Knowledge base: 2 loại: structured(graph, database), unstructured(txt, doc, pdf)
3. Prombt editting: tùy chỉnh dòng lệnh feed cho LLM
4. Retrieval method: phương pháp truy xuất, 2 phương pháp: sparse (rải rác, tìm keywords) và dense(dày đặc, tìm Vector embedding tương đồng)
5. Evaluate RAG: Bleu & Rouge
6. Unclear query: xử lý truy vấn mơ hồ bằng cách tái cấu trúc câu hoặc sử dụng NLU - natural language understading
7.  Corrective RAG: Webserch + accuracy_point -> tự kiểm tra độ chính xác của thông tin
8.  Late chunking: chunking trong lúc processing

## Các nhiệm vụ xử lý trong tuần: 
### Processing:
1. Thêm vào luồng Vietnamese_doc_embedding(Embedding) và PhoRanker(reranker). 
2. Cài đặt chainlit-UI cho chatbot (trong video và link): https://github.com/VOX304/SchoolChatbot/tree/main/Processing
3. Nghiên cứu kết hợp các mô hình advanced RAG vào chatbot (đang rất phân vân)
4.  Kịch bản trả lời: https://github.com/VOX304/SchoolChatbot/blob/main/Processing/Chatbot_script.md
5. Luồng hiện tại: readme.md

**Chú thích thêm cho phần cài đặt chatbot**:
-	 Preprocessing: phương pháp preprocessing gần như không đổi (ngoại trừ: các file doc -> docx và đọc docx) và chunking trên Google Colab
-	Tải các file của Vector Database Faiss về và load vào local
-	sử dụng chainlit + 4 mô hình Gemini (sử dụng thread và xoay vòng) -> tương đương có thể xử lý nhiều request/ min và vài nghìn request / day 

### Preprocessing: (trên ý tưởng)
1.  Cả luồng bao gồm Doc preprocessing và Chunk preprocessing: https://github.com/VOX304/SchoolChatbot/blob/main/Preprocessing/PreprocessingIdea.md
2. Các kỹ thuật cho từng dạng dữ liệu: https://github.com/VOX304/SchoolChatbot/blob/main/Preprocessing/PreprocessingIdea.md
3. Code lưng chừng: https://github.com/VOX304/SchoolChatbot/tree/main/Preprocessing/Colab_preprocessing

## Vấn đề khúc mắc
- Cài đặt và hiểu các mô hình RAG - chatbot cơ bản: Về cơ bản đã hoàn thành
- Tuy nhiên cần xác định kĩ bài toán để cải thiện các kĩ thuật cho mô hình, ví dụ: 
	+ Xác định bài toán: bài toán nhằm **mô tả thông tin trường** hay nhằm **tư vấn tuyển sinh**. Trong mô tả thông tin trường, ta đơn thuần trích xuất các thông tin có trong các tài liệu (trường công bố hoặc chưa công bố) hay còn dựa vào thông tin đưa ra những đề xuất cho các cán bộ - viên chức, sinh viên trường . 
	+ Xác định đối tượng bài toán nhắm tới: Học sinh (ngoài trường), sinh viên (trong trường), cán bộ - viên chức, ...
	
