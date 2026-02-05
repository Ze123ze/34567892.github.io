from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .models import ExtractionRequest, PipelineOutput
from .pipeline import MultiAgentKGPipeline

app = FastAPI(title="DeepSea Policy KG Multi-Agent API", version="0.1.0")
pipeline = MultiAgentKGPipeline()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/pipeline/extract", response_model=PipelineOutput)
async def extract(req: ExtractionRequest) -> PipelineOutput:
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text 不能为空")

    return await pipeline.run(doc_id=req.doc_id, title=req.title, text=req.text)
