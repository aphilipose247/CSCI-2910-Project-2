from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Operator
from app.schemas import OperatorCreate, OperatorResponse, OperatorUpdate

router = APIRouter(prefix="/operators", tags=["operators"])

NOT_FOUND_DETAIL = "Operator not found"
CONFLICT_DETAIL = "An operator with that name exists"

# These only add the errors to the /docs page. They don't raise anything.
NOT_FOUND: dict[int | str, dict[str, Any]] = {404: {"description": NOT_FOUND_DETAIL}}
CONFLICT: dict[int | str, dict[str, Any]] = {409: {"description": CONFLICT_DETAIL}}

# this function helps with error handling to ensure if an operator doesn't exist, then throw the exception
def get_operator_or_404(operator_id: int, db: Session) -> Operator:
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if operator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_DETAIL
        )
    return operator


def check_for_duplicate(
    operator_name : str, real_name : str, db: Session, ignore_id: int | None = None
) -> None:
    """Raise a 409 if another operator already has this operator name and real name."""
    query = db.query(Operator).filter(
        func.lower(Operator.operator_name) == operator_name.lower(), 
        func.lower(Operator.real_name) == real_name.lower(),
    )
    if ignore_id is not None:
        query = query.filter(Operator.id != ignore_id)
    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=CONFLICT_DETAIL
        )


#------------------------------------------ CRRUD OPERATIONS ------------------------------------

# Fetching all of the operators in the DB (READ ALL)

@router.get("/", response_model=list[OperatorResponse])
def read_operators(
    skip: int = Query(0, ge=0, description="Number of operators to skip"),
    limit: int = Query(
        10, ge=0, le=100, description="Maximum number of records to return (0-100)"
    ),
    faction: str | None = Query(
        None,
        description="Only return operators whose faction contains this text (not case-sensitive)",
    ),
    db: Session = Depends(get_db),
):

    # returns a list of operators which is ordered by ID
    query = db.query(Operator)
    if faction:
        query = query.filter(Operator.faction.ilike(f"%{faction}%"))
    return query.order_by(Operator.id).offset(skip).limit(limit).all()


# Fetch an operator based on their ID (READ), with error handling as well to ensure the operator you look for exists, otherwise throw an error

@router.get("/{operator_id}", response_model=OperatorResponse, responses=NOT_FOUND)
def read_operator(operator_id: int, db: Session = Depends(get_db)):
    """Return one operator by its ID. Returns 404 if no operator has that ID."""
    return get_operator_or_404(operator_id, db)

# Create an operator (CREATE)
@router.post(
    "/",
    response_model=OperatorResponse,
    status_code=status.HTTP_201_CREATED, 
    responses=CONFLICT,
)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    """
    Create a new operator and return it with its new ID.

    Returns 409 if an operator with the same name and real name already exists
    (not case-sensitive).
    """
    check_for_duplicate(operator.operator_name, operator.real_name, db)
    db_operator = Operator(**operator.model_dump())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


# Update a certain Operator (UPDATE)

@router.put(
    "/{operator_id}", response_model=OperatorResponse, responses={**NOT_FOUND, **CONFLICT}
)
def update_operator(
    operator_id: int, operator: OperatorUpdate, db: Session = Depends(get_db)
):
    """
    Replace every field of an existing operator.

    Returns 404 if no operator has that ID, and 409 if the new operator name and real name
    match a *different* operator.
    """
    db_operator = get_operator_or_404(operator_id, db)
    check_for_duplicate(operator.operator_name, operator.real_name, db, ignore_id=operator_id)
    for field, value in operator.model_dump().items():
        setattr(db_operator, field, value)
    db.commit()
    db.refresh(db_operator)
    return db_operator


# Deleting a certain operator by ID (DELETE)

@router.delete(
    "/{operator_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND
)
def delete_operator(operator_id: int, db: Session = Depends(get_db)):
    """Delete an operator. Returns 204 with no body, or 404 if no operator has that ID."""
    db_operator = get_operator_or_404(operator_id, db)
    db.delete(db_operator)
    db.commit()
