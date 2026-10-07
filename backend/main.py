from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
import os

from backend.database import create_tables, get_connection


# Project root
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from Ai.assistant import get_response


# =========================
# FASTAPI APP
# =========================
from fastapi.middleware.cors import CORSMiddleware 
app = FastAPI( 
    title="Nuvexa AI", 
    description="AI Business Assistant API", 
    version="1.0.0" 
) 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=False, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 


# =========================
# CREATE DATABASE TABLES
# =========================

create_tables()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# CHAT REQUEST
# =========================

class ChatRequest(BaseModel):
    message: str


# =========================
# BUSINESS INFORMATION
# =========================

class BusinessInfo(BaseModel):
    businessName: str
    phone: str
    email: str
    location: str
    courses: str
    fees: str
    timings: str
    additional: str


# =========================
# LEAD INFORMATION
# =========================

class LeadInfo(BaseModel):
    name: str
    phone: str
    course: str
    enquiry: str


class AppointmentInfo(BaseModel):
    name: str
    phone: str
    course: str
    appointmentDate: str
    appointmentTime: str   



# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Welcome to Nuvexa AI 🚀",
        "status": "Backend is running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================
# CHAT API
# =========================

@app.post("/chat")
def chat(request: ChatRequest):

    response = get_response(request.message)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations
        (
            user_message,
            ai_response
        )
        VALUES (?, ?)
    """, (
        request.message,
        response
    ))

    connection.commit()
    connection.close()

    return {
        "user_message": request.message,
        "ai_response": response
    }
@app.get("/conversations/count")
def get_conversation_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conversations
    """)

    result = cursor.fetchone()

    connection.close()

    return {
        "total_conversations": result["total"]
    }


# =========================
# SAVE BUSINESS INFORMATION
# =========================

@app.post("/business")
def save_business(info: BusinessInfo):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO business_info
        (
            business_name,
            phone,
            email,
            location,
            courses,
            fees,
            timings,
            additional
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        info.businessName,
        info.phone,
        info.email,
        info.location,
        info.courses,
        info.fees,
        info.timings,
        info.additional
    ))

    connection.commit()
    connection.close()

    return {
        "message": "Business information saved successfully!"
    }


# =========================
# GET BUSINESS INFORMATION
# =========================

@app.get("/business")
def get_business():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM business_info
        ORDER BY id DESC
        LIMIT 1
    """)

    business = cursor.fetchone()

    connection.close()

    if business is None:

        return {
            "message": "No business information found."
        }

    return {

        "id": business["id"],

        "businessName":
            business["business_name"],

        "phone":
            business["phone"],

        "email":
            business["email"],

        "location":
            business["location"],

        "courses":
            business["courses"],

        "fees":
            business["fees"],

        "timings":
            business["timings"],

        "additional":
            business["additional"]
    }


# =========================
# SAVE LEAD
# =========================

@app.post("/leads")
def save_lead(lead: LeadInfo):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leads
        (
            name,
            phone,
            course,
            enquiry
        )
        VALUES (?, ?, ?, ?)
    """, (
        lead.name,
        lead.phone,
        lead.course,
        lead.enquiry
    ))

    connection.commit()
    connection.close()

    return {
        "message": "Lead saved successfully!",
        "lead": {
            "name": lead.name,
            "phone": lead.phone,
            "course": lead.course
        }
    }
@app.put("/leads/{lead_id}/status")
def update_lead_status(lead_id: int, status: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE leads
        SET status = ?
        WHERE id = ?
    """, (status, lead_id))

    connection.commit()
    connection.close()

    return {
        "message": "Lead status updated successfully!",
        "lead_id": lead_id,
        "status": status
    }
@app.post("/appointments")
def save_appointment(appointment: AppointmentInfo):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (
            name,
            phone,
            course,
            appointment_date,
            appointment_time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        appointment.name,
        appointment.phone,
        appointment.course,
        appointment.appointmentDate,
        appointment.appointmentTime
    ))

    connection.commit()
    connection.close()

    return {
        "message": "Appointment booked successfully!",
        "appointment": {
            "name": appointment.name,
            "phone": appointment.phone,
            "course": appointment.course,
            "appointmentDate": appointment.appointmentDate,
            "appointmentTime": appointment.appointmentTime
        }
    }


@app.get("/appointments")
def get_appointments():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """)

    appointments = cursor.fetchall()
    connection.close()

    return {
        "total_appointments": len(appointments),
        "appointments": [
            {
                "id": appointment["id"],
                "name": appointment["name"],
                "phone": appointment["phone"],
                "course": appointment["course"],
                "appointmentDate": appointment["appointment_date"],
                "appointmentTime": appointment["appointment_time"],
                "status": appointment["status"]
            }
            for appointment in appointments
        ]
    }

@app.put("/appointments/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    status: str
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE appointments
        SET status = ?
        WHERE id = ?
    """, (
        status,
        appointment_id
    ))

    connection.commit()
    connection.close()

    return {
        "message": "Appointment status updated successfully!",
        "appointment_id": appointment_id,
        "status": status
    }
# =========================
# GET ALL LEADS
# =========================

@app.get("/leads")
def get_leads():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM leads
        ORDER BY id DESC
    """)

    leads = cursor.fetchall()

    connection.close()

    return {
        "total_leads": len(leads),
        "leads": [
            {
                "id": lead["id"],
                "name": lead["name"],
                "phone": lead["phone"],
                "course": lead["course"],
                "enquiry": lead["enquiry"],
                "status": lead["status"]
            }
            for lead in leads
        ]
    }






