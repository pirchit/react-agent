import sys
import asyncio
from langchain_core.messages import HumanMessage
from react_agent.graph import graph

async def main():
    # Get the user question from command line or prompt
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Enter your question: ")

    # Prepare the input for the agent
    input_data = {"messages": [HumanMessage(content=question)]}

    # Run the agent
    print("Running agent...\n")
    result = await graph.ainvoke(input_data)

    # Extract and print the final response
    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        print("Agent response:\n")
        print(last_message.content)
    else:
        print("No response from agent.")

if __name__ == "__main__":
    asyncio.run(main()) 