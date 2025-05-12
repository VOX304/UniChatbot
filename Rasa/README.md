# CollegeChatbot

<div>
    <a href="https://doi.org/10.3126/kjse.v8i1.69263">Cite this work:  </a>
</div>
<br>


## Introduction
Welcome to the College Chatbot! This chatbot has been developed using open source machine learning framework [Rasa](https://rasa.com/). The chatbot allows users to ask a college information. It can  be extended to handle queries related to `college details`, details about `specific programs`, `scholarship schemes`, `college facilities` via database integration.

## About Rasa
Rasa is a open-source machine learning framework that enables the development of conversational AI chatbots. The Rasa stack consists of two components:

1. Rasa NLU
2. Rasa Core

Rasa NLU handles the natural language understanding aspect of the chatbot, and Rasa Core handles the dialogue management aspect.

## Getting Started

Before getting started with the chatbot, make sure you have the following requirements installed:

- Python 3
- pip (package manager for Python)

To install Rasa, you can use the following pip command: <br />
```pip install -r requirements.txt```

Once rasa has been installed, clone this repository and navigate to the directory containing the chatbot files.
```git clone https://github.com/yubraaj11/CollegeChatbot.git```

## Training the Chatbot
To train the chatbot, you can use the following command:<br />
```rasa train```

## Running the Chatbot
**Step 1: To run the chatbot, you can use the following command:**<br />
```rasa run --enable-api```

**Step 2: For basic validations you need to be connected to action server**<br />
To run the action server, you can use the following command:<br />
```rasa run actions```

**Step 3: Accessing the chatbot via RASA CLI**<br />
Now we have the Rasa server up and running, and the chatbot will be available to chat with through the Rasa command line interface.
To talk with the bot, you can use the following command:<br />
```rasa shell```


## Instead of running chatbot via CLI, you can run it via *Streamlit* <br />
To run via streamlit: <br />
```streamlit run UI/app.py```


## Customizing the Chatbot<br />
The chatbot's behavior and responses are defined in the data/nlu.yml and domain.yml files. You can modify these files to add your own custom intents and responses. Additionally, the chatbot's conversational flow is defined in the stories.yml file, and you can modify this file to add custom actions and change the flow of the conversation.

---

# ScreenShot of the UI in Streamlit
![image](https://github.com/yubraaj11/CollegeChatbot/assets/84309182/2c688258-dc0c-4cf2-aba3-bb70b54e0280)
![image](https://github.com/yubraaj11/CollegeChatbot/assets/84309182/dc329dc4-e3bc-499c-b5d0-0ef4f342ea2f)
![image](https://github.com/yubraaj11/CollegeChatbot/assets/84309182/8eeb465f-de32-401d-889e-a5ab8ca25d60)
![image](https://github.com/yubraaj11/CollegeChatbot/assets/84309182/49952a59-8a58-4fd2-af38-64c1dda82536)






