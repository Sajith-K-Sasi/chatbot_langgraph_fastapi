from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile")

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_message}"),
        MessagesPlaceholder("messages")
    ]
)

llm_model = prompt_template|llm