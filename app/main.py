from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database.mongodb import MongoDB
from app.services.document_processor import DocumentProcessor
from app.services.llm_service import LLMService
from typing import List, Dict

app = FastAPI()
document_processor = DocumentProcessor()
llm_service = LLMService()

class DocumentQuery(BaseModel):
    document: str

class RecommendationResponse(BaseModel):
    uuid: str
    recommend_reason: str

@app.on_event("startup")
async def startup_event():
    await MongoDB.connect_to_mongodb()
    documents = await MongoDB.get_documents()
    document_processor.process_documents(documents)

@app.on_event("shutdown")
async def shutdown_event():
    await MongoDB.close_mongodb_connection()

@app.post("/recommend", response_model=List[RecommendationResponse])
async def get_recommendations(query: DocumentQuery):
    try:
        # Generate summary for the query document
        summary = await llm_service.generate_summary(query.document)
        
        # Query similar documents
        similar_docs = await document_processor.query_similar_documents(summary)
        
        recommendations = []
        for doc, score in similar_docs[:5]:
            recommend_reason = await llm_service.generate_recommendation_reason(
                query.document,
                doc.page_content
            )
            
            recommendations.append(RecommendationResponse(
                uuid=doc.metadata['uuid'],
                recommend_reason=recommend_reason
            ))
        
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 