from crewai import Flow
from crewai.flow.flow import listen, start, and_
import yaml

from typing import Optional
from pydantic import BaseModel

from crews.programming_crew.crew import (
	CrewDeveloper
)

from dotenv import load_dotenv
load_dotenv()

class CodeResult(BaseModel):
	code: str = ""
	feedback: Optional[str] = None
	valid: bool = False

class ProgrammingFlow(Flow[CodeResult]):

	@start()
	def read_user_input(self, file_name:str = "input.yaml")-> list:
		try:
			file_path = f'vylaw_ai_2/src/vylaw_ai_2/crews/programming_crew/config/{file_name}'
			with open(file_path, 'r', encoding='utf-8') as file:
				project_yml = yaml.safe_load(file)
			project = project_yml["project"][0]
		except FileNotFoundError as e:
			print(f"Error: {e}. Please check the file path for the input.yaml.")
		return project

	@listen(read_user_input)
	def generate_code(self, project:dict):
		print("Generating code...")
		if not project:
			print("No project found in the YAML file.")
			return None
		
		try:
			result = (CrewDeveloper().crew().kickoff(
				inputs={
					"project_name": project["project_name"],
					"project_description": project["project_description"],
					"feedback": self.state.feedback,
					"code": self.state.code
					}
				)
			)
		except FileNotFoundError as e:
			print(f"Error: {e}. Error on CrewDeveloper.")

		raw_code = result.raw
		self.state.code = f"""{raw_code}"""
		self.state.valid = result["valid"]
		self.state.feedback = result["feedback"]

		if self.state.valid:
			print(" OOOOOOOOOOOOK !!!!!\n")
			print(raw_code)
		return raw_code

def run_flow():
	programming_flow = ProgrammingFlow()
	programming_flow.plot()
	programming_flow.kickoff()


if __name__ == "__main__":
	run_flow()