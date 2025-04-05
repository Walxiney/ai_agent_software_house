from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class CrewDeveloper():
    """Developer Crew"""

    agents_config = "config/agent_dev.yaml"
    tasks_config = "config/task_dev.yaml"

    @agent
    def python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["python_developer"],
        )

    @task
    def develop_python_code(self) -> Task:
        return Task(
            config=self.tasks_config["develop_python_code"],
        )

    @crew
    def crew(self) -> Crew:
        """Create Dev Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
