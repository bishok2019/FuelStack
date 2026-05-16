from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse

from ..models import Hub
from ..schemas import HubBase

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_hub(hub: HubBase, db: Session = Depends(get_db)):
    """Create a new Hub record"""
    hub_query = Hub(**hub.model_dump())
    db.add(hub_query)
    db.commit()
    db.refresh(hub_query)

    return StandardResponse.success_response(
        data=HubBase.model_validate(hub_query),
        message="Hub created successfully",
    )


@router.get("/list", response_model=StandardResponse)
def list_hub(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """List all hub records with pagination"""
    result = paginate(
        query=db.query(Hub),
        # page=page,
        # page_size=page_size,
        pagination=pagination,
        schema=HubBase,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Hub fetched successfully",
        meta=result.meta,
    )
