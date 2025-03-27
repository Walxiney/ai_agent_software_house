from crewai import Agent, Crew, Process, Task
import yaml
import json

class AgentsTasksCrew():

    def __init__(self):
        pass

    def project_description(self):
        file_path = 'config/input.yaml'
        with open(file_path, 'r', encoding='utf-8') as file:
            project_yml = yaml.safe_load(file)
            project_info = project_yml["project"]
        return project_info
    
    def available_agents(self):
        agents_file_path = 'config/agents_few.yaml'
        with open(agents_file_path, 'r', encoding='utf-8') as file:
            agents_data = yaml.safe_load(file)

        # must have the agent parameter in the tasks.yaml file
        tasks_file_path = 'config/tasks_few.yaml'
        with open(tasks_file_path, 'r', encoding='utf-8') as tasks_file:
            tasks_data = yaml.safe_load(tasks_file)

        agents_tasks = {}
        for task_name, task_details in tasks_data.items():
            agent_name = task_details.get('agent')
            if agent_name in agents_data:
                agents_tasks[agent_name] = task_name
        
        agents_tasks_output = {"agents_tasks": agents_tasks}
        return agents_tasks_output
    
    def project_info_and_agents_tasks(self):
        project_info = self.project_description()
        agents_tasks_output = self.available_agents()
        project_info[0].update(agents_tasks_output)
        return project_info

    def read_agents_tasks(self):
        # Define file paths for YAML configurations
        files = {
            'agents': 'config/agents_few.yaml',
            'tasks': 'config/tasks_few.yaml',
        }
        # Load configurations from YAML files
        configs = {}
        for config_type, file_path in files.items():
            with open(file_path, 'r', encoding='utf-8') as file:
                configs[config_type] = yaml.safe_load(file)
        return configs
    
    def crew_orchestrator(self):
        # Load configurations from YAML files
        configs = self.read_agents_tasks()

        # AGENTS
        team_selector_agent = Agent(
            config=configs['agents']['team_selector_agent'],
            llm="gpt-4o-mini",
            verbose=True
        )

        # TASKS
        team_selection_task = Task(
            config=configs['tasks']['team_selection_task'],
            agent=team_selector_agent,
            #output_pydantic=AgentTask
        )

        return Crew(
            agents=[team_selector_agent],
            tasks=[team_selection_task],
            verbose=True
        )
    

atc = AgentsTasksCrew()

print("#"*30, "PROJECT DESCRIPTION", "#"*30)
project_info = atc.project_description()
print(type(project_info))
print(type(project_info[0]))
print(project_info[0].keys())
print("#"*80)

print("#"*30, "AVAIABLE AGENTS", "#"*30)
available_agents = atc.available_agents()
print(type(available_agents))
print(available_agents.keys())
print(available_agents[list(available_agents.keys())[0]])
print(len(available_agents[list(available_agents.keys())[0]].keys()))
print("#"*80)

print("#"*30, "PROJECT INFO AGENT TASKS", "#"*30)
project_info_and_agents_tasks = atc.project_info_and_agents_tasks()
print(type(project_info_and_agents_tasks))
print(len(project_info_and_agents_tasks))
print(project_info_and_agents_tasks[0].keys())
print(list(project_info_and_agents_tasks[0].keys()))
print(type(project_info_and_agents_tasks[0][list(project_info_and_agents_tasks[0].keys())[2]]))
print(len(project_info_and_agents_tasks[0][list(project_info_and_agents_tasks[0].keys())[2]].keys()))
print(project_info_and_agents_tasks[0][list(project_info_and_agents_tasks[0].keys())[2]].keys())
print("#"*80)

print("#"*30, "READ AGENTS TASKS", "#"*30)
read_agents_tasks = atc.read_agents_tasks()
print(len(read_agents_tasks["agents"]))
print(read_agents_tasks["agents"].keys())
print(len(read_agents_tasks["tasks"]))
print(read_agents_tasks["tasks"].keys())
print("#"*80)

input = atc.project_info_and_agents_tasks()
staff = atc.crew_orchestrator().kickoff(input[0])
# staff_json = json.loads(staff.encode('utf-8').decode('utf-8'))
staff_json = dict(staff)
staff_json = json.loads(staff_json['raw'].encode('utf-8').decode('utf-8'))
print(staff)
print(staff_json)

