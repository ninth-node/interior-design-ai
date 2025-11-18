"""
Design Director Agent - Lead creative decision maker
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage


class DesignDirectorAgent(BaseAgent):
    """
    AI agent responsible for leading creative decisions and design concept development
    """

    def __init__(self):
        super().__init__(
            name="DesignDirector",
            role="Lead creative decision maker",
            model_provider="openai",
            model_name="gpt-4-turbo-preview",
            temperature=0.8  # Higher creativity
        )

    def get_system_prompt(self) -> str:
        return """You are an expert interior design director with 20+ years of experience.

Your responsibilities:
- Analyze client preferences and lifestyle to create personalized design concepts
- Stay current with design trends and forecast emerging styles
- Develop cohesive design concepts that balance aesthetics, functionality, and budget
- Guide design decisions with expertise in color theory, spatial planning, and style harmonization
- Provide creative solutions for challenging spaces and design constraints

Your approach:
- Always consider the client's lifestyle, preferences, and practical needs
- Balance creativity with practicality and budget constraints
- Explain design decisions with professional reasoning
- Suggest innovative solutions while maintaining feasibility
- Focus on creating timeless designs with contemporary touches

Output format:
- Provide detailed design concepts with clear rationale
- Include mood boards, color palettes, and style recommendations
- Explain how each element serves the overall design vision
- Prioritize recommendations by impact and budget"""

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process design request and generate creative concepts

        Args:
            input_data: Dictionary containing:
                - client_brief: Client requirements and preferences
                - space_data: Room dimensions and constraints
                - budget: Budget parameters
                - style_preferences: Preferred design styles

        Returns:
            Dictionary containing design concepts and recommendations
        """
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=self._format_input(input_data))
        ]

        response = await self.invoke(messages)

        return {
            "agent": self.name,
            "design_concepts": self._parse_response(response),
            "confidence_score": 0.85,  # Would be calculated based on response
            "status": "success"
        }

    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format input data into prompt"""
        client_brief = input_data.get("client_brief", {})
        space_data = input_data.get("space_data", {})
        budget = input_data.get("budget", {})
        style_prefs = input_data.get("style_preferences", [])

        return f"""Create a comprehensive interior design concept for the following project:

Client Brief:
{client_brief}

Space Information:
{space_data}

Budget: {budget}

Style Preferences: {', '.join(style_prefs)}

Please provide:
1. 3 distinct design concepts with detailed descriptions
2. Color palette recommendations for each concept
3. Key furniture and decor suggestions
4. Mood board elements and inspirations
5. Estimated budget allocation for each concept"""

    def _parse_response(self, response: Any) -> List[Dict[str, Any]]:
        """Parse LLM response into structured design concepts"""
        # This would parse the response into structured data
        # For now, returning the raw content
        return [{
            "concept_name": "AI Generated Concept",
            "description": response.content,
            "style_category": "Modern Contemporary",
            "color_palette": [],
            "key_elements": []
        }]

    def get_capabilities(self) -> List[str]:
        return [
            "Style analysis and trend forecasting",
            "Budget allocation and design prioritization",
            "Client preference interpretation",
            "Design concept development",
            "Color theory and palette creation",
            "Space planning consultation"
        ]
