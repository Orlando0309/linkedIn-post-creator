import streamlit as st
import asyncio
from main import create_linkedin_graph
from chain_version import create_linkedin_chain

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="💼", layout="centered")

st.title("💡 LinkedIn Post Generator")
st.markdown("""
Welcome! This app helps you craft a high-performing LinkedIn post using either a LangGraph workflow or a classic Chain pipeline. 🚀

*Fill in the details below, choose your engine, and let the AI do the rest!* ✨
""")

# Input fields
with st.form("post_form"):
    theme = st.text_input("🌟 Theme/Topic", "AI and its impact on software development")
    style = st.selectbox("🗣️ Style of Speech", [
        "insightful", "conversational", "storytelling", "concise", "humorous", "professional", "punchy"
    ], index=0)
    job_title_and_industry = st.text_input("💼 Job Title & Industry", "Senior Software Engineer in AI/ML")
    audience = st.text_input("🎯 Target Audience", "Software developers and tech leaders")
    objective = st.text_input("🎯 Primary Objective", "Share insights about AI's impact on development practices")
    media_context = st.text_input("📝 Personal Story or Media/Context (optional)", "Recent experience implementing AI in legacy systems")
    engine = st.radio("🤖 Choose your engine:", ["LangGraph", "Chain"], index=0, help="LangGraph supports iterative review, Chain is a single-pass pipeline.")
    submitted = st.form_submit_button("✨ Generate My LinkedIn Post!")

if submitted:
    st.info("Thinking... Generating your post. Please wait! 🧠⏳")
    input_data = {
        "theme": theme,
        "style": style,
        "job_title_and_industry": job_title_and_industry,
        "audience": audience,
        "objective": objective,
        "media_context": media_context
    }
    post = None
    review = None
    iterations = None
    if engine == "LangGraph":
        async def run_langgraph():
            workflow = create_linkedin_graph()
            initial_state = {
                "messages": [],
                "next_step": "generate_post",
                "post_content": "",
                "post_review": "",
                "iterations": 0,
                "input_params": input_data
            }
            final_state = await workflow.ainvoke(initial_state)
            return final_state
        with st.spinner("LangGraph is thinking... 🤔"):
            final_state = asyncio.run(run_langgraph())
            post = final_state["post_content"]
            review = final_state["post_review"]
            iterations = final_state["iterations"]
    else:
        chain = create_linkedin_chain()
        chain_input = {"writer_input": input_data}
        with st.spinner("Chain is thinking... 🤔"):
            result = chain.invoke(chain_input)
            post = result
            review = None
            iterations = 1
    st.success("Your LinkedIn post is ready! 🎉")
    st.markdown("""
    ## 📝 Your LinkedIn Post
    """)
    st.text_area("Copy and share this post:", post, height=200)
    if review:
        st.markdown("""
        ## 🧐 Review & Feedback
        """)
        st.text_area("AI Review:", review, height=200)
    st.markdown(f"**Iterations:** {iterations if iterations is not None else 1}")
    st.markdown("---")
    st.markdown("Made with ❤️ using [LangChain](https://python.langchain.com/) and [Streamlit](https://streamlit.io/)") 