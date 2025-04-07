from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from typing import Optional
from pydantic import BaseModel

class CodeVerification(BaseModel):
    valid: bool
    feedback: Optional[str]

@CrewBase
class CrewDeveloper():
    """Developer Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # @agent
    # def manager(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["manager"],
    #     )

    @agent
    def python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["python_developer"],
        )
    
    @agent
    def python_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["python_validator"],
        )
    
    # @task
    # def management(self) -> Agent:
    #     return Task(
    #         config=self.tasks_config["management"],
    #     )

    @task
    def develop_python_code(self) -> Task:
        return Task(
            config=self.tasks_config["develop_python_code"],
        )
    
    @task
    def validator_python_code(self) -> Task:
        return Task(
            config=self.tasks_config["validator_python_code"],
            output_pydantic=CodeVerification
        )

    @crew
    def crew(self) -> Crew:
        """Create Dev Crew"""
        # Define a custom manager agent
        manager = Agent(
            role="Project Manager",
            goal="Efficiently manage the crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success.",
            allow_delegation=True,
            verbose= True
        )

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            manager_agent=manager,
            process=Process.hierarchical,
            verbose=True,
        )
