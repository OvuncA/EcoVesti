# Ecovesti

Ecovesti is a web application designed to promote sustainable fashion. By analyzing a given URL for a clothing product, Ecovesti assesses the sustainability of the brand, provides detailed information about sustainability certifications and practices, and suggests alternative products that align with eco-friendly principles. This is achieved through a multi-agent AI system leveraging the powerful and flexible framework provided by Crewai. The AI agents collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

![ecovesti_gif](https://github.com/OvuncA/EcoVesti/assets/6351370/ccd1661e-4c0b-427e-8bdc-a564ed6ac437)

# Features

**Sustainability Assessment:** Analyze the sustainability of clothing brands.

**Sustainability Information:** Get detailed information about various sustainability certifications, practices and methods.

**Alternative Products:** Discover eco-friendly alternatives similar to the product you searched for.

# How It Works
Ecovesti leverages multiple AI agents and tasks through the Crewai framework to deliver accurate and relevant sustainability information. Here’s a brief overview of the process:

**Input URL:** The user inputs a URL for a clothing product.

**Product information extraction:**  A specialized AI agent retrieves the product information (brand and product name).

**Data Analysis:** Another AI agent analyzes the product and brand for sustainability metrics, communicating with the prior AI agent

**Alternative Suggestions:** A separate specialized agent researches alternative products based on the information provided by the first agent.

**Information Display:**  All the gathered information is compiled into one comprehensive report and displayed to the user.

![ecovesti_agents_gid](https://github.com/OvuncA/EcoVesti/assets/6351370/cb8d78eb-97ee-4563-a0dc-8f41dea312ea)

## Technologies Used

**Python:** version 3.11

**Flask**

**Crewai Framework:** Utilized for creating and managing AI agents and tasks.

**Gemini LLM:** Other LLM alternatives such as OpenAI can be used but as a free option, it performs the best in my opinion

## Installation

Install all the required packages using:

**1. pip install -r requirements.txt**

**2. Create your own .env file and add your GOOGLE API KEY. _Alternatively, you can use an OPENAI API KEY with minor modifications._**
