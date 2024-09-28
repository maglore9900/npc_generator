import environ
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from . import prompts

env = environ.Env()
environ.Env.read_env()

class Adapter:
    def __init__(self, llm_type):
        self.llm_text = llm_type
        self.ollama_url = env("OLLAMA_URL")
        self.local_model = env("OLLAMA_MODEL")
        if self.llm_text.lower() == "openai":
            from langchain_openai import ChatOpenAI
            self.llm_chat = ChatOpenAI(
                temperature=0.3, model="gpt-4o", openai_api_key=env("OPENAI_API_KEY")
            )
        elif self.llm_text.lower() == "local":
            from langchain_community.chat_models import ChatOllama 
            self.llm_chat = ChatOllama(
                base_url=self.ollama_url, model=self.local_model
            )    
    def chat_template(self, query, char=None):
        try:
            if not char:
                sysprompt = "You are a helpful assistant."
            elif "alice" in char.lower():
                sysprompt = prompts.Alice
            elif "bob" in char.lower():
                sysprompt = prompts.Bob
            elif "charlie" in char.lower():
                sysprompt = prompts.Charlie
            elif "test" in char.lower():
                sysprompt = prompts.test_prompt
            chat_template = ChatPromptTemplate.from_messages(
                [SystemMessage(content=(sysprompt)),HumanMessagePromptTemplate.from_template(query),])
            return chat_template
        except Exception as e:
            print(e)
            return None
            
    def chat(self, query, char=None):
        prompt = self.chat_template(query, char)   
        chain = prompt | self.llm_chat | StrOutputParser()
        result = chain.invoke({"topic": query})
        return result