#%%
# import getpass
import os
key = os.environ["OPENAI_API_KEY"]
# os.environ["OPENAI_API_KEY"] = getpass.getpass()
#%%----------------------------------------------------------
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo")

#%%----------------------------------------------------------
from langchain_core.messages import HumanMessage, SystemMessage
messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]
model.invoke(messages)
#%%------------------- Output Parser ------------------------------
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
result = model.invoke(messages)
parser.invoke(result)

#%%---------------------- This is a Chain  ------------------------
chain = model | parser
chain.invoke(messages)

#%%---------------------Prompt Templates  -----------------------------
from langchain_core.prompts import ChatPromptTemplate
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")])
result = prompt_template.invoke({"language": "italian", "text": "hi"})
# result
result.to_messages()
#%%----------------------- Next Chain------------------------------------
chain = prompt_template | model | parser
chain.invoke({"language": "italian", "text": "hi"})

# %%-------------------- Remote Runnable --------------------------------
# THIS WILL NOT WORK!! unless server.py is running from the command line
from langserve import RemoteRunnable
remote_chain = RemoteRunnable("http://localhost:8000/chain/")
remote_chain.invoke({"language": "spanish", "text": "what time is it"})

