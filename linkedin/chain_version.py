from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from prompt import WRITER_PROMPT, CHECKER_PROMPT

def create_linkedin_chain():
    """Create the chain for LinkedIn post generation using pipe operator."""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    output_parser = StrOutputParser()
    
    # Create the writer chain
    writer_prompt = ChatPromptTemplate.from_template(WRITER_PROMPT)
    writer_chain = writer_prompt | llm | output_parser
    
    # Create the checker chain
    checker_prompt = ChatPromptTemplate.from_template(CHECKER_PROMPT)
    checker_chain = checker_prompt | llm | output_parser
    
    # Create functions to extract and format data
    def extract_writer_input(data):
        return data["writer_input"]
    
    def format_checker_input(data):
        writer_output = data["writer_output"]
        input_data = data["writer_input"]
        return {
            "post": writer_output,
            "theme": input_data["theme"],
            "style": input_data["style"],
            "job_title_and_industry": input_data["job_title_and_industry"],
            "audience": input_data["audience"],
            "objective": input_data["objective"],
            "media_context": input_data["media_context"]
        }
    
    # Combine chains using pipe operator
    chain = (
        RunnablePassthrough()
        | {
            "writer_output": (RunnableLambda(extract_writer_input) | writer_chain),
            "writer_input": lambda x: x["writer_input"]
        }
        | RunnableLambda(format_checker_input)
        | checker_chain
    )
    
    return chain

async def main():
    load_dotenv()
    
    # Sample input
    input_data = {
        "writer_input": {
            "theme": "AI and its impact on software development",
            "style": "insightful",
            "job_title_and_industry": "Senior Software Engineer in AI/ML",
            "audience": "Software developers and tech leaders",
            "objective": "Share insights about AI's impact on development practices",
            "media_context": "Recent experience implementing AI in legacy systems"
        }
    }
    
    # Create and run the chain
    linkedin_chain = create_linkedin_chain()
    result = linkedin_chain.invoke(input_data)
    
    # Print results
    print("\nFinal LinkedIn Post Review:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 