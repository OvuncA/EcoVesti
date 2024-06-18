from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ecovesti_v2.tools.webtools import WebTools
from langchain_google_genai import ChatGoogleGenerativeAI
import os

api_key = os.getenv("GOOGLE_API_KEY")
Gllm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)

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
			llm=Gllm,
		)
	
	@agent
	def sustainabilityAnalyst(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainabilityAnalyst'],
			# tool=[#WebTools.open_page,
		 	# 	 #WebTools.search_internet,	
			# ],
			Verbose=True,
			llm=Gllm,
		)
	
	@agent
	def sustainableProductResearcher(self) -> Agent:
		return Agent(
			config=self.agents_config['sustainableProductResearcher'],
			tool=[#WebTools.open_page,
		 		  WebTools.search_internet,
			],
			Verbose=True,
			llm=Gllm,
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