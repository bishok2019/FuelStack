from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse

from ..models import Dealer
from ..schemas import DealerBase

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_dealer(dealer: DealerBase, db: Session = Depends(get_db)):
    """Create a new dealer record"""
    dealer_query = Dealer(**dealer.model_dump())
    db.add(dealer_query)
    db.commit()
    db.refresh(dealer_query)

    return StandardResponse.success_response(
        data=DealerBase.model_validate(dealer_query),
        message="Dealer created successfully",
    )


@router.get("/list", response_model=StandardResponse)
def list_dealer(
    # page: int = 1,
    # page_size: int = 10,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """List all Dealer records with pagination"""
    result = paginate(
        query=db.query(Dealer),
        # page=page,
        # page_size=page_size,
        pagination=pagination,
        schema=DealerBase,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Dealer fetched successfully",
        meta=result.meta,
    )
