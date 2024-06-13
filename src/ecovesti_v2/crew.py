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
	def productInformationExtractor(self) -> Agent:
		return Agent(
			config=self.agents_config['productInformationExtractor'],
			#tool=[WebTools.open_page],
			Verbose=True,
		)
	
	@agent
	def sustainabilityAnalyst(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainabilityAnalyst'],
			# tool=[#WebTools.open_page,
		 	# 	 #WebTools.search_internet,	
			# ],
			Verbose=True,
		)
	
	@agent
	def sustainableProductResearcher(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainableProductResearcher'],
			tool=[#WebTools.open_page,
		 		  WebTools.search_internet,
			],
			Verbose=True,
		)
	
	@task
	def productInfoExtraction(self) -> Task:
		return Task(
			config=self.tasks_config['productInfoExtraction'],
			agent=self.productInformationExtractor(),
		)
	
	@task
	def sustainabilityAnalysis(self) -> Task:
		return Task(
			config=self.tasks_config['sustainabilityAnalysis'],
			agent=self.sustainabilityAnalyst(),
			#context=[self.productInfoExtraction],
		)
	
	@task
	def sustainableProductResearch(self) -> Task:
		return Task(
			config=self.tasks_config['sustainableProductResearch'],
			agent=self.sustainableProductResearcher(),
			#context=[self.product_info_extraction],
		)
	
	@task
	def finalProductReport(self) -> Task:
		return Task(
			config=self.tasks_config['finalProductReport'],
			agent=self.sustainabilityAnalyst(),
			#context=[self.product_info_extraction, self.sustainability_analysis, self.sustainable_product_research],
			#output_file="final-product-report.md",
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