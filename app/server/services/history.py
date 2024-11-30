from typing import Any

from fastapi import HTTPException, status

import app.server.database.core_data as core_service
from app.server.static import localization
from app.server.static.collections import Collections
from app.server.static.enums import ListingStatus


async def get_sold_listings(user_data: dict[str, Any], page: int, page_size: int) -> list[dict[str, Any]]:
    """Get a paginated list of Listings that the buyer is interested in.
    Args:
        user_data (dict[str, Any]): User token data
        page (int): The page number to retrieve.
        page_size (int): The number of items to retrieve per page.
    Returns:
        dict[str, Any]: _description_
    """
    return await core_service.read_many(collection_name=Collections.LISTINGS, data_filter={'seller_id': user_data['user_id'], 'status': ListingStatus.SOLD}, page=page, page_size=page_size)


async def get_purchased_listings(user_data: dict[str, Any], page: int, page_size: int) -> list[dict[str, Any]]:
    """Get a paginated list of Listings that the buyer is interested in.
    Args:
        user_data (dict[str, Any]): User token data
        page (int): The page number to retrieve.
        page_size (int): The number of items to retrieve per page.
    Returns:
        dict[str, Any]: _description_
    """
    return await core_service.read_many(collection_name=Collections.LISTINGS, data_filter={'buyer_id': user_data['user_id'], 'status': ListingStatus.SOLD}, page=page, page_size=page_size)


async def get_listing_details(listing_id: str, user_data: dict[str, Any]) -> dict[str, Any]:
    """Get a paginated list of Listings that the buyer is interested in.
    Args:
        user_data (dict[str, Any]): User token data
        page (int): The page number to retrieve.
        page_size (int): The number of items to retrieve per page.
    Returns:
        dict[str, Any]: _description_
    """
    listing_details = await core_service.read_one(collection_name=Collections.LISTINGS, data_filter={'_id': listing_id, 'status': ListingStatus.SOLD})
    if not listing_details:
        raise HTTPException(status.HTTP_404_NOT_FOUND, localization.EXCEPTION_LISTING_NOT_FOUND)
    if user_data['user_id'] != listing_details['seller_id'] and user_data['user_id'] != listing_details['buyer_id']:
        raise HTTPException(status.HTTP_403_FORBIDDEN, localization.EXCEPTION_FORBIDDEN_ACCESS)
    seller_name = await core_service.read_one(collection_name=Collections.USERS, data_filter={'_id': listing_details['seller_id']})
    buyer_name = await core_service.read_one(collection_name=Collections.USERS, data_filter={'_id': listing_details['buyer_id']})
    buyer_comments = await core_service.read_one(collection_name=Collections.TRANSACTIONS, data_filter={'listing_id': listing_id, 'buyer_id': listing_details['buyer_id']})
    if not seller_name or not buyer_name:
        raise HTTPException(status.HTTP_404_NOT_FOUND, localization.EXCEPTION_USER_NOT_FOUND)
    listing_details['seller_name'] = seller_name['first_name'] + ' ' + seller_name['last_name']
    listing_details['buyer_name'] = buyer_name['first_name'] + ' ' + buyer_name['last_name']
    listing_details['buyer_comments'] = buyer_comments['comments']
    return listing_details
