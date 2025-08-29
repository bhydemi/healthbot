import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from .state import StateManager
from .nodes import HealthBotNodes

class HealthBotWorkflow:
    """Main workflow orchestrator for HealthBot"""
    
    def __init__(self):
        self._setup_environment()
        self._initialize_llm_and_tools()
        self.nodes = HealthBotNodes(self.llm, self.llm_with_tools)
    
    def _setup_environment(self):
        """Load environment variables and validate API keys"""
        load_dotenv('config.env')
        
        assert os.getenv('OPENAI_API_KEY') is not None, "OPENAI_API_KEY not found in config.env"
        assert os.getenv('TAVILY_API_KEY') is not None, "TAVILY_API_KEY not found in config.env"
    
    def _initialize_llm_and_tools(self):
        """Initialize OpenAI LLM and bind Tavily tool"""
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        
        search_tool = TavilySearchResults(
            max_results=3,
            search_depth="advanced",
            include_domains=["mayoclinic.org", "webmd.com", "nih.gov", "cdc.gov", "healthline.com", "medlineplus.gov"]
        )
        
        # Bind Tavily tool to OpenAI for function calling
        self.llm_with_tools = self.llm.bind_tools([search_tool])
    
    def execute_workflow(self):
        """Execute the complete LangGraph-style workflow with state management"""
        print("Initializing HealthBot LangGraph workflow...")
        
        # Initialize state
        state = StateManager.create_initial_state()
        
        try:
            # Main workflow loop with LangGraph-style node execution
            while state["should_continue"] and state["workflow_step"] != "end":
                
                # Node execution based on workflow step (LangGraph-style edges)
                if state["workflow_step"] == "get_topic":
                    state = self.nodes.get_topic_node(state)
                    
                elif state["workflow_step"] == "search":
                    state = self.nodes.search_node(state)
                    
                elif state["workflow_step"] == "summarize":
                    state = self.nodes.summarize_node(state)
                    
                elif state["workflow_step"] == "present_info":
                    state = self.nodes.present_info_node(state)
                    
                elif state["workflow_step"] == "generate_quiz":
                    state = self.nodes.generate_quiz_node(state)
                    
                elif state["workflow_step"] == "present_quiz":
                    state = self.nodes.present_quiz_node(state)
                    
                elif state["workflow_step"] == "grade_quiz":
                    state = self.nodes.grade_quiz_node(state)
                    
                elif state["workflow_step"] == "check_continue":
                    state = self.nodes.check_continue_node(state)
                    
        except KeyboardInterrupt:
            print("\n\nHealthBot session ended by user. Stay healthy!")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please check your API keys and try again.")
        finally:
            print("\nThank you for using HealthBot!")
            print(f"\nSession Summary: Processed {len(state['messages'])} workflow steps")