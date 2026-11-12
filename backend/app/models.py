from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Operator(Base): #establishes the table that SQLAlchemy can call from
    __tablename__ = "operators"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    operator_name = Column(String, index=True)
    real_name = Column(String, index=True)
    faction = Column(String, index=True)
    nationality = Column(String)
    language = Column(String)
    is_available = Column (Boolean) # This means if they are able to be bought from bundles, instead of from compaigns or missions
    image_of_operator = Column (String)