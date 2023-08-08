from database import Base
from sqlalchemy import Column, String
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class ModelEmployee(Base):
    """
    Represents an Employee in the database.

    This model defines the structure of the 'employee' table in the database,
    including the id, name, and department fields.

    Attributes:
        id (GUID): The unique identifier for the employee, automatically generated.
        name (str): The name of the employee.
        department (str): The department to which the employee belongs.

    Note:
        The 'id' field is a GUID (Globally Unique Identifier) column with a default
        value generated using GUID_DEFAULT_SQLITE for SQLite databases.

    """
    __tablename__ = 'employee'
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
