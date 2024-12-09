# import pytest
# from fastapi import FastAPI, status
# from fastapi.testclient import TestClient
# from httpx import AsyncClient
# from unittest.mock import AsyncMock, MagicMock, patch
# from app.server.routes.student import router
# from app.server.static.enums import Role

# # Create a test FastAPI app
# app = FastAPI()
# app.include_router(router)
# client = TestClient(app)

# @pytest.mark.asyncio
# @patch("app.server.services.student.core_service.read_one", new_callable=AsyncMock)
# @patch("app.server.services.student.core_service.update_one", new_callable=AsyncMock)
# @patch("app.server.services.student.core_service.get_session", new_callable=AsyncMock)
# async def test_student_create_success(mock_get_session, mock_update_one, mock_read_one):
#     # Mocking `get_session` to simulate an async context manager
#     mock_session = MagicMock()
#     mock_session.__aenter__.return_value = mock_session
#     mock_session.__aexit__.return_value = None
#     mock_get_session.return_value = mock_session

#     mock_read_one.side_effect = [None, None, None]

#     # Configure `update_one` to simulate successful creation
#     mock_update_one.side_effect = [
#     {"_id": "user123", "email": "example@test.com"},  # User creation with correct email
#     None,  # Password update
# ]


#     # Payload for the test request
#     request_payload = {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": "example@test.com",
#         "university": "Test University",
#         "university_id": "uni123",
#         "phone": "1234567890",
#         "address": "123 Test Street",
#         "password": "password123",
#     }

#     update_one_payload = {
#         "first_name": request_payload["first_name"],
#         "last_name": request_payload["last_name"],
#         "email": request_payload["email"],
#         "university": request_payload["university"],
#         "university_id": request_payload["university_id"],
#         "phone": request_payload["phone"],
#         "address": request_payload["address"],
#         "user_type": Role.STUDENT,
#         "is_verified": False,
#     }

#     # Use AsyncClient to send the POST request
#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.post("/student/create", json=request_payload)

#     # Assertions for the response
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json().get("status") == "SUCCESS"

#     # Assertions for `read_one` calls
#     mock_read_one.assert_any_call(
#     "users", data_filter={"email": "example@test.com", "is_deleted": False}
#     )
#     mock_read_one.assert_any_call(
#     "users", data_filter={"phone": request_payload["phone"], "is_deleted": False}
#     )
#     mock_read_one.assert_any_call(
#         "users",
#         data_filter={"university_id": request_payload["university_id"], "is_deleted": False},
#     )

#     # Assertions for `update_one` calls
#     mock_update_one.assert_any_call(
#         "users", data_filter= {"email": request_payload["email"]}, update={"$set": update_one_payload}, upsert=True, session=mock_session
#     )


#     assert mock_update_one.call_count == 2
#     assert mock_get_session.call_count == 1


# @pytest.mark.asyncio
# @patch("app.server.services.student.core_service.read_one", new_callable=AsyncMock)
# @patch("app.server.services.student.create_login_token", new_callable=AsyncMock)
# @patch("app.server.services.student.password_utils.check_password", new_callable=AsyncMock)
# @patch("app.server.services.student.core_service.update_one", new_callable=AsyncMock)
# async def test_student_login(mock_update_one, mock_check_password, mock_create_login_token, mock_read_one):
#     mock_read_one.side_effect = [
#         {"_id": "user123", "is_verified": True, "user_type": Role.STUDENT},
#         {"_id": "id123", "user_id": "user123", "password": "hashed_password"},
# ]

#     mock_create_login_token.side_effect = [
#         {'access_token': "access_token", 'access_token_expiry': 1000, 'refresh_token': "refresh_token"},
# ]

#     mock_check_password.side_effect = [True]

#     mock_update_one.side_effect = [None]

#     request_payload = {
#         "email": "example@test.com",
#         "password": "password123",
#     }

#     read_one_payload = {
#         "email": "example@test.com",
#         "is_deleted": False,
#     }

#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.post("/student/login", json=request_payload)

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json().get("status") == "SUCCESS"

#     mock_read_one.assert_any_call("users", data_filter=read_one_payload)
#     assert mock_read_one.call_count == 2
#     assert mock_check_password.call_count == 1
#     assert mock_create_login_token.call_count == 1
#     assert mock_update_one.call_count == 1
