from typing import TypedDict, List, Optional, Literal

class HealthBotState(TypedDict):
    """LangGraph-style state object for HealthBot workflow"""
    messages: List[dict]
    current_topic: Optional[str]
    search_results: Optional[List[dict]]
    summary: Optional[str]
    quiz_question: Optional[str]
    correct_answer: Optional[str]
    patient_answer: Optional[str]
    quiz_feedback: Optional[str]
    should_continue: Optional[bool]
    workflow_step: Literal[
        "get_topic", "search", "summarize", "present_info", 
        "generate_quiz", "present_quiz", "grade_quiz", "check_continue", "end"
    ]

class StateManager:
    """Manages workflow state creation and transitions"""
    
    @staticmethod
    def create_initial_state() -> HealthBotState:
        """Create initial state for the workflow"""
        return HealthBotState(
            messages=[],
            current_topic=None,
            search_results=None,
            summary=None,
            quiz_question=None,
            correct_answer=None,
            patient_answer=None,
            quiz_feedback=None,
            should_continue=True,
            workflow_step="get_topic"
        )
    
    @staticmethod
    def reset_state_for_new_topic() -> HealthBotState:
        """Reset state for new topic while maintaining workflow structure"""
        return StateManager.create_initial_state()
    
    @staticmethod
    def update_state(state: HealthBotState, **kwargs) -> HealthBotState:
        """Update state with new values"""
        new_state = state.copy()
        for key, value in kwargs.items():
            if key in new_state:
                new_state[key] = value
        return new_state
    
    @staticmethod
    def add_message(state: HealthBotState, msg_type: str, content: str, **extra_data) -> HealthBotState:
        """Add a message to the state"""
        new_state = state.copy()
        message = {"type": msg_type, "content": content}
        message.update(extra_data)
        new_state["messages"].append(message)
        return new_state