# FastMcp Project

Welcome to the **FastMcp** project! This repository contains two main components:

1. **MCP Server** – A modular server (in `server.py`) with configuration and test integration.
2. **LinkedIn Post Writer** – An advanced LinkedIn post generator using LangChain, LangGraph, and Streamlit.

---

## 1. MCP Server

### Overview
The MCP server is a Python-based server designed for modular, configurable operation. It can be started independently and is designed to be easily integrated with other tools or scripts.

### Features
- Configurable via `config.json`
- Simple test integration (e.g., addition test)
- Easy to extend for new endpoints or logic

### Setup & Usage

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the server**
   Edit `config.json` to set host, port, and API endpoint as needed:
   ```json
   {
     "server": {
       "host": "localhost",
       "port": 8000,
       "protocol": "http"
     },
     "api": {
       "endpoint": "/calculate",
       "timeout": 30
     }
   }
   ```

3. **Run the server**
   ```bash
   python server.py
   ```

4. **Test integration**
   The `main.py` script demonstrates loading the config and running a simple addition test using LangChain.
   ```bash
   python main.py
   ```

---

## 2. LinkedIn Post Writer

### Overview
The LinkedIn Post Writer is a modern, AI-powered tool for generating high-quality LinkedIn posts. It offers two engines:
- **LangGraph**: Iterative, with AI review and feedback
- **Chain**: Classic, single-pass pipeline

It features a beautiful Streamlit web interface for easy use.

### Features
- Choose between LangGraph (iterative) and Chain (single-pass) engines
- Fill in all required post parameters in a friendly, emoji-rich UI
- AI-powered post writing and review (using OpenAI GPT-4)
- Spinner and success messages for a delightful user experience
- Copy-paste ready output and AI feedback

### Setup & Usage

1. **Install dependencies**
   ```bash
   pip install -r linkedin/requirements.txt
   ```

2. **Set your OpenAI API key**
   Create a `.env` file in the `linkedin/` directory:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run linkedin/streamlit_app.py
   ```

4. **Use the app**
   - Fill in the post details (theme, style, job title, audience, etc.)
   - Choose your engine (LangGraph or Chain)
   - Click "Generate My LinkedIn Post!"
   - Copy your post and review/feedback as needed

### File Structure
```
linkedin/
├── main.py              # LangGraph implementation
├── chain_version.py     # Chain (pipe) implementation
├── prompt.py            # Prompts for writer and checker
├── requirements.txt     # Dependencies for LinkedIn project
├── streamlit_app.py     # Streamlit web interface
```

---

## Project Structure
```
.
├── main.py              # MCP test integration
├── server.py            # (Your MCP server implementation)
├── config.json          # Server configuration
├── linkedin/            # LinkedIn post writer project
│   ├── main.py
│   ├── chain_version.py
│   ├── prompt.py
│   ├── requirements.txt
│   └── streamlit_app.py
└── README.md            # This file
```

---

## License
This project is for educational and demonstration purposes. Please check individual package licenses for production use.

---

## Credits
- Built with [LangChain](https://python.langchain.com/), [LangGraph](https://github.com/langchain-ai/langgraph), [Streamlit](https://streamlit.io/), and [OpenAI](https://openai.com/).
- UI inspired by modern SaaS best practices.
