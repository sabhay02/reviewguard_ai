from fastapi import APIRouter, HTTPException
from app.database.history import get_reviews
import sqlite3
import os
from app.graphs.workflow import review_graph

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_stats():
    reviews = get_reviews()
    
    total_reviews = len(reviews)
    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "average_score": 0,
            "total_findings": 0,
            "critical_risk_count": 0
        }
        
    avg_score = sum(r["score"] for r in reviews) / total_reviews
    total_findings = sum(r["findings"] for r in reviews)
    critical_count = sum(1 for r in reviews if r["risk"] == "CRITICAL")
    
    return {
        "total_reviews": total_reviews,
        "average_score": round(avg_score, 1),
        "total_findings": total_findings,
        "critical_risk_count": critical_count
    }

@router.get("/reviews")
def list_reviews():
    # Convert sqlite3.Row objects to dicts
    reviews = get_reviews()
    return [dict(r) for r in reviews]

@router.get("/pending")
def list_pending():
    conn = sqlite3.connect('data/reviewguard.db')
    try:
        threads = [row[0] for row in conn.execute('SELECT DISTINCT thread_id FROM checkpoints').fetchall()]
    except Exception:
        threads = []
    finally:
        conn.close()

    pending_reviews = []
    for tid in threads:
        try:
            state = review_graph.get_state({"configurable": {"thread_id": tid}})
            if state and state.next and 'human_review' in state.next:
                val = state.values
                if val.get("source") != "webhook":
                    continue
                pending_reviews.append({
                    "review_id": tid,
                    "repo_name": val.get("repo_name", "Unknown"),
                    "owner": val.get("owner", ""),
                    "pr_number": val.get("pr_number"),
                    "score": val.get("score"),
                    "grade": val.get("grade"),
                    "risk": val.get("risk"),
                    "findings": len(val.get("findings", [])),
                    "summary": val.get("summary", "")
                })
        except Exception as e:
            print(f"Error reading state for {tid}: {e}")
            
    return pending_reviews

@router.get("/report/{review_id}")
def get_report(review_id: str):
    report_path = os.path.join("reports", f"{review_id}.md")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        state = review_graph.get_state({"configurable": {"thread_id": review_id}})
        stats = state.values.get("stats", {}) if state and state.values else {}
    except Exception as e:
        print(f"Error fetching state for report {review_id}: {e}")
        stats = {}
        
    return {"content": content, "stats": stats}
