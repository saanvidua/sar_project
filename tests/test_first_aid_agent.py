import pytest
import os
from sar_project.agents.first_aid_agent import FirstAidAgent

class TestFirstAidAgent:
    @pytest.fixture
    def agent(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the test file
        first_aid_path = os.path.join(base_dir, "../src/sar_project/knowledge/first_aid_intents.json")
        triage_path = os.path.join(base_dir, "/src/sar_project/knowledge/patient_priority.csv")

        print(f"\nDEBUG: First Aid JSON Path -> {first_aid_path}")
        print(f"DEBUG: Triage CSV Path -> {triage_path}")

        return FirstAidAgent(first_aid_path, triage_path)  # Fixed class name

    def test_first_aid_guidance(self, agent):
        # Basic check that the response is non-empty and mentions the condition
        guidance = agent.provide_first_aid_guidance("How do you treat a sprain?")
        assert "sprain" in guidance.lower() or "treat" in guidance.lower()

    def test_assign_triage_via_llm(self, agent):
        patient_info = {
            "age": 52.0,
            "gender": 1.0,
            "blood pressure": 130.0,
            "cholesterol": 294.0,
            "max heart rate": 150.0,
            "bmi": 32.0
        }
        triage_response = agent.assign_triage_via_llm(patient_info)
        expected_colors = ["red", "yellow", "green", "black", "white"]
        
        assert isinstance(triage_response, str) and len(triage_response) > 0
        # Check that one of the expected colors is mentioned in the response along with an explanation.
        assert any(color in triage_response.lower() for color in expected_colors)
        assert ":" in triage_response  # Ensure explanation is included, expecting a colon between the color and its explanation.

    def test_generate_summary(self, agent):
        summary = agent.generate_triage_summary()
        expected_keys = {"red", "yellow", "green", "black", "white", "orange"}
        assert all(key.lower() in expected_keys for key in summary.keys())

    def test_answer_combined_question(self, agent):
        # Check that summary keys are within the set of expected triage categories
        combined_query = "What is the recommended first aid for deep cuts for middle-aged women with low blood pressure?"
        triage_info = "Yellow: Serious injuries needing immediate attention."
        answer = agent.answer_combined_question(combined_query, triage_info)
        
        assert isinstance(answer, str) and len(answer) > 0

    def test_load_first_aid_knowledge_file_not_found(self, monkeypatch):
        # Test handling when the first aid JSON file is missing.
        fake_first_aid_path = "non_existent_file.json"
        fake_csv_path = "non_existent_file.csv"
        agent = FirstAidAgent(fake_first_aid_path, fake_csv_path)
        knowledge = agent.load_first_aid_knowledge()
        assert knowledge == []

    def test_load_triage_data_file_not_found(self, monkeypatch):
        # Test handling when the triage CSV file is missing.
        fake_first_aid_path = "non_existent_file.json"
        fake_csv_path = "non_existent_file.csv"
        agent = FirstAidAgent(fake_first_aid_path, fake_csv_path)
        df = agent.load_triage_data()
        assert df.empty

