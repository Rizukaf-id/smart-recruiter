from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateReview(BaseModel):
    '''Representasi Data Hasil Review kandidat'''
    candidate_name: str = Field(..., description='Nama kandidat')
    score: int = Field(..., description='Skor kecocokan 0-100')
    summary: str = Field(..., description='Ringkasan hasil review')
    pros: List[str] = Field(default_factory=list, description='Kelebihan')
    cons: List[str] = Field(default_factory=list, description='Kekurangan')
    filename: str = Field(..., description='Nama file asal')