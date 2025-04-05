
from typing import Optional
import yaml
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from crews.crew_developer.crew_dev import (
    CrewDeveloper
)
from crews.crew_validator.crew_val import (
    CodeReviewCrew
)

from dotenv import load_dotenv
load_dotenv()

class CodeResult(BaseModel):
    code: str = ""
    feedback: Optional[str] = None
    valid: bool = False
    retry_count: int = 0

class ProgrammingFlow(Flow[CodeResult]):

    def read_user_input(self, file_name:str = "input.yaml") -> dict:
        """Read user input from a YAML file"""
        try:
            file_path = f"vylaw_ai/src/vylaw_ai/user_input/{file_name}"
            with open(file_path, "r", encoding='utf-8') as file:
                project_yaml = yaml.safe_load(file)
            project = project_yaml["project"][0]
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        return project

    @start("retry")
    def generate_code(self):
        print("Generating code...")
        
        project = self.read_user_input()
        if not project:
            print("No project found in the YAML file.")
            return
        
        if self.state.retry_count > 0:
            result = (
                CrewDeveloper().crew().kickoff(
                    inputs={
                        "project_name": project["project_name"],
                        "retry": self.state.retry_count,
                        "project_description": project["project_description"],
                        "feedback": self.state.feedback,
                        "code": self.state.code
                    }
                )
            )
            raw_code = result.raw
            self.state.code = f"""{raw_code}"""
        else:
            result = (
                CrewDeveloper().crew().kickoff(
                    inputs={
                        "project_name": project["project_name"],
                        "retry": self.state.retry_count,
                        "project_description": project["project_description"],
                        "feedback": self.state.feedback,
                        "code": None
                    }
                )
            )
            raw_code = result.raw
            self.state.code = f"""{raw_code}"""

    @router(generate_code)
    def validate_code(self):
        project = self.read_user_input()

        if self.state.retry_count > 3:
            return "max_retry_exceeded"
        
        result = CodeReviewCrew().crew().kickoff(
            inputs={
                "code": self.state.code,
                "project_description": project["project_description"]
            }
        )
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]

        print(f"Validation result: {self.state.valid}")
        print(f"Feedback: {self.state.feedback}")
        self.state.retry_count += 1

        if self.state.valid:
            return "complete"
        
        return "retry"

    @listen("complete")
    def save_result(self):
        print("Code is valid")
        print("Code:", self.state.code)

        with open("python_code.py", "w") as file:
            file.write(self.state.code)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded!")
        print("Code:", self.state.code)	
        print("Feedback:", self.state.feedback)

def kickoff():
    programming_flow = ProgrammingFlow()
    programming_flow.plot()
    programming_flow.kickoff()

if __name__ == "__main__":
    kickoff()
