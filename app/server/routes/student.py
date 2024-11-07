from typing import Any

from fastapi import APIRouter, Depends

from app.server.models.auth import EmailLoginRequest, OtpRequest, VerifyOtpRequest
from app.server.models.users import UserCreateRequest, UserUpdateRequest
from app.server.services import student
from app.server.utils.token_util import JWTAuthUser

router = APIRouter()


@router.post('/students/create', summary='Creates new students accounts')
async def student_create(params: UserCreateRequest) -> dict[str, Any]:
    data = await student.create_user(params)
    return {'data': data, 'status': 'SUCCESS'}


@router.post('/students/login', summary='Email based login')
async def student_login(params: EmailLoginRequest) -> dict[str, Any]:
    data = await student.login(params)
    return {'data': data, 'status': 'SUCCESS'}


@router.post('/students/send_otp', summary='Send otp to email id')
async def send_otp(params: OtpRequest) -> dict[str, Any]:
    data = await student.send_otp(params)
    return {'data': data, 'status': 'SUCCESS'}


@router.post('/students/verify_otp', summary='Verify otp sent to email id for verification or password reset flow')
async def verify_otp(params: VerifyOtpRequest) -> dict[str, Any]:
    data = await student.verify_otp(params)
    return {'data': data, 'status': 'SUCCESS'}


@router.post('/refresh', summary='Creates new access token for session maintenance')
# async def refresh_access_token(refresh_token: str = Body(..., embed=True)) -> dict[str, Any]:
async def refresh_access_token(refresh_token: str) -> dict[str, Any]:
    data = await student.refresh_access_token(refresh_token)
    return {'data': data, 'status': 'SUCCESS'}


# @router.get("/auth/users/paginated", summary="Gets all users in paginated form")
# async def get_all_industry_paginated(
#     page: int = 1, page_size: int = 10, search_query: Optional[str] = None
# ) -> dict[str, Any]:
#     data = await student.get_students_paginated(
#         page=page, page_size=page_size, search_query=search_query
#     )
#     return {"data": data, "status": "SUCCESS"}


@router.put('/students/update', summary='Update student profile')
async def student_update(params: UserUpdateRequest, user_data=Depends(JWTAuthUser(['STUDENT']))) -> dict[str, Any]:
    data = await student.student_update(params, user_data)
    return {'data': data, 'status': 'SUCCESS'}
