from sqlalchemy.orm import Session

from app.database import engine
from app.models import Operator, Base

# Retrieved this data from mw4.gg
# https://mw4.gg/operators/ 
# this is the link 

operators_data = [
    {
        "operator_name": "Price",
        "real_name": "John Price",
        "faction": "South Korean Quick Reaction Force",
        "nationality": "United Kingdom",
        "language": "English",
        "is_available": True,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-price/bioImage.webp?v=1792430497236"
    },  
    {
        "operator_name": "Ghost",
        "real_name": "Simon Riley",
        "faction": "South Korean Quick Reaction Force",
        "nationality": "United Kingdom",
        "language": "English",
        "is_available": True,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-ghost/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Blix",
        "real_name": "Unknown",
        "faction": "South Korean Quick Reaction Force",
        "nationality": "South Korea",
        "language": "Korean",
        "is_available": True,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-blix/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Hector",
         "real_name": "Hector Torres",
        "faction": "Valeria's Strike Cell",
        "nationality": "United States",
        "language": "English",
        "is_available": False,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-hector/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Valen",
        "real_name": "Unknown",
        "faction": "Valeria's Strike Cell",
        "nationality": "Mexico",
        "language": "Spanish",
        "is_available": False,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-yara/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Kal",
        "real_name": "Kwon Hae-Soo",
        "faction": "South Korean Quick Reaction Force",
        "nationality": "South Korea",
        "language": "Korean",
        "is_available": False,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-kal/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Luca",
        "real_name": "Luca Marchand",
        "faction": "Valeria's Strike Cell",
        "nationality": "France",
        "language": "French",
        "is_available": False,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-luca/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Ohji",
        "real_name": "Unknown",
        "faction": "Valeria's Strike Cell",
        "nationality": "Japan",
        "language": "Japanese",
        "is_available": False,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-ohji/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Dallas",
        "real_name": "Unknown",
        "faction": "Shadow Company",
        "nationality": "United States",
        "language": "English",
        "is_available": True,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-dallas/bioImage.webp?v=1792430497236"
    },
    {
        "operator_name": "Dunn",
        "real_name": "Joseph Dunn",
        "faction": "JSOF",
        "nationality": "United States",
        "language": "English",
        "is_available": True,
        "image_of_operator" : "https://api.mw4.gg/api/v2/media/v2/operator/op-dunn/bioImage.webp?v=1792430497236"
    }
]


def populate():
    """Create the table and seed it, but only if it's empty (so your changes survive a restart)."""
    Base.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        if session.query(Operator).count() > 0:
            return
        for operator in operators_data:
            session.add(Operator(**operator))
        session.commit()


def reset():
    """Wipe the table and re-seed it. Run with `python -m app.scripts.populate_db`"""
    Base.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        session.query(Operator).delete()
        session.commit()
    populate()


if __name__ == "__main__":
    reset()
