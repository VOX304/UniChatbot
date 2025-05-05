# Nhật ký thực tập tuần 3
## Thứ 2 - 3 - 4 - 5 - 6 - 7 - Cn 
### 1) Công việc đã hoàn thành
- Bấm đầu dây mạng, đi lại đường dây điện, đi đường dây mạng, kiểm tra modem, dán nhãn các đường dây, dọn dẹp -> chuẩn bị Workshop cho lễ đón tiếp Đ/c Thượng tướng Nguyễn Trọng Nghĩa, Bí thư Trung ương Đảng, Ủy viên Bộ Chính Trị, Trưởng ban Tuyên giáo và Dân vận Trung Ương. (Chiều t4 + t5, t6, t7, sáng Cn)
- Code xong img-preprocessing, sử dụng (Yolov8 + PaddleOCR) để lấy dữ liệu trong ảnh bao gồm: object detection và OCR
- Code xong table-preprocessing(pdf), sử dụng (Yolov8 table detection + img2table, PaddleOCR) để trích các bảng trong các file pdf bị hỏng định dạng (encoding)

### 2) Các ý tưởng mới
#### 2.1) Bức tranh preprocessing cuối cùng: 
- là 1 công cụ với đầy đủ UI và 1 database có khả năng quản lý các docs (CRUD) và xử lý dữ liệu tự động để đưa ra file VectorDB
- **Các giai đoạn để hoàn thành**
	- Hoàn thành các phần preprocessing components riêng lẻ bao gồm txt-prep, img-prep, table-prep(2 loại), chunking_tech để ouput ra preprocessED data (sử dụng trên ggColab) và ra được remote Faiss
	- 1 flow preprocessing hoàn chỉnh, không cần xử lý tay và ghép dữ liệu, tự ra được Faiss (localhost, chưa có Database quản lý)
	- Localhost + database quản lý

### 2.2) Các cách preprocessing bổ sung:
- img-preprocessing: sử dụng gemini-2.0-flash-thinking để đọc file ảnh và output content, sau đó dùng content để embeddings
- table-preprocessing: accent restoration và txt-normalization (pyvi +VnCoreNLP) để khôi phục các ký tự trong văn bản bị mất (chi phí O(n^2)). Kết hợp heuristic technique để định ra quy tắc cho bảng.
- Áp dụng Chunking technique: document-specific + semantics technique và metadata -> kỹ thuật chunking vẫn giữ được sự tương quan của từng dòng, đoạn, câu đối với văn bản.
	
