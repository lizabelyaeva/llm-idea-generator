from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.entities import Idea
from app.schemas.idea import AnalyzeRequest, GenerateRequest, GenerateResponse, IdeaResponse, ScoreRequest
from app.services.orchestrator import IdeaOrchestrator

router = APIRouter()


def to_idea_response(idea: Idea) -> IdeaResponse:
    analysis = None
    if idea.analysis:
        analysis = {
            "white": idea.analysis.white,
            "red": idea.analysis.red,
            "black": idea.analysis.black,
            "yellow": idea.analysis.yellow,
            "green": idea.analysis.green,
            "blue": idea.analysis.blue,
        }
    return IdeaResponse(
        id=idea.id,
        title=idea.title,
        description=idea.description,
        rank=idea.rank,
        analysis=analysis,
        score=idea.score,
        session_id=idea.session_id,
        session_topic=idea.session.topic if idea.session else "Без темы",
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_ideas(request: GenerateRequest, db: Session = Depends(get_db)):
    orchestrator = IdeaOrchestrator(db)
    session_id, ideas = await orchestrator.run_full_pipeline(request)
    return GenerateResponse(session_id=session_id, ideas=[to_idea_response(idea) for idea in ideas])


@router.get("/ideas", response_model=list[IdeaResponse])
def get_ideas(session_id: int | None = None, db: Session = Depends(get_db)):
    query = (
        db.query(Idea)
        .options(joinedload(Idea.analysis), joinedload(Idea.session))
        .order_by(Idea.session_id.desc(), Idea.rank.asc().nullslast(), Idea.id.asc())
    )
    if session_id:
        query = query.filter(Idea.session_id == session_id)
    ideas = query.all()
    return [to_idea_response(idea) for idea in ideas]


@router.post("/analyze", response_model=IdeaResponse)
async def analyze_idea(request: AnalyzeRequest, db: Session = Depends(get_db)):
    idea = (
        db.query(Idea)
        .options(joinedload(Idea.session), joinedload(Idea.analysis))
        .filter(Idea.id == request.idea_id)
        .one_or_none()
    )
    if idea is None:
        raise HTTPException(status_code=404, detail="Идея не найдена")
    orchestrator = IdeaOrchestrator(db)
    await orchestrator.analyze_idea(idea.session.topic, idea)
    db.commit()
    db.refresh(idea)
    return to_idea_response(idea)


@router.post("/score", response_model=IdeaResponse)
async def score_idea(request: ScoreRequest, db: Session = Depends(get_db)):
    idea = (
        db.query(Idea)
        .options(joinedload(Idea.session), joinedload(Idea.analysis))
        .filter(Idea.id == request.idea_id)
        .one_or_none()
    )
    if idea is None:
        raise HTTPException(status_code=404, detail="Идея не найдена")
    orchestrator = IdeaOrchestrator(db)
    await orchestrator.score_idea(idea.session.topic, idea)
    db.commit()
    db.refresh(idea)
    return to_idea_response(idea)


@router.delete("/ideas/{idea_id}")
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    idea = db.query(Idea).options(joinedload(Idea.session)).filter(Idea.id == idea_id).one_or_none()
    if idea is None:
        raise HTTPException(status_code=404, detail="Идея не найдена")
    db.delete(idea)
    db.commit()
    return {"status": "deleted", "idea_id": idea_id}
