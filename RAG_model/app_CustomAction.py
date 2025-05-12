from fastapi import FastAPI
from pydantic import BaseModel
from Retrieval import answer_query

class QueryIn(BaseModel):
    query: str
    history: list

class QueryOut(BaseModel):
    response: str
    sources: dict

app = FastAPI()

@app.get("/connect")
def connect():
    return {"response": "🎓 Xin chào! Tôi là mô hình Truy xuất Tăng Cường Uni-chatbot của Trường Sĩ Quan Thông Tin. Bạn cần tra cứu điều gì?\nType \"exit\" to exit", "sources": {}}

@app.post("/answer", response_model=QueryOut)
def answer(payload: QueryIn):
    return answer_query(payload.query, payload.history)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
