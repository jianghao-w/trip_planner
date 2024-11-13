from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class TripPlanner():
	"""TripPlanner crew"""

	# Specifying the agents and tasks configuration
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# Creating agents
	@agent
	def city_selection_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['city_selection_expert'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			tools=[SearchTools.search_internet]
		)

	@agent
	def local_tour_guide(self) -> Agent:
		return Agent(
			config=self.agents_config['local_tour_guide'],
			verbose=True,
			tools=[SearchTools.search_internet]
		)
	
	@agent
	def expert_travel_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['expert_travel_agent'],
			verbose=True,
			tools=[
				SearchTools.search_internet,
                CalculatorTools.calculate
				]
		)
	

	@task
	def identify_city(self) -> Task:
		return Task(
			config=self.tasks_config['identify_city'],
		)

	@task
	def gather_city_info(self) -> Task:
		return Task(
			config=self.tasks_config['gather_city_info'],
		)
	
	@task
	def plan_itinerary(self) -> Task:
		return Task(
			config=self.tasks_config['plan_itinerary'],
			output_file='final_itineary.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TripPlanner crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
