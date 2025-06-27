from models.user_input_model import UserInput, SignInActivity
from transformer.user_transformer import UserTransformer


def test_user_transformer():
    transformer = UserTransformer()
    user_data = UserInput(
        id="123",
        mail="test@example.com",
        userType="Member",
        usageLocation="US",
        accountEnabled=True,
        givenName="Test",
        surname="User",
        signInActivity=SignInActivity(lastSignInDateTime="2023-01-01T12:00:00Z"),
    )

    transformed = transformer.transform(user_data)

    assert transformed["id"] == "123"
    assert transformed["mail"] == "test@example.com"
    assert transformed["is_enabled"] is True
    assert "external_id" in transformed
    assert transformed["sign_in_activity"]["last_sign_in"]["date_time"] == "2023-01-01T12:00:00Z"
