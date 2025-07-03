from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
from ..model.transformer_model import TransformerCodeAnalyzer

app = FastAPI(
    title="Code Analysis API",
    description="API for analyzing code quality and providing suggestions",
    version="1.0.0"
)

# Initialize model
model = TransformerCodeAnalyzer()

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    context: Optional[Dict] = None

class CodeAnalysisResponse(BaseModel):
    issues: List[Dict]
    suggestions: List[Dict]
    metrics: List[Dict]

@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code and return suggestions.
    """
    try:
        result = model.analyze_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def get_model_info():
    """
    Get information about the model.
    """
    return model.get_model_info()

@app.get("/health")
async def health_check():
    """
    Check if the service is healthy.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 