import requests

API_URL = "http://localhost:8000/answer"
CONNECT_URL = "http://localhost:8000/connect"


def chat_with_server():
    # Connect and get the welcome message
    try:
        connect_response = requests.get(CONNECT_URL)
        connect_response.raise_for_status()
        data = connect_response.json()
        print("Response:", data["response"])
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return
    
    print("Type 'exit' to stop the chat.")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Ending chat. Goodbye!")
            break
        payload = {
            "query": query,
            "history": []  # You can adjust this to maintain history
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            print("Response:", data["response"])
            #print("Sources:", data["sources"])
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")


if __name__ == "__main__":
    chat_with_server()
