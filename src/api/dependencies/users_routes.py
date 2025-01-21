from fastapi_users import FastAPIUsers

from api.dependencies.backend import authentication_backend
from api.dependencies.users import get_user_manager
from core.models.user.user_model import User
from core.types.user_types import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
