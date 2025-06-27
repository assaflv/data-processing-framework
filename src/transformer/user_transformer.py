from core.abstract import DataTransformer
from models.user_input_model import UserInput
import uuid


class UserTransformer(DataTransformer):
    def transform(self, data: UserInput):
        transformed_data = {
            "id": data.id,
            "external_id": str(uuid.uuid4()),
            "mail": data.mail,
            "type": data.userType,
            "location": data.usageLocation,
            "is_enabled": data.accountEnabled,
            "first_name": data.givenName,
            "last_name": data.surname,
            "sign_in_activity": self._sign_in_activity_map(data.signInActivity),
        }
        return transformed_data

    def _sign_in_activity_map(self, signInActivity):
        if not signInActivity:
            return None

        return {
            "last_sign_in": {
                "date_time": signInActivity.lastSignInDateTime,
                "request_id": signInActivity.lastSignInRequestId,
            },
            "last_non_interactive_sign_in": {
                "date_time": signInActivity.lastNonInteractiveSignInDateTime,
                "request_id": signInActivity.lastNonInteractiveSignInRequestId,
            },
            "last_successful_sign_in": {
                "date_time": signInActivity.lastSuccessfulSignInDateTime,
                "request_id": signInActivity.lastSuccessfulSignInRequestId,
            },
        }
