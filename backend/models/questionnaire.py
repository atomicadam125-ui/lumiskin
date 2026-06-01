from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, func
from sqlalchemy import UUID as SAUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    skin_type: Mapped[str] = mapped_column(String(40), nullable=False)
    sensitivity_level: Mapped[int] = mapped_column(Integer, nullable=False)
    acne_frequency: Mapped[str] = mapped_column(String(40), nullable=False)
    current_products: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    sun_exposure_level: Mapped[int] = mapped_column(Integer, nullable=False)
    sleep_quality: Mapped[int] = mapped_column(Integer, nullable=False)
    stress_level: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="questionnaires")
    analyses = relationship("Analysis", back_populates="questionnaire")
