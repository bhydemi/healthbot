from .state import HealthBotState, StateManager
from .search import MedicalSearchService, MedicalSummarizationService
from .quiz import QuizService

class HealthBotNodes:
    """Individual workflow nodes with single responsibilities"""
    
    def __init__(self, llm, llm_with_tools):
        self.llm = llm
        self.llm_with_tools = llm_with_tools
        self.search_service = MedicalSearchService()
        
    def get_topic_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Get health topic from patient"""
        print("\n" + "="*70)
        print("HEALTHBOT - AI-POWERED PATIENT EDUCATION SYSTEM")
        print("="*70)
        print("I can help you learn about medical conditions, treatments, and health topics.")
        print("All information comes from trusted medical sources like Mayo Clinic, NIH, and CDC.")
        print("="*70)
        
        topic = input("\nWhat health topic or medical condition would you like to learn about?\n>>> ").strip()
        
        if not topic:
            print("Please enter a valid health topic.")
            return state
        
        # Update state
        new_state = StateManager.update_state(state, 
            current_topic=topic,
            workflow_step="search"
        )
        new_state = StateManager.add_message(new_state, "user_input", f"Learning topic: {topic}")
        
        return new_state
    
    def search_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Search medical information using OpenAI + Tavily integration"""
        print(f"\nUsing AI to search trusted medical sources for: '{state['current_topic']}'")
        
        try:
            search_results = self.search_service.search_medical_info(
                state['current_topic'], 
                self.llm_with_tools
            )
            
            print(f"Found {len(search_results)} relevant medical sources!")
            
            # Update state
            new_state = StateManager.update_state(state,
                search_results=search_results,
                workflow_step="summarize"
            )
            new_state = StateManager.add_message(new_state, "search_completed",
                f"OpenAI called Tavily and found {len(search_results)} sources",
                results_count=len(search_results)
            )
            
            return new_state
            
        except Exception as e:
            print(f"Error in search: {str(e)}")
            new_state = StateManager.update_state(state, workflow_step="get_topic")
            return new_state
    
    def summarize_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Summarize search results into patient-friendly format"""
        print("\nCreating patient-friendly summary from search results...")
        
        try:
            summary = MedicalSummarizationService.create_patient_summary(
                self.llm,
                state['current_topic'],
                state['search_results']
            )
            
            print("Patient-friendly summary created from search results!")
            
            # Update state
            new_state = StateManager.update_state(state,
                summary=summary,
                workflow_step="present_info"
            )
            new_state = StateManager.add_message(new_state, "summary_created",
                "3-4 paragraph summary generated using only search results",
                summary=summary
            )
            
            return new_state
            
        except Exception as e:
            print(f"Error creating summary: {str(e)}")
            new_state = StateManager.update_state(state, workflow_step="get_topic")
            return new_state
    
    def present_info_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Present information to patient"""
        print("\n" + "="*70)
        print(f"HEALTH EDUCATION: {state['current_topic'].upper()}")
        print("="*70)
        print(state["summary"])
        print("="*70)
        
        input("\nPlease read the information above carefully.\nPress Enter when you're ready for a comprehension check: ")
        
        # Update state
        new_state = StateManager.update_state(state, workflow_step="generate_quiz")
        new_state = StateManager.add_message(new_state, "info_presented", 
            "Patient has read the health information")
        
        return new_state
    
    def generate_quiz_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Generate quiz question based ONLY on summary"""
        print("\nGenerating comprehension question from the summary...")
        
        try:
            quiz_content, correct_answer = QuizService.generate_quiz_question(
                self.llm,
                state['current_topic'],
                state['summary']
            )
            
            print("Quiz question generated from summary!")
            
            # Update state
            new_state = StateManager.update_state(state,
                quiz_question=quiz_content,
                correct_answer=correct_answer,
                workflow_step="present_quiz"
            )
            new_state = StateManager.add_message(new_state, "quiz_generated",
                "Quiz question created using only summary data",
                quiz=quiz_content
            )
            
            return new_state
            
        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            new_state = StateManager.update_state(state, workflow_step="check_continue")
            return new_state
    
    def present_quiz_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Present quiz to patient and collect answer"""
        print("\n" + "="*60)
        print("COMPREHENSION CHECK")
        print("="*60)
        
        # Display quiz without showing correct answer
        lines = state["quiz_question"].split('\n')
        quiz_display = ""
        
        for line in lines:
            if not line.startswith('Correct Answer:'):
                quiz_display += line + '\n'
                
        print(quiz_display)
        
        patient_answer = input("Please enter your answer (A, B, C, or D): ").strip().upper()
        
        while patient_answer not in ['A', 'B', 'C', 'D']:
            patient_answer = input("Please enter A, B, C, or D: ").strip().upper()
        
        # Update state
        new_state = StateManager.update_state(state,
            patient_answer=patient_answer,
            workflow_step="grade_quiz"
        )
        new_state = StateManager.add_message(new_state, "patient_answer",
            f"Patient answered: {patient_answer}")
        
        return new_state
    
    def grade_quiz_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Grade patient's quiz answer using ONLY the summary"""
        print("\nGrading your answer using the health summary...")
        
        try:
            grade, feedback = QuizService.grade_quiz_answer(
                self.llm,
                state['current_topic'],
                state['quiz_question'],
                state['patient_answer'],
                state['correct_answer'],
                state['summary']
            )
            
            is_correct = grade == "A"
            
            print("\n" + "="*60)
            print("QUIZ RESULTS & FEEDBACK")
            print("="*60)
            print(f"Grade: {grade}")
            if is_correct:
                print("CORRECT!")
            else:
                print("INCORRECT - Let's learn from this!")
            print("-" * 60)
            print(feedback)
            print("="*60)
            
            # Update state
            new_state = StateManager.update_state(state,
                quiz_feedback=feedback,
                workflow_step="check_continue"
            )
            new_state = StateManager.add_message(new_state, "quiz_graded",
                f"Grade: {grade} - Justified using only summary content",
                feedback=feedback,
                correct=is_correct,
                grade=grade
            )
            
            return new_state
            
        except Exception as e:
            print(f"Error grading quiz: {str(e)}")
            new_state = StateManager.update_state(state, workflow_step="check_continue")
            return new_state
    
    def check_continue_node(self, state: HealthBotState) -> HealthBotState:
        """Node: Check if patient wants to continue with new topic"""
        print("\n" + "="*50)
        print("What would you like to do next?")
        print("1. Learn about another health topic")
        print("2. Exit HealthBot")
        
        choice = input("\nEnter 1 or 2: ").strip()
        
        if choice == "1":
            print("\nResetting state for new learning session...")
            # Reset state for new topic (maintains privacy)
            new_state = StateManager.reset_state_for_new_topic()
            return new_state
        elif choice == "2":
            new_state = StateManager.update_state(state,
                should_continue=False,
                workflow_step="end"
            )
            new_state = StateManager.add_message(new_state, "session_end", "Patient chose to exit")
            return new_state
        else:
            print("Please enter 1 or 2.")
            return state