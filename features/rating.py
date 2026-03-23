# rating.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/ratings", tags=["ratings"])

# Basit veri tabanı (geçici)
ratings_db = []
next_id = 1


class RatingCreate(BaseModel):
    user_id: int
    hotel_id: int
    booking_id: int  # Tamamlanmış rezervasyon ID
    score: int  # 1-5 arası
    comment: str = None


class RatingResponse(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    booking_id: int
    score: int
    comment: str


@router.post("/", response_model=RatingResponse)
async def create_rating(rating: RatingCreate):
    global next_id

    # Puan kontrolü (1-5 arası)
    if rating.score < 1 or rating.score > 5:
        raise HTTPException(status_code=400, detail="Puan 1-5 arasında olmalı")

    # Rating oluştur
    new_rating = {
        "id": next_id,
        "user_id": rating.user_id,
        "hotel_id": rating.hotel_id,
        "booking_id": rating.booking_id,
        "score": rating.score,
        "comment": rating.comment
    }

    ratings_db.append(new_rating)
    next_id += 1

    return new_rating


@router.get("/hotel/{hotel_id}")
async def get_hotel_ratings(hotel_id: int):
    # Otelin tüm ratinglerini getir
    hotel_ratings = [r for r in ratings_db if r["hotel_id"] == hotel_id]

    if not hotel_ratings:
        return {"message": "Henüz rating yok", "ratings": [], "average_score": 0}

    # Ortalama puan hesapla
    average = sum(r["score"] for r in hotel_ratings) / len(hotel_ratings)

    return {
        "hotel_id": hotel_id,
        "ratings": hotel_ratings,
        "average_score": round(average, 1),
        "total_ratings": len(hotel_ratings)
    }