from crewai import Agent, Crew, Process, Task
import yaml
import os

class AgentsTasksCrew():
    """Agents and Tasks crew
    This class is responsible for creating a crew of agents and tasks based on the provided YAML configurations.
    It includes methods to read agent and task configurations from YAML files, create a crew orchestrator,
    and dynamically create agents and tasks based on the provided team configuration.
    """

    def __init__(self):
        pass

    def read_agents_tasks(self)-> dict:
        """
        Read agents and tasks from YAML files.
        This method loads the configurations for agents and tasks from the specified YAML files.
        - input: None
        - output: Dictionary containing agents and tasks configurations
        """
        # Define file paths for YAML configurations
        files = {
            'agents': 'software_house/src/software_house/config/agents_few.yaml',
            'tasks': 'software_house/src/software_house/config/tasks_few.yaml',
        }

        # Load configurations from YAML files
        configs = {}
        
        for config_type, file_path in files.items():
            with open(file_path, 'r', encoding='utf-8') as file:
                configs[config_type] = yaml.safe_load(file)

        return configs

    def crew_orchestrator(self)-> Crew:
        """
        Create the crew orchestrator.
        This orchestrator is responsible for managing the agents and tasks.
        - input: None
        - output: Crew object
        """

        try:
            # Load the available agents from the agents.yaml file
            agents_file_path = 'software_house/src/software_house/config/agent_orchestrator.yaml'
            with open(agents_file_path, 'r', encoding='utf-8') as file:
                agent_orchestrator = yaml.safe_load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}. Please check the file path for the agent_orchestrator.yaml.")

        try:
            # Load the available tasks from the tasks.yaml file
            tasks_file_path = 'software_house/src/software_house/config/task_orchestrator.yaml'
            with open(tasks_file_path, 'r', encoding='utf-8') as tasks_file:
                task_orchestrator = yaml.safe_load(tasks_file)
        except FileNotFoundError as e:
            print(f"Error: {e}. Please check the file path for the task_orchestrator.yaml.")

        orchestrator_output = "software_house/src/software_house/orchestrator_output/agent_orchestrator.txt"
        with open(orchestrator_output, "w", encoding="utf-8") as file:
            file.write("")
        # AGENTS
        team_selector_agent = Agent(
            config=agent_orchestrator['team_selector_agent'],
            llm="gpt-4o-mini",
            verbose=True
        )

        # TASKS
        team_selection_task = Task(
            config=task_orchestrator['team_selection_task'],
            agent=team_selector_agent,
            output_file=orchestrator_output
            # output_pydantic=AgentTask
        )

        return Crew(
            agents=[team_selector_agent],
            tasks=[team_selection_task],
            verbose=True
        )

    def creating_crew_dev(self, team, folder_name)-> Crew:
        """
        Create the crew for the project.
        This method dynamically creates agents and tasks based on the provided team configuration.
        - input: team (dict) - Dictionary containing the team configuration
        - output: Crew object
        """

        # Load configurations from YAML files
        configs = self.read_agents_tasks()

        # Assign loaded configurations to specific variables
        agents_config = configs['agents']
        tasks_config = configs['tasks']

        model_to_use = "gpt-4o-mini"

        try:
            # Dynamically create agents based on the team
            agents = {}
            for agent_key in team["agents_tasks"].keys():
                if agent_key in agents_config:
                    agents[agent_key] = Agent(
                        config=agents_config[agent_key],
                        llm=model_to_use,
                        verbose=True
                    )
        except Exception as e:
            print(f"Error while creating agents: {e}")

        try:
            # Dynamically create tasks based on the agents
            tasks = []
            output_dir = f"software_house/src/software_house/{folder_name}"
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            for agent_key, task_key in team["agents_tasks"].items():
                if agent_key in agents and task_key in tasks_config:

                    # Define the output file path
                    output_file_path = os.path.join(output_dir, f"{task_key}.txt")
                    # Create or overwrite the file (ensure it's ready for writing)
                    with open(output_file_path, "w", encoding="utf-8") as file:
                        file.write("")  # Write an empty string to initialize or clear the file
                    
                    task = Task(
                        config=tasks_config[task_key],
                        agent=agents[agent_key],
                        output_file=output_file_path,
                        context=None,  # Initialize context as None
                    )
                    tasks.append(task)

                    t = len(tasks)
                    # Set the context for the code aggregation task
                    if task_key == "code_aggregation_task" and t >= 2:
                        t = len(tasks)
                        tasks[-1].context = [tasks[t-3], tasks[t-2]]
                    
        except Exception as e:
            print(f"Error while creating tasks: {e}")

        # Return the dynamically created crew
        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process= Process.sequential, #Process.hierarchical,
            verbose=True
        )