"""Declaring base model classes for sqlalchemy models."""
import re
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class BaseDBModel(DeclarativeBase):
    """Class defining common db model components."""
    # Auto-generate created_at timestamp for all models
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # refresh server defaults with asyncio 
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    # if not declared generate tablename automatically based on class name 
    # insert _ infront of class capitalized letters and bring to lower case
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"(\w)([A-Z])", r"\1_\2", cls.__name__).lower()