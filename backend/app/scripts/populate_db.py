from sqlalchemy.orm import Session

from app.database import engine
from app.models import Operator, Base

# Retrieved this data from mw4.gg
# https://mw4.gg/operators/ 
# this is the link 

operators_data = [
    {
        "operator_name": "Mona Lisa",
        "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },  
    {
        "operator_name": "Mona Lisa",
        "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },
    {
        "operator_name": "Mona Lisa",
        "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },
    {
        "operator_name": "Mona Lisa",
         "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },
    {
        "operator_name": "Mona Lisa",
        "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },
    {
        "operator_name": "Mona Lisa",
        "real_name": "Leonardo da Vinci",
        "faction": 1503,
        "nationality": "Oil on poplar panel",
        "language": "Louvre",
        "is_available": "",
        "image_of_operator" : ""
    },
    
    

    
    
    
]


def populate():
    """Create the table and seed it, but only if it's empty (so your changes survive a restart)."""
    Base.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        if session.query(Artwork).count() > 0:
            return
        for artwork in artworks_data:
            session.add(Artwork(**artwork))
        session.commit()


def reset():
    """Wipe the table and re-seed it. Run with `python -m app.scripts.populate_db`"""
    Base.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        session.query(Artwork).delete()
        session.commit()
    populate()


if __name__ == "__main__":
    reset()
