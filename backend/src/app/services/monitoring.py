"""
Monitoring Service
Handles monitoring and logging for AI provider interactions and tool calls
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from ..models.mcp_invocation import MCPToolInvocation
from sqlmodel import Session


logger = logging.getLogger(__name__)


class MonitoringService:
    """Handles monitoring and logging for AI provider interactions and tool calls"""
    
    @staticmethod
    def log_ai_interaction(provider: str, model: str, input_tokens: int, output_tokens: int, 
                          response_time: float, success: bool, error_msg: Optional[str] = None) -> None:
        """Log AI provider interactions"""
        log_data = {
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "response_time_ms": round(response_time * 1000, 2),
            "success": success
        }
        
        if error_msg:
            log_data["error"] = error_msg
        
        logger.info(f"AI Interaction: {log_data}")
    
    @staticmethod
    def log_tool_invocation(session: Session, tool_name: str, user_id: str, conversation_id: str, 
                           parameters: Dict[str, Any], success: bool, result: Optional[Dict[str, Any]] = None, 
                           error_msg: Optional[str] = None) -> Optional[MCPToolInvocation]:
        """Log MCP tool invocations"""
        try:
            invocation = MCPToolInvocation(
                tool_name=tool_name,
                parameters=parameters,
                conversation_id=conversation_id,
                user_id=user_id,
                status="success" if success else "failed",
                result=result,
                error_message=error_msg
            )
            
            session.add(invocation)
            session.commit()
            session.refresh(invocation)
            
            log_data = {
                "tool_name": tool_name,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "success": success
            }
            
            if error_msg:
                log_data["error"] = error_msg
                
            logger.info(f"MCP Tool Invocation: {log_data}")
            
            return invocation
        except Exception as e:
            logger.error(f"Error logging tool invocation: {str(e)}")
            return None
    
    @staticmethod
    def log_provider_failure(provider: str, error_type: str, error_message: str) -> None:
        """Log AI provider failures"""
        log_data = {
            "provider": provider,
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.error(f"Provider Failure: {log_data}")
    
    @staticmethod
    def log_fallback_activation(primary_provider: str, fallback_provider: str, reason: str) -> None:
        """Log when fallback is activated"""
        log_data = {
            "primary_provider": primary_provider,
            "fallback_provider": fallback_provider,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.warning(f"Fallback Activated: {log_data}")
    
    @staticmethod
    def log_performance_metric(metric_name: str, value: float, unit: str = "", tags: Optional[Dict[str, str]] = None) -> None:
        """Log performance metrics"""
        log_data = {
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if tags:
            log_data["tags"] = tags
            
        logger.info(f"Performance Metric: {log_data}")