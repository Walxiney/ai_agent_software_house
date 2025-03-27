from crewai import Agent, Crew, Process, Task
import yaml

from pydantic import BaseModel, Field
from typing import Dict

# from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

class AgentTask(BaseModel):
    agents_tasks: Dict = Field(..., description="Agent's name and respective task's name.")

class AgentsTasksCrew():
    """Agents and Tasks crew"""

    def __init__(self):
        pass

    def read_agents_tasks(self):
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

    def crew_orchestrator(self):
        """
        Create the crew orchestrator.
        """
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
            agent=team_selector_agent
            # output_pydantic=AgentTask
        )

        return Crew(
            agents=[team_selector_agent],
            tasks=[team_selection_task],
            verbose=True
        )

    def creating_crew_dev(self, team):

        # Load configurations from YAML files
        configs = self.read_agents_tasks()

        # Assign loaded configurations to specific variables
        agents_config = configs['agents']
        tasks_config = configs['tasks']

        model_to_use = "gpt-4o-mini"

        # Dynamically create agents based on the team
        agents = {}
        for agent_key in team["agents_tasks"].keys():
            if agent_key in agents_config:
                agents[agent_key] = Agent(
                    config=agents_config[agent_key],
                    llm=model_to_use,
                    verbose=True
                )

        # Dynamically create tasks based on the agents
        tasks = []
        for agent_key, task_key in team["agents_tasks"].items():
            if agent_key in agents and task_key in tasks_config:
                task = Task(
                    config=tasks_config[task_key],
                    agent=agents[agent_key]
                )
                tasks.append(task)

        # Return the dynamically created crew
        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process= Process.sequential, #Process.hierarchical,
            verbose=True
        )

        # # AGENTS
        # product_owner = Agent(
        #     config=agents_config['product_owner'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # scrum_master = Agent(
        #     config=agents_config['scrum_master'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # software_architect = Agent(
        #     config=agents_config['software_architect'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # frontend_developer = Agent(
        #     config=agents_config['frontend_developer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # backend_developer = Agent(
        #     config=agents_config['backend_developer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # database_engineer = Agent(
        #     config=agents_config['database_engineer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # devops_engineer = Agent(
        #     config=agents_config['devops_engineer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # qa_engineer = Agent(
        #     config=agents_config['qa_engineer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # security_engineer = Agent(
        #     config=agents_config['security_engineer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # technical_writer = Agent(
        #     config=agents_config['technical_writer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # ux_ui_designer = Agent(
        #     config=agents_config['ux_ui_designer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # business_analyst = Agent(
        #     config=agents_config['business_analyst'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # ai_ml_engineer = Agent(
        #     config=agents_config['ai_ml_engineer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # #-----------------simple agent------------------#
        # senior_fullstack_engineer_agent = Agent(
        #     config=agents_config['senior_fullstack_engineer_agent'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # qa_engineer_agent = Agent(
        #     config=agents_config['qa_engineer_agent'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # chief_qa_engineer_agent = Agent(
        #     config=agents_config['chief_qa_engineer_agent'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # technical_writer = Agent(
        #     config=agents_config['technical_writer'],
        #     llm=model_to_use,
        #     verbose=True
        # )

        # code_aggregator_agent = Agent(
        #     config=agents_config['code_aggregator_agent'],
        #     llm=model_to_use,
        #     verbose=True
        # )   
        # #-----------------------------------------------#

        # # TASKS
        # define_requirements = Task(
        #     config=tasks_config['define_requirements'],
        #     agent=product_owner
        # )

        # manage_sprints = Task(
        #     config=tasks_config['manage_sprints'],
        #     agent=scrum_master
        # )

        # design_architecture = Task(
        #     config=tasks_config['design_architecture'],
        #     agent=software_architect,
        #     context=[define_requirements]
        # )

        # develop_frontend = Task(
        #     config=tasks_config['develop_frontend'],
        #     agent=frontend_developer,
        #     context=[define_requirements, design_architecture]
        # )

        # develop_backend = Task(
        #     config=tasks_config['develop_backend'],
        #     agent=backend_developer,
        #     context=[define_requirements, design_architecture, develop_frontend]
        # )

        # manage_database = Task(
        #     config=tasks_config['manage_database'],
        #     agent=database_engineer,
        #     context=[define_requirements, design_architecture]
        # )

        # implement_devops = Task(
        #     config=tasks_config['implement_devops'],
        #     agent=devops_engineer
        # )

        # execute_tests = Task(
        #     config=tasks_config['execute_tests'],
        #     agent=qa_engineer,
        #     context=[develop_frontend, develop_backend, manage_database]
        # )

        # ensure_security = Task(
        #     config=tasks_config['ensure_security'],
        #     agent=security_engineer,
        #     context=[develop_frontend, develop_backend, manage_database]
        # )

        # write_documentation = Task(
        #     config=tasks_config['write_documentation'],
        #     agent=technical_writer,
        #     context=[define_requirements, design_architecture, develop_frontend, develop_backend, manage_database, implement_devops, execute_tests, ensure_security]
        # )

        # design_ui_ux = Task(
        #     config=tasks_config['design_ui_ux'],
        #     agent=ux_ui_designer,
        #     context=[define_requirements, design_architecture]
        # )

        # analyze_business = Task(
        #     config=tasks_config['analyze_business'],
        #     agent=business_analyst,
        #     context=[define_requirements]
        # )

        # develop_ml_models = Task(
        #     config=tasks_config['develop_ml_models'],
        #     agent=ai_ml_engineer,
        #     context=[define_requirements, software_architect]
        # )

        # #-----------------simple task------------------#
        # code_task = Task(
        #     config=tasks_config['code_task'],
        #     agent=senior_fullstack_engineer_agent
        # )

        # review_task = Task(
        #     config=tasks_config['review_task'],
        #     agent=qa_engineer_agent,
        #     context=[code_task]
        # )

        # evaluate_task = Task(
        #     config=tasks_config['evaluate_task'],
        #     agent=chief_qa_engineer_agent,
        #     context=[review_task]
        # )

        # write_documentation = Task(
        #     config=tasks_config['write_documentation'],
        #     agent=technical_writer,
        #     context=[evaluate_task]
        # )

        # code_aggregation_task = Task(         
        #     config=tasks_config['code_aggregation_task'],
        #     agent=code_aggregator_agent,
        #     context=[evaluate_task, write_documentation]
        # )
        # #----------------------------------------------#

        # return Crew(
        #     agents=[
        #         product_owner,
        #         scrum_master,
        #         software_architect,
        #         frontend_developer,
        #         backend_developer,
        #         database_engineer,
        #         devops_engineer,
        #         qa_engineer,
        #         security_engineer,
        #         technical_writer,
        #         ux_ui_designer,
        #         business_analyst,
        #         ai_ml_engineer,
        #         senior_fullstack_engineer_agent,
        #         qa_engineer_agent,
        #         chief_qa_engineer_agent,
        #         technical_writer,
        #         code_aggregator_agent
        #     ],
        #     tasks=[
        #         define_requirements,
        #         manage_sprints,
        #         design_architecture,
        #         develop_frontend,
        #         develop_backend,
        #         manage_database,
        #         implement_devops,
        #         execute_tests,
        #         ensure_security,
        #         write_documentation,
        #         design_ui_ux,
        #         analyze_business,
        #         develop_ml_models,
        #         code_task,
        #         review_task,
        #         evaluate_task,
        #         write_documentation,
        #         code_aggregation_task
        #     ],
        #     verbose=True
        # )