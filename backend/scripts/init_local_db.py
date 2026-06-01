import sys
from pathlib import Path

from sqlalchemy import create_engine

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import models  # noqa: F401
from core.config import settings
from db.base import Base


def main() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    engine = create_engine(settings.database_url, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    print("SQLite database is ready.")


if __name__ == "__main__":
    main()
