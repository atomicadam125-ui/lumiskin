from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy import UUID as SAUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    photo_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("photos.id", ondelete="CASCADE")
    )
    photo_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    questionnaire_id: Mapped[UUID | None] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("questionnaires.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(30), default="completed", nullable=False)
    scores: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    skin_profile: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    model_versions: Mapped[dict[str, str]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="analyses")
    photo = relationship("Photo", back_populates="analyses")
    questionnaire = relationship("Questionnaire", back_populates="analyses")
    recommendations = relationship(
        "Recommendation", back_populates="analysis", cascade="all, delete-orphan"
    )
