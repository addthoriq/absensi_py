from unittest import TestCase
from common.responses import (
    Ok,
    Created,
    NoContent,
    NotFound,
    Unauthorized,
    BadRequest,
    Forbidden,
    InternalServerError,
    common_response,
)


class TestResponseService(TestCase):
    def test_Ok(self):
        # Given
        req = Ok(data={"id": 1, "name": "Test User OK"})

        # When
        result = common_response(res=req)

        # Expect
        self.assertEqual(result.body, b'{"id":1,"name":"Test User OK"}')
        self.assertEqual(result.status_code, 200)

    def test_Created(self):
        # Given
        req = Created(data={"id": 1, "name": "Test User Created"})

        # When
        result = common_response(res=req)

        # Expect
        self.assertEqual(result.body, b'{"id":1,"name":"Test User Created"}')
        self.assertEqual(result.status_code, 201)

    def test_NoContent(self):
        # Given
        req = NoContent()

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.status_code, 204)

    def test_BadRequest(self):
        # Given
        req = BadRequest(message="Bad request sample message")

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"message":"Bad request sample message"}')
        self.assertEqual(result.status_code, 400)

    def test_BadRequestCustomResponse(self):
        # Given
        req = BadRequest(custom_response={"custom": "Bad request custom response"})

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"custom":"Bad request custom response"}')
        self.assertEqual(result.status_code, 400)

    def test_Unauthorized(self):
        # Given
        req = Unauthorized()

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"message":"Unauthorized"}')
        self.assertEqual(result.status_code, 401)

    def test_UnauthorizedCustomResponse(self):
        # Given
        req = Unauthorized(custom_response={"custom": "Unauthorized Custom Response"})

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"custom":"Unauthorized Custom Response"}')
        self.assertEqual(result.status_code, 401)

    def test_Forbidden(self):
        # Given
        req = Forbidden()

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(
            result.body,
            b'{"message":"You don\'t have permission to perform this action!"}',
        )
        self.assertEqual(result.status_code, 403)

    def test_ForbiddenCustomResponse(self):
        # Given
        req = Forbidden(custom_response={"custom": "Forbidden Custom"})

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"custom":"Forbidden Custom"}')
        self.assertEqual(result.status_code, 403)

    def test_NotFound(self):
        # Given
        req = NotFound()

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"message":"Not Found"}')
        self.assertEqual(result.status_code, 404)

    def test_InternalServerError(self):
        # Given
        req = InternalServerError(error="Something wrong with application")

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"error":"Something wrong with application"}')
        self.assertEqual(result.status_code, 500)

    def test_InternalServerErrorCustomResponse(self):
        # Given
        req = InternalServerError(custom_response={"custom": "The Server was Error"})

        # When
        result = common_response(req)

        # Expect
        self.assertEqual(result.body, b'{"custom":"The Server was Error"}')
        self.assertEqual(result.status_code, 500)
