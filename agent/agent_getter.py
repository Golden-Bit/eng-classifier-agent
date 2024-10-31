from typing import Any

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from prompt_getter import get_prompt
from utilities.tools.dataloader import DocumentToolKitManager
from utilities.tools.mongodb import MongoDBToolKitManager


def get_chain(llm: Any = None,
              connection_string: str = "mongodb://localhost:27017",
              default_database: str = None,
              default_collection: str = None):

    if connection_string:
        # Initialize the MongoDB tools
        mongo_tools = MongoDBToolKitManager(
            connection_string=connection_string,
            default_database=default_database,
            default_collection=default_collection,
        ).get_tools()
    else:
        mongo_tools = []

    # Inizializza gli strumenti per i documenti
    doc_tools = DocumentToolKitManager().get_tools()

    tools = mongo_tools + doc_tools

    # Get the prompt to use - you can modify this!
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", get_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),  # Placeholder richiesto per i passaggi intermedi
        ]
    )

    agent = create_openai_tools_agent(
        llm.with_config({"tags": ["agent_llm"]}), tools, prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_config(
        {"run_name": "Agent"}
    )
    return agent_executor


# esempio di utilizzo
if __name__ == "__main__":

    llm = ChatOpenAI(
        temperature=0,
        streaming=True,
        api_key="............."
    )

    get_chain(
        llm=llm,
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection=None
    )


