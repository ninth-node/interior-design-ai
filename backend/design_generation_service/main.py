"""
Design Generation Service - AI design creation and style analysis
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import sys
sys.path.append('..')

from ai_agents.design_director_agent import DesignDirectorAgent

app = FastAPI(
    title="Design Generation Service",
    version="0.1.0"
)

# Initialize AI agents
design_director = DesignDirectorAgent()


class DesignRequest(BaseModel):
    """Design generation request"""
    client_brief: Dict[str, Any]
    space_data: Dict[str, Any]
    budget: Dict[str, Any]
    style_preferences: List[str]


class DesignResponse(BaseModel):
    """Design generation response"""
    agent: str
    design_concepts: List[Dict[str, Any]]
    confidence_score: float
    status: str


@app.get("/")
async def root():
    return {
        "service": "Design Generation Service",
        "status": "operational",
        "version": "0.1.0"
    }


@app.post("/generate-design", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    """
    Generate design concepts using AI
    """
    try:
        input_data = {
            "client_brief": request.client_brief,
            "space_data": request.space_data,
            "budget": request.budget,
            "style_preferences": request.style_preferences
        }

        result = await design_director.process(input_data)
        return DesignResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent-info")
async def get_agent_info():
    """Get information about available AI agents"""
    return {
        "design_director": design_director.get_agent_info()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
