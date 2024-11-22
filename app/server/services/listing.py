from typing import Any, Optional

from fastapi import HTTPException, status

import app.server.database.core_data as core_service
from app.server.models.listing import ListingCreateDB, ListingCreateRequest, ListingUpdateDB, ListingUpdateRequest
from app.server.static import localization
from app.server.static.collections import Collections
from app.server.static.enums import ListingStatus, Role


async def create_listing(params: ListingCreateRequest, user_data: dict[str, any]) -> dict[str, Any]:
    """Create a listing for an item

    Args:
        params (ListingCreateRequest): Listing Details
        user_data (dict[str, any]): User token data

    Raises:
        HTTPException: Item category not found

    Returns:
        dict[str, Any]: Success message.
    """
    listing_data = params.dict()

    existing_item = await core_service.read_one(Collections.ITEMS, data_filter={'_id': params.item_id})
    if not existing_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, localization.EXCEPTION_ITEM_NOT_FOUND)

    listing_data['item_name'] = 'Item'  # existing_item['item_name']
    listing_data.pop('item_id')
    listing_data['status'] = ListingStatus.NEW
    listing_data['seller_id'] = user_data.get('user_id')

    listing_data = ListingCreateDB(**listing_data).dict(exclude_none=True)
    await core_service.create_one(Collections.LISTINGS, data=listing_data)

    return {'message': 'Listing created successfully'}


async def get_all_listings(item_id: Optional[str], page: int, page_size: int) -> list[dict[str, Any]]:
    """
    Get a paginated list of Listings.

    Args:
        item_id (Optional[str]): Optional item id to filter the listings.
        page (int): The page number to retrieve.
        page_size (int): The number of items to retrieve per page.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the Listings.

    Raises:
        None
    """
    data_filter = {}

    if item_id:
        data_filter['item_id'] = item_id

    return await core_service.read_many(collection_name=Collections.LISTINGS, data_filter=data_filter, page=page, page_size=page_size)


async def get_listing_by_id(listing_id: str) -> dict[str, Any]:
    """Get a listing by id

    Args:
        listing_id (str): Listing id
        user_data (dict[str, any]): User token data

    Raises:
        HTTPException: Listing not found

    Returns:
        dict[str, any]: Listing data
    """
    return await core_service.read_one(collection_name=Collections.LISTINGS, data_filter={'_id': listing_id, 'is_deleted': False})


async def get_listings_by_user(user_data: dict[str, Any], page: int, page_size: int) -> list[dict[str, Any]]:
    """Get all listing of a user

    Args:
        user_data (dict[str, Any]): User token data
        page (int): The page number to retrieve.
        page_size (int): The number of items to retrieve per page.

    Returns:
        dict[str, Any]: _description_
    """
    return await core_service.read_many(collection_name=Collections.LISTINGS, data_filter={'seller_id': user_data['user_id'], 'is_deleted': False}, page=page, page_size=page_size)


async def update_listing(listing_id: str, params: ListingUpdateRequest, user_data: dict[str, Any]) -> dict[str, Any]:
    """Update details of a listing

    Args:
        listing_id (str): Listing id
        params (ListingUpdateRequest): Request body containing listing update details
        user_data (dict[str, Any]): Token data of user

    Raises:
        HTTPException: Listing not found
        HTTPException: Listing marked as sold

    Returns:
        dict[str, Any]: Success message
    """
    listing_data = await core_service.read_one(collection_name=Collections.LISTINGS, data_filter={'_id': listing_id, 'seller_id': user_data['user_id'], 'is_deleted': False})
    if not listing_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, localization.EXCEPTION_LISTING_NOT_FOUND)

    if listing_data['status'] == ListingStatus.SOLD:
        raise HTTPException(status.HTTP_403_FORBIDDEN, localization.EXCEPTION_LISTING_MARKED_SOLD)

    params = ListingUpdateDB(**params.dict(exclude_none=True))

    await core_service.update_one(Collections.LISTINGS, data_filter={'_id': listing_data.get('_id')}, update={'$set': params.dict(exclude_none=True)}, upsert=True)

    return {'message': 'Listing updated successfully'}


async def delete_listing(listing_id: str, user_data: dict[str, Any]) -> dict[str, Any]:
    """Soft delete a listing

    Args:
        listing_id (str): Listing id
        user_data (dict[str, Any]): Token data

    Raises:
        HTTPException: Listing not found
        HTTPException: Listing marked as sold

    Returns:
        dict[str, Any]: Success message
    """
    if user_data['user_type'] == Role.STUDENT:
        listing_data = await core_service.read_one(collection_name=Collections.LISTINGS, data_filter={'_id': listing_id, 'seller_id': user_data['user_id'], 'is_deleted': False})
    else:
        listing_data = await core_service.read_one(collection_name=Collections.LISTINGS, data_filter={'_id': listing_id, 'is_deleted': False})

    if not listing_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, localization.EXCEPTION_LISTING_NOT_FOUND)

    if listing_data['status'] == ListingStatus.SOLD:
        raise HTTPException(status.HTTP_403_FORBIDDEN, localization.EXCEPTION_LISTING_MARKED_SOLD)

    params = {'is_deleted': True}

    await core_service.update_one(Collections.LISTINGS, data_filter={'_id': listing_id}, update={'$set': params}, upsert=False)

    return {'message': 'Listing deleted successfully'}
