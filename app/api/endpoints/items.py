from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.config import settings
from app.core.manager import ItemsManager
from fastapi.responses import JSONResponse

router = APIRouter()


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


@router.post("/", response_model=Item)
async def create_item(item: Item):
    # Create instance of ItemsManager
    service = ItemsManager()
    
    # Convert Pydantic item to dict and save it
    item_dict = item.dict()
    service.add_item(item_dict)
    
    # Return the item that was created
    return item


@router.get("/", response_model=List[Item])
async def get_items():
    # Use the manager to get items from the JSON file
    service = ItemsManager()
    return service.items


@router.get(
    "/{item_id}",
    response_model=Item,
    responses={
        200: {
            "description": "Item found",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Sample Item", "description": "This is a sample item."}
                }
            },          
        },
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with ID {item_id} not found"}
                }
            },
        },
        400: {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid item format"}
                }
            },
        }
    },
)
async def get_item(item_id: int):
    # Use the manager to get items from the JSON file
    service = ItemsManager()
    try: 
        # Find items with the matching ID
        matching_items = service.get_item_by_id(item_id)
        
        # Check if we found any items
        # if not matching_items:
        #     raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
        
        # Get the first matching item
        item = matching_items[0]
    
    # Validate that the item has the required fields

        # Validate by creating an Item model from it
        return Item(**item)
    except Exception as e:
        raise e


class ParseRequest(BaseModel):
    count: int


@router.post("/parse")
async def parse_items(request: ParseRequest):
    # Create instance of ItemsManager
    service = ItemsManager()
    
    # Parse items from the JSON file with the given count
    result = await service.parse_items3(request.count)
    
    # Return a success message
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Items parsed successfully with count={request.count}",
            "result": result
        }
    )
    return {"message": f"Items parsed successfully with count={result}"}