from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class SoftwareHouse():
	"""SoftwareHouse crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# @before_kickoff # Optional hook to be executed before the crew starts
	# def pull_data_example(self, inputs):
	# 	inputs['extra_data'] = "This is extra data"
	# 	return inputs

	# @after_kickoff # Optional hook to be executed after the crew has finished
	# def log_results(self, output):
	# 	print(f"Results: {output}")
	# 	return output

	@agent
	def product_owner_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['product_owner_ai'],
			verbose=True
		)

	@agent
	def scrum_master_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['scrum_master_ai'],
			verbose=True
		)

	@agent
	def software_architect_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['software_architect_ai'],
			verbose=True
		)

	@agent
	def frontend_developer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['frontend_developer_ai'],
			verbose=True
		)

	@agent
	def backend_developer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['backend_developer_ai'],
			verbose=True
		)

	@agent
	def database_engineer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['database_engineer_ai'],
			verbose=True
		)

	@agent
	def devops_engineer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['devops_engineer_ai'],
			verbose=True
		)

	@agent
	def qa_engineer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['qa_engineer_ai'],
			verbose=True
		)

	@agent
	def security_engineer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['security_engineer_ai'],
			verbose=True
		)

	@agent
	def technical_writer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_writer_ai'],
			verbose=True
		)

	@agent
	def ux_ui_designer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['ux_ui_designer_ai'],
			verbose=True
		)

	@agent
	def business_analyst_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['business_analyst_ai'],
			verbose=True
		)

	@agent
	def ai_ml_engineer_ai(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_ml_engineer_ai'],
			verbose=True
		)

	@task
	def define_requirements(self) -> Task:
		return Task(
			config=self.tasks_config['define_requirements'],
		)

	@task
	def manage_sprints(self) -> Task:
		return Task(
			config=self.tasks_config['manage_sprints'],
		)

	@task
	def design_architecture(self) -> Task:
		return Task(
			config=self.tasks_config['design_architecture'],
		)

	@task
	def develop_frontend(self) -> Task:
		return Task(
			config=self.tasks_config['develop_frontend'],
		)

	@task
	def develop_backend(self) -> Task:
		return Task(
			config=self.tasks_config['develop_backend'],
		)

	@task
	def manage_database(self) -> Task:
		return Task(
			config=self.tasks_config['manage_database'],
		)

	@task
	def implement_devops(self) -> Task:
		return Task(
			config=self.tasks_config['implement_devops'],
		)

	@task
	def execute_tests(self) -> Task:
		return Task(
			config=self.tasks_config['execute_tests'],
		)

	@task
	def ensure_security(self) -> Task:
		return Task(
			config=self.tasks_config['ensure_security'],
		)

	@task
	def write_documentation(self) -> Task:
		return Task(
			config=self.tasks_config['write_documentation'],
		)

	@task
	def design_ui_ux(self) -> Task:
		return Task(
			config=self.tasks_config['design_ui_ux'],
		)

	@task
	def analyze_business(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_business'],
		)

	@task
	def develop_ml_models(self) -> Task:
		return Task(
			config=self.tasks_config['develop_ml_models'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SoftwareHouse crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
