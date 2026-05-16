from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from apps.database import get_db

from .pagination import get_pagination_params, paginate

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ReadSchemaType = TypeVar("ReadSchemaType")


class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None
    errors: Optional[List[Dict[str, str]]] = None
    meta: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    @classmethod
    def success_response(
        cls,
        data: Any = None,
        message: str = "Operation successful",
        meta: Optional[Dict[str, Any]] = None,
    ) -> "StandardResponse":
        return cls(
            success=True,
            data=data,
            message=message,
            # meta=meta,
            **({} if meta is None else {"meta": meta}),
        )

    @classmethod
    def error_response(
        cls,
        message: str = "Error occurred",
        error: Optional[str] = None,
        errors: Optional[List[Dict[str, str]]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "StandardResponse":
        return cls(
            success=False,
            message=message,
            error=error,
            errors=errors,
            # meta=meta,
            **({} if meta is None else {"meta": meta}),
        )
