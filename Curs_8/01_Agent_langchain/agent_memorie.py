from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer in Romanian."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

history = []

print('Agent cu memorie (scrie exit pentru a ieși)')

while True:
    user_input = input('Tu: ')
    if user_input.lower() == 'exit':
        break

    response = chain.invoke({"input": user_input, "history": history})

    # history.append(HumanMessage(content=user_input))
    # history.append(AIMessage(content=response))

    print(f'Agent: {response}')
