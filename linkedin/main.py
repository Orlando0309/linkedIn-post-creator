from typing import TypedDict, Annotated, Sequence, Union, List, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import operator
from dotenv import load_dotenv
from prompt import WRITER_PROMPT, CHECKER_PROMPT

# Define our state
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    next_step: str
    post_content: str
    post_review: str
    input_params: dict
    iterations: int

def generate_post(state: AgentState) -> AgentState:
    """Generate the LinkedIn post using the writer prompt."""
    prompt = ChatPromptTemplate.from_template(WRITER_PROMPT)
    
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke(
        prompt.format(
            theme=state["input_params"]["theme"],
            style=state["input_params"]["style"],
            job_title_and_industry=state["input_params"]["job_title_and_industry"],
            audience=state["input_params"]["audience"],
            objective=state["input_params"]["objective"],
            media_context=state["input_params"]["media_context"]
        )
    )
    
    state["post_content"] = response.content
    state["next_step"] = "review_post"
    return state

def review_post(state: AgentState) -> AgentState:
    """Review the generated post using the checker prompt."""
    prompt = ChatPromptTemplate.from_template(CHECKER_PROMPT)
    
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    response = llm.invoke(
        prompt.format(
            post=state["post_content"],
            theme=state["input_params"]["theme"],
            style=state["input_params"]["style"],
            job_title_and_industry=state["input_params"]["job_title_and_industry"],
            audience=state["input_params"]["audience"],
            objective=state["input_params"]["objective"],
            media_context=state["input_params"]["media_context"]
        )
    )
    
    state["post_review"] = response.content
    state["iterations"] += 1
    return state

def should_continue(state: AgentState) -> Literal["generate_post", "end"]:
    """Determine if we should continue refining based on the review."""
    if "❌ REVISIONS NEEDED" in state["post_review"] and state["iterations"] < 3:
        return "generate_post"
    return "end"

def create_linkedin_graph() -> StateGraph:
    """Create the LinkedIn post generation workflow graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("generate_post", generate_post)
    workflow.add_node("review_post", review_post)
    
    # Add edges
    workflow.add_edge("generate_post", "review_post")
    
    # Define the conditional edges
    edges = {
        "generate_post": "generate_post",
        "end": END
    }
    
    # Add conditional edges from review_post
    workflow.add_conditional_edges(
        "review_post",
        should_continue,
        edges
    )
    
    # Set entrypoint
    workflow.set_entry_point("generate_post")
    
    return workflow.compile()

async def main():
    load_dotenv()
    
    # Initialize state with input parameters
    initial_state = {
        "messages": [],
        "next_step": "generate_post",
        "post_content": "",
        "post_review": "",
        "iterations": 0,
        "input_params": {
            "theme": "AI and its impact on software development",
            "style": "insightful",
            "job_title_and_industry": "Senior Software Engineer in AI/ML",
            "audience": "Software developers and tech leaders",
            "objective": "Share insights about AI's impact on development practices",
            "media_context": "Recent experience implementing AI in legacy systems"
        }
    }
    
    # Create and run the graph
    workflow = create_linkedin_graph()
    final_state = await workflow.ainvoke(initial_state)
    
    # Print the results
    print("\nFinal LinkedIn Post:")
    print("-" * 50)
    print(final_state["post_content"])
    print("\nFinal Review:")
    print("-" * 50)
    print(final_state["post_review"])
    print(f"\nNumber of iterations: {final_state['iterations']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 