from core.ABC.data_transformer import DataTransformer
from models.user_model import User
import uuid


class UserTransformer(DataTransformer):
    def transform(self, data: User):
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
            "last_sign_in_date_time": signInActivity.lastSignInDateTime,
            "last_sign_in_request_id": signInActivity.lastSignInRequestId,
            "last_non_interactive_sign_in_date_time": signInActivity.lastNonInteractiveSignInDateTime,
            "last_non_interactive_sign_in_request_id": signInActivity.lastNonInteractiveSignInRequestId,
            "last_successful_sign_in_date_time": signInActivity.lastSuccessfulSignInDateTime,
            "last_successful_sign_in_request_id": signInActivity.lastSuccessfulSignInRequestId,
        }
