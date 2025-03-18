# SchoolChatbot
Chatbot feeded by school's information

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
