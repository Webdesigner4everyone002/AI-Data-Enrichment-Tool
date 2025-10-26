# llm_agent.py
import os
from langchain.schema import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# TODO: Replace with Gemini client once available
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=GEMINI_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def extract_info(entity, prompt_template, search_results):
    """
    Extracts information from search results using an LLM.
    
    Args:
        entity (str): The entity being searched.
        prompt_template (str): The prompt template with {entity} placeholder.
        search_results (list): List of search result dicts with 'title', 'snippet', 'link'.
    
    Returns:
        str: Extracted information.
    """
    system_msg = "You are an assistant that extracts the requested information from search results. Return only the extracted value."
    
    search_text = ""
    for idx, r in enumerate(search_results, 1):
        search_text += f"{idx}) Title: {r['title']}\nSnippet: {r['snippet']}\nURL: {r['link']}\n\n"
    
    user_msg = prompt_template.replace("{entity}", entity) + "\nSearch Results:\n" + search_text
    
    response = llm([SystemMessage(content=system_msg), HumanMessage(content=user_msg)])
    return response.content
