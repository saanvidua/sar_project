import os
import json
import re
import pandas as pd
import openai
from openai.types import Completion, CompletionChoice, CompletionUsage
from sar_project.agents.base_agent import SARBaseAgent
import difflib

class FirstAidAgent(SARBaseAgent):
    def __init__(self, first_aid_path, triage_path):
        """
        Initialize the FirstAidAgent with the paths to the first aid JSON and triage CSV.
        OpenAI API key is set in the environment (OPENAI_API_KEY).
        """
        super().__init__(
            name="FirstAidAgent",
            role="First Aid Guidance Agent",
            system_message="You are a search and rescue medical assistant specialized in providing first aid guidance and medical triage advice."
        )

        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )
        self.first_aid_path = first_aid_path
        self.triage_path = triage_path
        self.first_aid_knowledge = self.load_first_aid_knowledge()
        self.df_triage = self.load_triage_data()

    def load_first_aid_knowledge(self):
        """Load the first aid knowledge base from a JSON file."""
        try:
            with open(self.first_aid_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data.get("intents", [])
        except Exception as e:
            print(f"Error loading first aid knowledge: {e}")
            return []


    def load_triage_data(self):
        """Load the triage data from a CSV file into a DataFrame."""
        try:
            return pd.read_csv(self.triage_path)
        except Exception as e:
            print(f"Error loading triage data: {e}")
            return pd.DataFrame()

    def provide_first_aid_guidance(self, query):
        """Find the best matching first aid advice for a given query."""
        query = query.lower()
        best_match = None
        highest_ratio = 0

        for intent in self.first_aid_knowledge:
            for pattern in intent["patterns"]:
                pattern = pattern.lower()
                ratio = difflib.SequenceMatcher(None, query, pattern).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = intent

        if best_match and highest_ratio > 0.6:  # Adjust threshold as needed
            return best_match["responses"][0]  # Return the first response
        else:
            return "I'm sorry, I couldn't find relevant first aid guidance. Please consult a medical professional"

    def assign_triage_via_llm(self, patient_info):
        """Assign a triage category using OpenAI's Chat API."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Adjust model as needed
                messages=[
                    {"role": "system", "content": (
                    "You are a medical triage assistant. Based on the provided patient information, "
                    "assign an appropriate triage color and explain its meaning.\n"
                    "Triage Definitions:\n"
                    "Red: Needs immediate attention for a critical life-threatening injury or illness; transport first for medical help.\n"
                    "Yellow: Serious injuries needing immediate attention. In some systems, yellow tags are transported first because they have a better chance of recovery than red-tagged patients.\n"
                    "Green: Less serious or minor injuries, non-life-threatening, delayed transport; will eventually need help but can wait for others.\n"
                    "Black: Deceased or mortally wounded; may not mean the person has already died, but that they are beyond help.\n"
                    "White: No injury or illness.\n\n"
                    "Please return only the assigned triage category followed by its meaning."
                    )},
                    {"role": "user", "content": f"Patient info: {patient_info}"}
                ]
            )
            
            # Extracting the actual response text
            assigned_triage = response.choices[0].message.content.strip()
            return assigned_triage

        except Exception as e:
            print(f"Error assigning triage via LLM: {e}")
            return None  # Return None if an error occurs

    def generate_triage_summary(self):
        """
        Generate a summary of the triage levels from the CSV data.
        """
        if "triage" not in self.df_triage.columns:
            return {}
        summary = self.df_triage["triage"].value_counts().to_dict()
        return summary

    def answer_combined_question(self, first_aid_guidance, triage_info):
        """Generate a final response combining first aid guidance and triage info."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical assistant. Combine first aid guidance with triage information."},
                    {"role": "user", "content": f"First Aid Guidance: {first_aid_guidance}\nTriage Info: {triage_info}"}
                ]
            )

            # Extract the response correctly
            combined_answer = response.choices[0].message.content.strip()
            return combined_answer

        except Exception as e:
            print(f"Error generating combined answer: {e}")
            return "Unable to generate a combined response."

# Example usage (for development/testing):
if __name__ == "__main__":
    # Update paths as needed.
    first_aid_file = "src/sar_project/knowledge/first_aid_intents.json"
    triage_file = "src/sar_project/knowledge/patient_priority.csv"
    
    agent = FirstAidAgent(first_aid_file, triage_file)
    
    # Task 1: Provide first aid guidance.
    query1 = "How do you treat a bee sting?"
    print("First Aid Guidance:")
    print(agent.provide_first_aid_guidance(query1))
    
    # Task 2: Assign triage using the LLM approach.
    # Patient info may be incomplete.
    patient_info = {
        "age": 52.0,
        "gender": 1.0,
        "blood pressure": 130.0,
        "cholesterol": 294.0,
        "max heart rate": 150.0,
        "bmi": 23.0
        # Other fields might be missing.
    }
    print("\nAssigned Triage via LLM for Patient Info:")
    triage_info = agent.assign_triage_via_llm(patient_info)
    print(triage_info)
    # Task 3: Generate a triage summary.
    print("\nTriage Summary:")
    print(agent.generate_triage_summary())
    
    # Task 4: Answer a combined question using OpenAI context.
    combined_query = "What is the recommended first aid for a 57 year old with high heart rate who has been stung by a bee?"
    print("\nCombined Answer:")
    print(agent.answer_combined_question(combined_query, triage_info))

