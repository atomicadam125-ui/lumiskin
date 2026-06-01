from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SAUUID
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    original_filename: Mapped[str | None] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    image_width: Mapped[int | None] = mapped_column(Integer)
    image_height: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="photos")
    analyses = relationship("Analysis", back_populates="photo", cascade="all, delete-orphan")
