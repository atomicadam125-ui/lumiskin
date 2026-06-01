from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SAUUID
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(120))
    auth_provider: Mapped[str] = mapped_column(String(40), default="password", nullable=False)
    apple_sub: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
    questionnaires = relationship(
        "Questionnaire", back_populates="user", cascade="all, delete-orphan"
    )
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship(
        "Recommendation", back_populates="user", cascade="all, delete-orphan"
    )
