"""
Feedback Service
Captures and stores feedback data about AI performance
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from sqlmodel import Session


logger = logging.getLogger(__name__)


class FeedbackService:
    """Captures and stores feedback data about AI performance"""
    
    @staticmethod
    def log_ai_misinterpretation(user_input: str, ai_response: str, expected_response: Optional[str] = None, 
                                conversation_context: Optional[str] = None, user_id: Optional[str] = None) -> None:
        """Log AI misinterpretations for future improvements"""
        feedback_data = {
            "user_input": user_input,
            "ai_response": ai_response,
            "expected_response": expected_response,
            "conversation_context": conversation_context,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"AI Misinterpretation Logged: {feedback_data}")
    
    @staticmethod
    def log_tool_execution_error(tool_name: str, parameters: Dict[str, Any], error: str, 
                                conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> None:
        """Log errors in tool execution"""
        feedback_data = {
            "tool_name": tool_name,
            "parameters": parameters,
            "error": error,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.error(f"Tool Execution Error Logged: {feedback_data}")
    
    @staticmethod
    def log_nlp_accuracy_issue(user_input: str, parsed_intent: str, executed_action: str, 
                              expected_action: Optional[str] = None, confidence_score: Optional[float] = None) -> None:
        """Log NLP accuracy issues"""
        feedback_data = {
            "user_input": user_input,
            "parsed_intent": parsed_intent,
            "executed_action": executed_action,
            "expected_action": expected_action,
            "confidence_score": confidence_score,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.warning(f"NLP Accuracy Issue Logged: {feedback_data}")
    
    @staticmethod
    def log_user_satisfaction(conversation_id: str, rating: int, comment: Optional[str] = None, 
                             user_id: Optional[str] = None) -> None:
        """Log user satisfaction ratings"""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        feedback_data = {
            "conversation_id": conversation_id,
            "rating": rating,
            "comment": comment,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"User Satisfaction Logged: {feedback_data}")
    
    @staticmethod
    def store_feedback_for_analysis(feedback_type: str, data: Dict[str, Any], 
                                   session: Optional[Session] = None) -> None:
        """Store feedback for later analysis (placeholder implementation)"""
        # In a real implementation, this would store feedback in a database
        # or send it to an analytics system
        feedback_record = {
            "type": feedback_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Feedback Stored for Analysis: {feedback_record}")