from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List

class MedicalSearchService:
    """Handles medical information search using Tavily"""
    
    def __init__(self):
        self.search_tool = TavilySearchResults(
            max_results=3,
            search_depth="advanced",
            include_domains=["mayoclinic.org", "webmd.com", "nih.gov", "cdc.gov", "healthline.com", "medlineplus.gov"]
        )
    
    def search_medical_info(self, topic: str, llm_with_tools: ChatOpenAI) -> List[dict]:
        """Search for medical information using OpenAI + Tavily integration"""
        search_prompt = f"""
        Search for comprehensive, reliable medical information about "{topic}".
        Find information covering:
        - What this condition/topic is
        - Symptoms and signs
        - Causes and risk factors  
        - Treatment options
        - Prevention strategies
        - When to seek medical care
        
        Use the search tool to find current, accurate information from reputable medical sources.
        """
        
        # OpenAI will automatically call Tavily tool when needed
        response = llm_with_tools.invoke([HumanMessage(content=search_prompt)])
        
        # Check if tool was called and get results
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print("OpenAI successfully called Tavily search tool...")
            search_results = []
            for tool_call in response.tool_calls:
                if tool_call['name'] == 'tavily_search_results_json':
                    results = self.search_tool.invoke(tool_call['args'])
                    search_results.extend(results)
        else:
            # Direct search as fallback
            search_query = f"{topic} medical information symptoms treatment causes"
            search_results = self.search_tool.invoke({"query": search_query})
        
        return search_results

class MedicalSummarizationService:
    """Handles summarization of medical search results"""
    
    @staticmethod
    def create_patient_summary(llm: ChatOpenAI, topic: str, search_results: List[dict]) -> str:
        """Create patient-friendly summary from search results"""
        search_content = ""
        sources = []
        for result in search_results:
            url = result.get('url', 'Unknown source')
            sources.append(url)
            search_content += f"Source: {url}\n"
            search_content += f"Content: {result.get('content', '')}\n\n"
        
        
        system_message = SystemMessage(content="""You are a medical education specialist creating patient education materials. 
        Your goal is to make complex medical information accessible to patients while maintaining complete accuracy. 
        Use ONLY the provided search results - do not add information from your training data.""")
        
        human_message = HumanMessage(content=f"""
        Create a comprehensive patient education summary about "{topic}" using ONLY 
        the provided search results. Do not use any other knowledge sources.
        
        Structure your response with these sections:
        ## What is {topic}?
        ## Common Signs and Symptoms  
        ## Causes and Risk Factors
        ## Treatment Options
        ## When to Seek Medical Care
        ## Key Takeaways
        
        Requirements:
        - Write 3-4 comprehensive paragraphs
        - Use simple, patient-friendly language
        - Explain medical terms in parentheses when used
        - Base content ONLY on the provided search results
        - Be encouraging and informative
        
        Search Results from Trusted Medical Sources:
        {search_content}
        
        Sources used: {', '.join(sources)}
        """)
        
        response = llm.invoke([system_message, human_message])
        return response.content