from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import Column, DateTime, func

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column("id", type_=int, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
