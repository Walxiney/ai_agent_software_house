#from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai import Flow
from crewai.flow.flow import listen, start, and_
import yaml
import json

from agent_tasks_crew import AgentsTasksCrew

from dotenv import load_dotenv
load_dotenv()

class SoftwareHouse(Flow):
	"""SoftwareHouse flow"""
	@start()
	def project_description(self):
		"""
		Describe the project.
		"""
		file_path = 'software_house/src/software_house/config/input.yaml'
		with open(file_path, 'r', encoding='utf-8') as file:
			project_yml = yaml.safe_load(file)
			project_info = project_yml["project"]
		return project_info
	
	@listen(project_description)
	def available_agents(self):
		"""
		Load the available agents and tasks from the agents.yaml and tasks.yaml files.
		"""
		# Load the available agents from the agents.yaml file
		agents_file_path = 'software_house/src/software_house/config/agents_few.yaml'
		with open(agents_file_path, 'r', encoding='utf-8') as file:
			agents_data = yaml.safe_load(file)

		# Load the available tasks from the tasks.yaml file
		tasks_file_path = 'software_house/src/software_house/config/tasks_few.yaml'
		with open(tasks_file_path, 'r', encoding='utf-8') as tasks_file:
			tasks_data = yaml.safe_load(tasks_file)

		# Prepare the output in the format required for creating_crew_dev
		agents_tasks = {}
		for task_name, task_details in tasks_data.items():
			agent_name = task_details.get('agent')
			if agent_name in agents_data:
				agents_tasks[agent_name] = task_name

		# return a dictionary with the available agents and tasks
		agents_tasks_output = {"agents_tasks": agents_tasks}
		return agents_tasks_output

	@listen(and_(project_description, available_agents))
	def project_info_and_agents_tasks(self, project_info, agents_tasks_output):
		"""
		Combine the project information and available agents/tasks.
		"""
		# project_info = self.project_description()
		# agents_tasks_output = self.available_agents()
		input_data = project_info[0] | agents_tasks_output
		return input_data

	@listen(project_info_and_agents_tasks)
	def staff_selector(self, input_data):
		"""
		Select the staff for the project.
		"""
		atc = AgentsTasksCrew()
		staff_selected = atc.crew_orchestrator()

		# run the crew
		selected_team = {}
		selected_team = staff_selected.kickoff(input_data)

		self.state["staff_results"] = selected_team

		selected_team_dict = selected_team.raw
		selected_team_json = json.loads(selected_team_dict.encode('utf-8').decode('utf-8'))
		return selected_team_json

	@listen(and_(project_description, staff_selector))
	def sh_start(self, project_info, selected_team_json):
		"""
		Create the crew for the project.
		"""
		atc = AgentsTasksCrew()
		software_house_team = atc.creating_crew_dev(selected_team_json)

		# run the crew
		dev_code = software_house_team.kickoff_for_each(project_info)
		self.state["dev_results"] = dev_code
		return dev_code

if __name__ == "__main__":
	flow = SoftwareHouse()
	flow.plot()
	project_details = flow.project_description()
	# print("#"*50)
	# print(project_details[0])
	# print(type(project_details[0]))
	# print("#"*50)
	agents_tasks_result = flow.available_agents()
	# print("#"*50)
	# print(agents_tasks_result)
	# print(type(agents_tasks_result))
	# print("#"*50)
	input_data = flow.project_info_and_agents_tasks(project_details, agents_tasks_result)
	# print("#"*50)
	# print(input_data)
	# print("#"*50)
	team = flow.staff_selector(input_data)
	print("#"*50)
	print(team)
	print("#"*50)
	code = flow.sh_start(project_details, team)
	# software = flow.kickoff()

	# sh = SoftwareHouse()
	# project_details = sh.project_description()
	# staff_agents_available = sh.available_agents()
	# staff = sh.staff_selector(project_details, staff_agents_available)
	# sh.sh_start(project_details, staff)