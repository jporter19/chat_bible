#%%
from pprint import pprint
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"]
os.environ["OPENAI_API_KEY"]
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo")

# %%
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

user_rep = "When is Christmas" 
#ai_resp = 
#model.invoke([HumanMessage(content=user_rep)])
pprint("hi there")
print(ai_resp.content) 
print(ai_resp.response_metadata['token_usage'])   # completion, prompt and total tokens
print(ai_resp.response_metadata['token_usage']['total_tokens']) # value of total



#%%
model.invoke([HumanMessage(content="What's my name?")])
# %%
from langchain_core.messages import AIMessage
model.invoke(
    [
        HumanMessage(content="Hi! I'm Bob"),
        AIMessage(content="Hello Bob! How can I assist you today?"),
        HumanMessage(content="What's my name?"),
    ]
)

#%% ---------------------- Message History -----------------------------

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
with_message_history = RunnableWithMessageHistory(model, get_session_history)
# %%
config = {"configurable": {"session_id": "abc2"}}
response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Bob")],
    config=config,
)
response.content

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)
response.content

#%% --------------------------- Prompt Template ----------------------------
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model

#%%
response = chain.invoke({"messages": [HumanMessage(content="hi! I'm bob")]})
response.content

# %%