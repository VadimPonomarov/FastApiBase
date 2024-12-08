import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class CrtUpdDatetimeMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )
    updated_at = Mapped[datetime.datetime] = mapped_column(
        server_default=text(
            "TIMEZONE('utc', CURRENT_TIMESTAMP)", onupdate=datetime.datetime.now
        )
    )
