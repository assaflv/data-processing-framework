from typing import List, Optional
from pydantic import BaseModel


class SignInActivity(BaseModel):
    lastSignInDateTime: Optional[str] = None
    lastSignInRequestId: Optional[str] = None
    lastNonInteractiveSignInDateTime: Optional[str] = None
    lastNonInteractiveSignInRequestId: Optional[str] = None
    lastSuccessfulSignInDateTime: Optional[str] = None
    lastSuccessfulSignInRequestId: Optional[str] = None


class UserInput(BaseModel):
    userPrincipalName: Optional[str] = None
    usageLocation: Optional[str] = None
    mail: Optional[str] = None
    accountEnabled: Optional[bool] = None
    mobilePhone: Optional[str] = None
    userType: Optional[str] = None
    givenName: Optional[str] = None
    surname: Optional[str] = None
    otherMails: Optional[List[str]] = None
    id: str
    signInActivity: Optional[SignInActivity] = None


class UsersResponse(BaseModel):
    value: List[UserInput] = None
