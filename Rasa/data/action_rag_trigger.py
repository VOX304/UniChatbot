import subprocess
import os
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionRagTrigger(Action):
    def name(self):
        return "action_rag_trigger"

    async def run(self, dispatcher, tracker, domain):
        # Get the user input
        user_input = tracker.latest_message.get("text")

        try:
            # Get the absolute path to draft.py
            script_path = os.path.join(os.path.dirname(__file__), 'draft.py')

            # Open a new terminal window to start draft.py as a Streamlit app and pass the user input
            subprocess.Popen(['start', 'cmd', '/k', f'python {script_path} "{user_input}" & pause'], shell=True)
            
            dispatcher.utter_message(text="RAG interface has been triggered in a new terminal.")

        except Exception as e:
            dispatcher.utter_message(text=f"Error triggering RAG interface: {e}")

        return []
