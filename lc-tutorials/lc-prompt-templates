#%% - 

from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"]
model = ChatOpenAI(model="gpt-3.5-turbo")

#%% - this is leveraging a prompt template
# -  Note that the template has 2 variables {name} and {user_input}
from langchain_core.prompts import ChatPromptTemplate
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

# The following includes values for the variable in the template above
prompt_value = template.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?"
    }
)
# Output or value of prompt_value:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot. Your name is Bob.'),
#        HumanMessage(content='Hello, how are you doing?'),
#        AIMessage(content="I'm doing well, thanks!"),
#        HumanMessage(content='What is your name?')
#    ]
#)

# In addition to Human/AI/Tool/Function messages,
# you can initialize the template with a MessagesPlaceholder
# either using the class directly or with the shorthand tuple syntax:
#%%
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot."),
    # Means the template will receive an optional list of messages under
    # the "conversation" key
    ("placeholder", "{conversation}")
    # Equivalently:
    # MessagesPlaceholder(variable_name="conversation", optional=True)
])

prompt_value = template.invoke(
    {
        "conversation": [
            ("human", "Hi!"),
            ("ai", "How can I assist you today?"),
            ("human", "Can you make me an ice cream sundae?"),
            ("ai", "No.")
        ]
    }
)

# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot.'),
#        HumanMessage(content='Hi!'),
#        AIMessage(content='How can I assist you today?'),
#        HumanMessage(content='Can you make me an ice cream sundae?'),
#        AIMessage(content='No.'),
#    ]
#)

from langchain_core.prompts import ChatPromptTemplate
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is Carl."),
    ("human", "{user_input}"),
])
prompt_value = template.invoke("Hello, there!")
# Equivalent to
# prompt_value = template.invoke({"user_input": "Hello, there!"})

# Output:
#  ChatPromptValue(
#     messages=[
#         SystemMessage(content='You are a helpful AI bot. Your name is Carl.'),
#         HumanMessage(content='Hello, there!'),
#     ]
# )