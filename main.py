from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Base, Ticket
from ai_engine import analyze_ticket

app = FastAPI()

Base.metadata.create_all(bind=engine)

# ----------- INPUT MODEL -----------
class TicketInput(BaseModel):
    description: str

# ----------- HOME ROUTE -----------
@app.get("/")
def home():
    return {"message": "AI Ticket System Running 🚀"}

# ----------- SAMPLE EMPLOYEES -----------
def get_employees():
    return [
        {"name": "Rahul", "department": "IT", "skill": "Access", "availability": "Available", "ticket_load": 2},
        {"name": "Priya", "department": "IT", "skill": "Bug", "availability": "Available", "ticket_load": 1},
        {"name": "Amit", "department": "Finance", "skill": "Billing", "availability": "Busy", "ticket_load": 3},
    ]

# ----------- ASSIGN LOGIC -----------
def assign_employee(department, category):
    employees = get_employees()

    suitable = [
        e for e in employees
        if e["department"] == department
        and e["availability"] == "Available"
    ]

    if not suitable:
        return "No available employee"

    best = min(suitable, key=lambda x: x["ticket_load"])
    return best["name"]

# ----------- CREATE TICKET -----------
@app.post("/ticket")
def create_ticket(ticket: TicketInput):
    db = SessionLocal()

    ai_result = analyze_ticket(ticket.description)

    assigned_employee = None

    if ai_result["resolution"] != "Auto-resolve":
        assigned_employee = assign_employee(
            ai_result["department"],
            ai_result["category"]
        )

    new_ticket = Ticket(
        description=ticket.description,
        category=ai_result["category"],
        severity=ai_result["severity"],
        status="New",
        department=ai_result["department"]
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    if ai_result["resolution"] == "Auto-resolve":
        response_message = "Please reset your password using the 'Forgot Password' option."
    else:
        response_message = f"Assigned to {assigned_employee}"

    return {
        "ticket_id": new_ticket.id,
        "ai_analysis": ai_result,
        "assigned_to": assigned_employee,
        "response": response_message
    }

# ----------- 🔥 LIFECYCLE API -----------
@app.put("/ticket/{ticket_id}/status")
def update_ticket_status(ticket_id: int, new_status: str):
    db = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    valid_status = ["New", "Assigned", "In Progress", "Pending", "Resolved", "Closed"]

    if new_status not in valid_status:
        return {"error": "Invalid status"}

    ticket.status = new_status
    db.commit()

    return {
        "message": f"Ticket {ticket_id} updated to {new_status}"
    }

# ----------- 📊 ANALYTICS DASHBOARD (FINAL STEP) -----------
@app.get("/analytics")
def get_analytics():
    db = SessionLocal()

    total = db.query(Ticket).count()
    resolved = db.query(Ticket).filter(Ticket.status == "Resolved").count()
    pending = db.query(Ticket).filter(Ticket.status != "Resolved").count()

    return {
        "total_tickets": total,
        "resolved_tickets": resolved,
        "pending_tickets": pending
    }