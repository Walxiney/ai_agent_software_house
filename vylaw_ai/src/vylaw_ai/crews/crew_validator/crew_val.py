from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

class CodeVerification(BaseModel):
    valid: bool
    feedback: Optional[str]

@CrewBase
class CodeReviewCrew:
    """Code Review Crew"""

    agents_config = "config/agent_val.yaml"
    tasks_config = "config/task_val.yaml"

    @agent
    def python_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["python_validator"],
        )

    @task
    def validator_python_code(self) -> Task:
        return Task(
            config=self.tasks_config["validator_python_code"],
            output_pydantic=CodeVerification
        )

    @crew
    def crew(self) -> Crew:
        """Create the Code Review Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
