import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.config.settings import settings
from src.utils.exceptions import AuthenticationError
from src.utils.jwt_utils import create_access_token, decode_token

# Test data for JWT token generation and verification
test_user_data = {
    "sub": "testuser",
    "role": "patron",
}

test_payload = {
    "sub": "testuser",
    "role": "patron",
    "exp": datetime.utcnow() + timedelta(minutes=15),
}

# Test case for creating a valid JWT access token
def test_create_access_token_valid():
    """Tests the creation of a valid JWT access token."""
    token = create_access_token(data=test_user_data, expires_delta=timedelta(minutes=15))
    assert isinstance(token, str)
    assert token is not None

# Test case for decoding a valid JWT access token
def test_decode_token_valid():
    """Tests the decoding of a valid JWT access token."""
    token = create_access_token(data=test_payload, expires_delta=timedelta(minutes=15))
    decoded_token = decode_token(token)
    assert isinstance(decoded_token, dict)
    assert decoded_token["sub"] == test_user_data["sub"]
    assert decoded_token["role"] == test_user_data["role"]

# Test case for handling an expired JWT access token
def test_decode_token_expired():
    """Tests the handling of an expired JWT access token."""
    token = create_access_token(data=test_payload, expires_delta=timedelta(seconds=1))
    with pytest.raises(AuthenticationError):
        decode_token(token)

# Test case for handling an invalid JWT access token
def test_decode_token_invalid():
    """Tests the handling of an invalid JWT access token."""
    with pytest.raises(AuthenticationError):
        decode_token("invalid_token")

# Test case for handling exceptions during token decoding
@patch("src.utils.jwt_utils.jwt.decode")
def test_decode_token_exception(mock_decode):
    """Tests the handling of exceptions during JWT token decoding."""
    mock_decode.side_effect = Exception("Error decoding token")
    with pytest.raises(AuthenticationError):
        decode_token("test_token")