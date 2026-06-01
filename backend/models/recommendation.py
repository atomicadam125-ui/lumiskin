from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, func
from sqlalchemy import UUID as SAUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    analysis_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE")
    )
    routine: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    llm_model: Mapped[str] = mapped_column(String(80), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="recommendations")
    analysis = relationship("Analysis", back_populates="recommendations")
