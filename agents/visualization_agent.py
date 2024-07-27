# data_analysis_app/agents/visualization_agent.py

import subprocess
import os
import sys

class VisualizationAgent:
    def execute_code(self, script_path):
        try:
            # Execute the generated Python script
            result = subprocess.run([sys.executable, script_path], 
                                    capture_output=True, text=True, check=True)
            
            # Check if the output plot was generated
            if os.path.exists('output_plot.png'):
                return True, result.stdout
            elif os.path.exists('output.csv'):
                return True, result.stdout
            else:
                return False, f"Visualization not generated. Script output:\n{result.stdout}\nError output:\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return False, f"Error executing code:\nStandard output: {e.stdout}\nError output: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"