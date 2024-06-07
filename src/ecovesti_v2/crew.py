from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ecovesti_v2.tools.webtools import WebTools

# Uncomment the following line to use an example of a custom tool
# from ecovesti_v2.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class EcovestiV2Crew():
	"""EcovestiV2 crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def product_information_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['product_information_extractor'],
			#tool=[WebTools.open_page],
			Verbose=True,
		)
	
	@agent
	def sustainability_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainability_analyst'],
			# tool=[#WebTools.open_page,
		 	# 	 #WebTools.search_internet,	
			# ],
			Verbose=True,
		)
	
	@agent
	def sustainable_product_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainable_product_researcher'],
			tool=[#WebTools.open_page,
		 		  WebTools.search_internet,
			],
			Verbose=True,
		)
	
	@task
	def product_info_extraction(self) -> Task:
		return Task(
			config=self.tasks_config['product_info_extraction'],
			agent=self.product_information_extractor(),
			output_file="product-information.md",
		)
	
	@task
	def sustainability_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['sustainability_analysis'],
			agent=self.sustainability_analyst(),
		)
	
	@task
	def sustainable_product_research(self) -> Task:
		return Task(
			config=self.tasks_config['sustainable_product_research'],
			agent=self.sustainable_product_researcher(),
			output_file="alternative-sustainable-products.md",
		)
	
	@task
	def final_product_report(self) -> Task:
		return Task(
			config=self.tasks_config['final_product_report'],
			agent=self.sustainability_analyst(),
			output_file="final-product-report.md",
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the EcovestiV2 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)