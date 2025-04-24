# Nhật ký thực tập tuần 4

## Các tác vụ theo từng ngày: 

### Thứ 2: 
- Sáng xử lý đường dây, gán thêm nhãn với chú Tuấn
- Sáng + chiều: Tham khảo về metadata kết hợp với chunking 
### Thứ 3: 
- Nghỉ
- Tham khảo thêm về mô hình RAG và Preprocess tài liệu
### Thứ 4: 
- Nghiên cứu về các phương pháp Chunking: Semantics, Hierarchical  để Embed vào VecDB
- Sửa Txt-Preprocessing và lấy log txt-preprocessing
- Viết văn bản và làm audio cho chú Thuận
### Thứ 5
- Sửa phần img-Preprocessing, table-Preprocessing
- Xuất chunking và save local VectorDB
### Thứ 6:
- Thuyết trình Chatbot và tiến trình của 4 tuần
- Tổng kết lại thành quả 4 tuần và làm doc
- Làm lại audio cho chú Thuận

### Thứ 7: 
- Tiếp tục tham khảo thêm về mô hình RAG và Preprocess tài liệu -> Rasa-chatbot framework + Deepseek-DocPreprocessing

## Các tác vụ đã hoàn thành 
- Xuất file meta log Txt-, img-, table- Prep Doc (có Document Name, data_type = {txt, img, table}, extracted_data)
- Xuất file Chunking của Txt-, img-, table- 
- Xuất file local VectorDB	

![A diagram illustrating the differences between selected types of chunking in natural language processing](https://bitpeak.com/wp-content/uploads/2024/04/Chunking-methodv5.png)

# Những góp ý sau bài thuyết trình 
1. Lưu ý việc tạo các testcase, các kịch bản để vừa kiểm tra tiến độ, vừa kiểm tra hiệu năng của Chatbot
2. Về vấn đề Chunking, cần xem xét việc chia tài liệu để đảm bảo tính toạn vẹn của nghĩa trong câu 
3. Ưu tiên vào Tiền xử lý dữ liệu txt hơn là table và image
4. Cần tìm cách để kiểm tra Doc-prep và chunking (file log) -> BM25 + 
5. Làm Query, Retrieve -enrichment để đảm bảo truy vấn của người dùng (paraphase)
6. Tìm hiểu các công cụ tương tự Khoj
7. Citation - trích dẫn sai
   
# Thuyết trình tổng kết 4 tuần:

https://app.slidespeak.co/presentation/cm923w7nb000c2io68cchj78p/share
