# data_analysis_app/agents/interface_agent.py

from models.groq_model import GroqModel

class InterfaceAgent:
    def __init__(self):
        self.model = GroqModel()

    def process_input(self, user_input):
        prompt = f"""
        Analyze the following user input and extract the intent for data analysis:
        User input: {user_input}
        
        Provide the intent in the following format:
        Intent: [brief description of the intent]
        Analysis type: [e.g., descriptive, comparative, predictive]
        Visualization: [type of visualization if applicable, e.g., bar chart, scatter plot, etc.]
        """

        response = self.model.generate(prompt)
        
        # Parse the response to extract intent details
        intent_lines = response.strip().split('\n')
        intent = {line.split(': ')[0].lower(): line.split(': ')[1] for line in intent_lines}

        return intent

    def clarify_intent(self, user_input):
        prompt = f"""
        The user's request "{user_input}" is unclear. Generate a clarifying question to better understand their data analysis needs.
        """

        clarification = self.model.generate(prompt)
        return clarification.strip()
