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
                sysprompt = prompts.new_prompt
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
    
    def create_prompt(self, attributes):
        # Construct the traits as a comma-delimited string
        traits = ", ".join(attributes)
        
        # Define the system prompt
        sysprompt = f"You are an imaginative writer. Create a system prompt for a fictional character using the following attributes: {traits}. The prompt should be in the form of a narative description without location details that will help the writer to embody the character. Start the prompt with 'You are a' followed by the character's name and the description."
        query = "Please generate the character prompt."
        # Create the ChatPromptTemplate using SystemMessage and HumanMessagePromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=sysprompt),
            HumanMessagePromptTemplate.from_template(query)
        ])
        chain = prompt | self.llm_chat | StrOutputParser()
        # Invoke the chain to get the result
        result = chain.invoke({"topic": query})
        modifier = """
        As you respond, fully embody these traits, bringing out the complexity of your character in every interaction.

        If you describe actions make sure to keep them from a neutral perspective, as if you were describing them to someone else.

        Do not provide any inner thoughts or feelings, only describe what you do and say."""
        result = result + "\n" + modifier
        return result