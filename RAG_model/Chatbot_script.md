```mermaid
graph TD;
  A[User sends a message] -->|Check if exit command| B{Exit?};
  B -- Yes --> C[Ask for user feedback];
  C --> D[Send thank you message] --> E[End conversation];
  B -- No --> F[Store user message in history];

  F --> G[Retrieve relevant documents];
  G --> H[Augment prompt with history + documents];
  
  H --> I[Select Gemini model - Round Robin];
  I --> J[Construct full prompt with history & sources];
  
  J --> K[Send empty message for streaming];
  K --> L{Stream Gemini response?};
  
  L -- Yes --> M[Send response token-by-token] --> L;
  L -- No --> N[Save response in history];

  N --> O[Retrieve & format sources];
  O --> P[Send source information to user];
  
  P --> Q[Update sidebar with conversation history];
  Q --> A;

