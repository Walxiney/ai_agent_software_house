from crewai import Flow
from crewai.flow.flow import listen, start, and_
import json
import yaml
import os
import shutil

from software_house.src.software_house.crew import AgentsTasksCrew
# from crew import AgentsTasksCrew

from dotenv import load_dotenv
load_dotenv()

class SoftwareHouse(Flow):
	"""
	SoftwareHouse flow
	This class defines the flow for the Software House's project.
	It includes methods to describe the project, load available agents and tasks,
	select staff for the project, and create the crew for the project.
	"""

	@start()
	def project_description(self)-> list:
		"""
		Describe the project.
		This method loads the project description from the input.yaml file.
		- input: None
		- output: Project description as a list
		"""
		try:
			file_path = 'software_house/src/software_house/config/input.yaml'
			with open(file_path, 'r', encoding='utf-8') as file:
				project_yml = yaml.safe_load(file)

			project_info = project_yml["project"]
		except FileNotFoundError as e:
			print(f"Error: {e}. Please check the file path for the input.yaml.")
		return project_info

	@listen(project_description)
	def software_architeture(self, project_info:list)-> dict:
		"""
		"""
		try:
			atc=AgentsTasksCrew()
			drawing_architeture = atc.crew_architeture()
			architeture_created = drawing_architeture.kickoff(project_info[0])
			self.state["software_architeture"] = architeture_created
		except Exception as e:
			print(f"Error while running software_architeture: {e}")

		architeture = {}
		try:
			# architeture = architeture_created.raw

			architeture["project_name"] = project_info[0]["project_name"]
			architeture["project_description"] = architeture_created.raw

			# debugging
			print("#"*20,"STAFF SELECTED", "#"*20)
			print(architeture)
			print(type(architeture))
			print("#"*55)

		except Exception as e:
			print(f"Error while converting selected_team to JSON: {e}")
		return architeture

	@listen(project_description)
	def available_agents(self)-> dict:
		"""
		Load the available agents and tasks from the agents.yaml and tasks.yaml files.
		- input: None
		- output: Dictionary containing available agents and tasks
		"""
		try:
			# Load the available agents from the agents.yaml file
			agents_file_path = 'software_house/src/software_house/config/agents_few.yaml'
			with open(agents_file_path, 'r', encoding='utf-8') as file:
				agents_data = yaml.safe_load(file)
		except FileNotFoundError as e:
			print(f"Error: {e}. Please check the file path for the agents_few.yaml.")

		try:
			# Load the available tasks from the tasks.yaml file
			tasks_file_path = 'software_house/src/software_house/config/tasks_few.yaml'
			with open(tasks_file_path, 'r', encoding='utf-8') as tasks_file:
				tasks_data = yaml.safe_load(tasks_file)
		except FileNotFoundError as e:
			print(f"Error: {e}. Please check the file path for the tasks_few.yaml.")

		# Prepare the output in the format required for creating_crew_dev
		agents_tasks = {}
		for task_name, task_details in tasks_data.items():
			agent_name = task_details.get('agent')
			if agent_name in agents_data:
				agents_tasks[agent_name] = task_name
				#agents_tasks[f"{agent_name}_and_goal_{task_name}_and_description"] = [{agent_name: agents_data[agent_name].get('goal')}, {task_name:task_details.get('description')}]

		# print("#"*20,"AGENTS AND TASKS", "#"*20)
		# print(agents_tasks)
		# print("#"*55)

		if not agents_tasks:
			print("Error: No matching agents found for the tasks in the YAML files.")
			return {}
		# return a dictionary with the available agents and tasks
		agents_tasks_output = {"agents_tasks": agents_tasks}
		return agents_tasks_output

	@listen(and_(software_architeture, available_agents))
	# def project_info_and_agents_tasks(self, project_info:list, agents_tasks_output:dict)-> dict:
	def project_info_and_agents_tasks(self, architeture:dict, agents_tasks_output:dict)-> dict:
		"""
		Combine the project information and available agents/tasks.
		This method merges the project information with the available agents and tasks.
		- input: 
			project_info: Project information
			agents_tasks_output: available agents and taskstasks
		- output: Combined input data for the staff selector
		"""
		# if type(project_info[0]) != dict:
		# 	print("Error: project_info[0] is not a dictionary. Please check the project description format.")
		# 	return {}
		if type(architeture) != dict:
			print("Error: project_info[0] is not a dictionary. Please check the project description format.")
			return {}
		if type(agents_tasks_output) != dict:
			print("Error: agents_tasks_output is not a dictionary. Please check the available agents and tasks format.")
			return {}
		
		# Combine project information and available agents_tasks
		input_data = {}
		output_format = {
			"template":{
				"agents_tasks":{"agent_name_1": "task_name_1", "agent_name_2": "task_name_2"},
			}
		}

		try:
			input_data = architeture | agents_tasks_output # project_info[0] | agents_tasks_output
			input_data = input_data | output_format
		except Exception as e:
			print(f"Error while combining the project_info[0] and agents_tasks_output: {e}")

		return input_data

	@listen(project_info_and_agents_tasks)
	def staff_selector(self, input_data:dict)-> dict:
		"""
		Select the staff for the project.
		This method uses the AgentsTasksCrew class to call the crew_orchestrator that is responsible
		for analyse and select the agents based on the project description.
		- input: input_data: Dictionary combining project description and agents and tasks
		- output: Selected team for the project
		"""
		try:
			atc=AgentsTasksCrew()
			staff_selected = atc.crew_orchestrator()
			# run the crew
			selected_team = {}
			selected_team = staff_selected.kickoff(input_data)
			self.state["staff_results"] = selected_team
		except Exception as e:
			print(f"Error while running staff_selected, selecting the staff: {e}")

		try:
			selected_team_dict = selected_team.raw
			selected_team_json = json.loads(selected_team_dict.replace("'","\"").encode('utf-8').decode('utf-8'))
			print("#"*20,"STAFF SELECTED", "#"*20)
			print(selected_team_json)
			print(type(selected_team_json))
			print("#"*55)
		except Exception as e:
			print(f"Error while converting selected_team to JSON: {e}")
		
		return selected_team_json

	@listen(and_(project_info_and_agents_tasks, staff_selector))
	def sh_start(self, input_software_achiteture:dict, selected_team_json:dict):
		"""
		Create the crew for the project.
		This method uses the AgentsTasksCrew class to call the creating_crew_dev that is responsible
		for creating the crew based on the selected team.
		- input: 
			project_info: Project information
			selected_team_json: Selected team for the project in JSON format
		- output: Software house team for the project
		"""
		# folder_name = input_data["project_name"]
		try:
			# Create the crew for the project using the selected team
			atc = AgentsTasksCrew()
			software_house_team = atc.creating_crew_dev(selected_team_json)

			## run the crew
			dev_code = software_house_team.kickoff(input_software_achiteture)
			self.state["dev_results"] = dev_code

		except Exception as e:
			print(f"Error while running sh_start, creating the crew: {e}")

		#return dev_code #software_house_team

	@listen(sh_start)
	def organize_files(self, folder:str="MySoftwareProject"):
		"""
		Organize files in the project folder.
		This method organizes the files generated by the agents in the project folder.
		"""
		target_folder:str=f"software_house/src/software_house/{folder}"
		source_folder = "software_house/src/software_house/agent_output"
		mapping = {
			".py":"src/utils",
			".json":"config",
			".md":"docs",
			".txt":"docs",
			".log":"logs",
			".html":"src/frontend",
			".css":"src/frontend",
			".js":"src/frontend",
			".csv":"data",
			".sql":"data"
		}
		for file_name in os.listdir(source_folder):
			file_path = os.path.join(source_folder, file_name)
			
			if os.path.isfile(file_path):
				ext = os.path.splitext(file_name)[1]
				target_subfolder = mapping.get(ext, "misc")

				destination_path = os.path.join(target_folder, target_subfolder)
				os.makedirs(destination_path, exist_ok=True)

				shutil.move(file_path, os.path.join(destination_path, file_name))
				print(f"Moved: {file_name} -> to -> {target_subfolder}.")


def run_flow():
	flow = SoftwareHouse()
	flow.plot()
	user_input = flow.project_description()
	architeture = flow.software_architeture(user_input)
	agents_available = flow.available_agents()
	architeture_and_available_agents = flow.project_info_and_agents_tasks(architeture, agents_available)
	team = flow.staff_selector(architeture_and_available_agents)
	flow.sh_start(architeture, team)
	flow.organize_files()


if __name__ == "__main__":
	run_flow()
	# flow = SoftwareHouse()
	# flow.plot()

	# project_details = flow.project_description()
	# architeture = flow.software_architeture(project_details)
	# agents_tasks_result = flow.available_agents()
	# input_data = flow.project_info_and_agents_tasks(architeture, agents_tasks_result)
	# team = flow.staff_selector(input_data)
	# flow.sh_start(project_details, team)
	# flow.organize_files()
	# software = flow.kickoff()