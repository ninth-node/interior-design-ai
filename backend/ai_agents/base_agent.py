"""
Base Agent class for LangGraph multi-agent system
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from shared.config import settings


class BaseAgent(ABC):
    """Base class for all AI agents in the system"""

    def __init__(
        self,
        name: str,
        role: str,
        model_provider: str = "openai",
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7
    ):
        self.name = name
        self.role = role
        self.model_provider = model_provider
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the language model based on provider"""
        if self.model_provider == "openai":
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=settings.OPENAI_API_KEY
            )
        elif self.model_provider == "anthropic":
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                api_key=settings.ANTHROPIC_API_KEY
            )
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return agent output
        Must be implemented by each specific agent
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent
        Must be implemented by each specific agent
        """
        pass

    async def invoke(self, messages: List[BaseMessage]) -> Any:
        """Invoke the language model with messages"""
        return await self.llm.ainvoke(messages)

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent metadata"""
        return {
            "name": self.name,
            "role": self.role,
            "model_provider": self.model_provider,
            "model_name": self.model_name,
            "capabilities": self.get_capabilities()
        }

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get list of agent capabilities
        Must be implemented by each specific agent
        """
        pass
