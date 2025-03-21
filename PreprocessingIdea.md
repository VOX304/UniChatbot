# Preprocessing

## Document Preprocessing
```mermaid
graph TD;
A[Start: Upload Document] --> B{Detect File Type};

B -->|DOCX/DOC| C[Read file using python-docx];
B -->|PDF| D[Read file using pdfplumber];

D --> E[Analyze Content Type];
C --> E;

E -->|Text Found| F[Store Extracted Text];
E -->|Table Detected| G{Is Table Recognizable as Text?};
E -->|Image Found| H[Extract Images];

G -->|Yes| I[Extract Table Directly];
G -->|No| J[Convert Table to Image & Apply OCR];

H --> K[Apply OCR on Images if Necessary];

I --> L[Organize the order];
J --> L;
K --> L;
F --> L;

L --> M[Chunking Preprocessing];

```

## Chunking Preprocessing
```mermaid
graph TD;
A(Start) --> C(Document Preprocessing);

subgraph Chunking Preprocessing
  C --> D{Recursive Chunking?};

  subgraph Recursive Chunking
    D -->|Yes| E[Split by Sections - Paragraphs - Sentences];
    E --> H{Check Chunk Size};
    H -->|Too Large| D;
    H -->|Optimal| I[Store Initial Chunks + Attach Metadata];
  end

  subgraph Semantic Chunking
    I --> J[Generate Embeddings: Sentence-BERT];
    J --> K[Compute Cosine Similarity];
    K --> L[Agglomerative Clustering];
    L --> M{Merge Similar Chunks?};
    M -->|Yes| N[Merge Chunks];
  end

  M -->|No| O[Store Final Chunks in VectorDB];
  N --> O;
end

O --> Q[End Preprocessing Step];
Q --> R(End);

```
