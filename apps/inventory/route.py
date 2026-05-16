from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.database import get_db
from apps.dealers.models.brand import Brand
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse

from .models import Inventory
from .schemas import InventoryCreate, InventoryList, InventoryRetrieve, InventoryUpdate

router = APIRouter()


@router.post(
    "/create",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
):
    """Create a new inventory record"""
    brand = db.query(Brand).filter(Brand.id == inventory.brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid brand_id provided",
        )
    db_inventory = Inventory(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return StandardResponse.success_response(
        data=InventoryRetrieve.model_validate(db_inventory),
        message="Inventory created successfully",
    )


@router.get("/list", response_model=StandardResponse)
def list_inventory(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """List all inventory records with pagination"""
    result = paginate(
        query=db.query(Inventory),
        # page=page,
        # page_size=page_size,
        pagination=pagination,
        schema=InventoryList,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Inventory fetched successfully",
        meta=result.meta,
    )


@router.get("/retrieve/{inventory_id}", response_model=StandardResponse)
def retrieve_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific inventory record by ID"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=StandardResponse.error_response(
                message="Inventory record not found"
            ).model_dump(),
        )

    return StandardResponse.success_response(
        data=InventoryRetrieve.model_validate(inventory),
        message="Inventory retrieved successfully",
    )


@router.patch("/update/{inventory_id}", response_model=StandardResponse)
def patch_inventory(
    inventory_id: int, inventory_data: InventoryUpdate, db: Session = Depends(get_db)
):
    """Partially update an inventory record"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=StandardResponse.error_response(
                message="Inventory record not found"
            ).model_dump(),
        )

    # Only update fields provided
    for field, value in inventory_data.model_dump(exclude_unset=True).items():
        setattr(inventory, field, value)

    db.commit()
    db.refresh(inventory)

    return StandardResponse.success_response(
        data=InventoryRetrieve.model_validate(inventory),
        message="Inventory updated successfully",
    )


@router.delete("/delete/{inventory_id}", response_model=StandardResponse)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """Delete an inventory record"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=StandardResponse.error_response(
                message="Inventory record not found"
            ).model_dump(),
        )

    db.delete(inventory)
    db.commit()

    return StandardResponse.success_response(
        data=None,
        message="Inventory deleted successfully",
    )
