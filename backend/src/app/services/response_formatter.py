"""
Response Formatter
Formats responses for the API
"""

from typing import Dict, Any, List, Optional


class ResponseFormatter:
    """Formats responses for the API"""
    
    @staticmethod
    def format_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
        """Format a successful response"""
        response = {
            "success": True,
            "data": data
        }
        if message:
            response["message"] = message
        return response
    
    @staticmethod
    def format_error_response(error: str, message: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format an error response"""
        response = {
            "success": False,
            "error": error
        }
        if message:
            response["message"] = message
        if details:
            response["details"] = details
        return response
    
    @staticmethod
    def format_ai_response(ai_text: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Format an AI response"""
        response = {
            "response": ai_text,
            "type": "ai_response"
        }
        if tool_calls:
            response["tool_calls"] = tool_calls
        return response
    
    @staticmethod
    def format_fallback_response(provider_name: str, message: str = "Using fallback provider due to primary provider unavailability") -> Dict[str, Any]:
        """Format a fallback response"""
        return {
            "response": message,
            "provider_status": "fallback_active",
            "active_provider": provider_name,
            "type": "fallback_notification"
        }
    
    @staticmethod
    def format_provider_status(provider_name: str, is_available: bool, response_time: Optional[float] = None) -> Dict[str, Any]:
        """Format provider status information"""
        status_info = {
            "provider": provider_name,
            "available": is_available
        }
        if response_time is not None:
            status_info["response_time_ms"] = round(response_time * 1000, 2)
        return status_info