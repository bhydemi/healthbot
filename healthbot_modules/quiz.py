from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from typing import Tuple

class QuizService:
    """Handles quiz generation and grading"""
    
    @staticmethod
    def generate_quiz_question(llm: ChatOpenAI, topic: str, summary: str) -> Tuple[str, str]:
        """Generate quiz question based ONLY on summary"""
        system_message = SystemMessage(content="""You are creating educational quiz questions for patient comprehension testing. 
        Use ONLY the provided summary to create the quiz question. Do not use external knowledge.""")
        
        human_message = HumanMessage(content=f"""
        Based ONLY on the following health information summary about "{topic}", 
        create ONE multiple choice question to test patient understanding.
        
        Requirements:
        - Question must be answerable using the summary alone
        - Test understanding of key concepts from the summary
        - Use information that appears in the summary only
        - Make it appropriate for a general audience
        - Have one clearly correct answer based on the summary
        - Make incorrect options plausible but clearly wrong based on the summary
        
        Format EXACTLY as shown:
        Question: [Your question here]
        A) [Option A]
        B) [Option B] 
        C) [Option C]
        D) [Option D]
        Correct Answer: [A, B, C, or D]
        
        Health Information Summary (your ONLY data source):
        {summary}
        """)
        
        response = llm.invoke([system_message, human_message])
        quiz_content = response.content
        
        # Parse the correct answer
        lines = quiz_content.split('\n')
        correct_answer = None
        for line in lines:
            if line.startswith('Correct Answer:'):
                correct_answer = line.split(':')[1].strip()
                break
        
        return quiz_content, correct_answer
    
    @staticmethod
    def grade_quiz_answer(llm: ChatOpenAI, topic: str, quiz_question: str, 
                         patient_answer: str, correct_answer: str, summary: str) -> Tuple[str, str]:
        """Grade patient's quiz answer using ONLY the summary"""
        is_correct = patient_answer == correct_answer
        
        system_message = SystemMessage(content="""You are providing educational feedback on a health quiz question. 
        Be encouraging and educational. Use ONLY the provided summary for all explanations and justifications.""")
        
        human_message = HumanMessage(content=f"""
        Grade a patient's quiz answer about "{topic}".
        
        Patient answered: {patient_answer}
        Correct answer: {correct_answer}
        Result: {"CORRECT" if is_correct else "INCORRECT"}
        
        Provide grading feedback that includes:
        1. Clear grade (A for correct, F for incorrect)
        2. Justification for why the correct answer is right using ONLY the summary
        3. Specific references and citations from the health summary
        4. Educational reinforcement of key concepts from the summary
        5. Encouraging tone regardless of correctness
        6. Use ONLY information from the provided summary - no external knowledge
        
        Quiz Question and Options:
        {quiz_question}
        
        Health Information Summary (your ONLY reference for grading justification):
        {summary}
        """)
        
        response = llm.invoke([system_message, human_message])
        feedback = response.content
        grade = "A" if is_correct else "F"
        
        return grade, feedback