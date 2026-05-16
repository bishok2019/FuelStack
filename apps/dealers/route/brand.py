from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse

from ..models import Brand
from ..schemas import BrandBase

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_brand(brand: BrandBase, db: Session = Depends(get_db)):
    """Create a new brand record"""
    brand_query = Brand(**brand.model_dump())
    db.add(brand_query)
    db.commit()
    db.refresh(brand_query)

    return StandardResponse.success_response(
        data=BrandBase.model_validate(brand_query),
        message="Brand created successfully",
    )


@router.get("/list", response_model=StandardResponse)
def list_brand(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """List all Brand records with pagination"""
    result = paginate(
        query=db.query(Brand),
        # page=page,
        # page_size=page_size,
        pagination=pagination,
        schema=BrandBase,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Brand fetched successfully",
        meta=result.meta,
    )
