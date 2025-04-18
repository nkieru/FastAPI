from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[uniq]
    password: Mapped[str]

    is_reader: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def to_dict(self):
        return {
            "id": self.id,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
