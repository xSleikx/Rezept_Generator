from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
import os
from dotenv import load_dotenv
load_dotenv()

# change diffrent groq model here. Uses groq model as agent with pydantic-ai.
model = GroqModel(
    'meta-llama/llama-4-maverick-17b-128e-instruct', provider=GroqProvider(api_key=os.getenv('GROQ_API_KEY'))
    
)
agent = Agent(model)