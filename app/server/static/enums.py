from enum import Enum


class TokenType(str, Enum):
    BEARER = 'bearer'
    RESET_PASSWORD = 'reset_password'
    REFRESH = 'refresh'


class Role(str, Enum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    TALENT = 'TALENT'
    CLIENT = 'CLIENT'


class AccountType(str, Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    ORGANIZATION = 'ORGANIZATION'


class AccountStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
