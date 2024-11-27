from enum import Enum


class TokenType(str, Enum):
    BEARER = 'bearer'
    RESET_PASSWORD = 'reset_password'
    REFRESH = 'refresh'


class Role(str, Enum):
    ADMIN = 'ADMIN'
    STUDENT = 'STUDENT'


class AccountType(str, Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    ORGANIZATION = 'ORGANIZATION'


class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class VerificationType(str, Enum):
    AUTHENTICATION = 'AUTHENTICATION'
    FORGOT_PASSWORD = 'FORGOT_PASSWORD'


class ListingStatus(str, Enum):
    NEW = 'NEW'
    ON_HOLD = 'ON_HOLD'
    SOLD = 'SOLD'


class SaleStatus(str, Enum):
    INTERESTED = 'INTERESTED'
    SHARE_DETAILS = 'SHARE_DETAILS'
    SOLD = 'SOLD'
    REJECTED = 'REJECTED'
