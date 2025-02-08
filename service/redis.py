import json
import logging
from redis.asyncio import Redis
from pydantic import BaseModel
from datetime import datetime

redis_client = Redis(host="redis", port=6379, db=0, decode_responses=True)

class User(BaseModel):
    id: int
    name: str | None = None
    phone: str | None = None
    username: str | None = None
    email: str | None = None
    approved: bool | None = None
    date_joined: datetime | None = None

    async def save_to_redis(self):
        user_data = self.model_dump()
        if user_data["date_joined"]:
            user_data["date_joined"] = user_data["date_joined"].isoformat()
        await redis_client.set(f"user:{self.id}", json.dumps(user_data))
        logging.info(f"User {self.id} saved to redis")

    @staticmethod
    async def get_from_redis(user_id: int):
        user_data = await redis_client.get(f"user:{user_id}")
        if user_data:
            user_dict = json.loads(user_data)
            if user_dict.get("date_joined"):
                user_dict["date_joined"] = datetime.fromisoformat(user_dict["date_joined"])
            return User(**user_dict)
        return None

    async def update_in_redis(self, **kwargs):
        existing_user = await User.get_from_redis(self.id)
        if not existing_user:
            logging.info(f"User {self.id} does not exist")
            return None

        updated_user = existing_user.model_dump() | kwargs
        if updated_user.get("date_joined") and isinstance(updated_user["date_joined"], datetime):
            updated_user["date_joined"] = updated_user["date_joined"].isoformat()

        await redis_client.set(f"user:{self.id}", json.dumps(updated_user))
        logging.info(f"User {self.id} updated in redis")

        return User(**updated_user)

    @classmethod
    async def exist_in_redis(cls, user_id: int) -> bool:
        return await redis_client.exists(f"user:{user_id}") > 0

    @classmethod
    async def get_all_from_redis(cls):
        keys = await redis_client.keys("user:*")
        users = []
        for key in keys:
            user_data = await redis_client.get(key)
            if user_data:
                user_dict = json.loads(user_data)
                if user_dict.get("date_joined"):
                    user_dict["date_joined"] = datetime.fromisoformat(user_dict["date_joined"])
                users.append(User(**user_dict))
        return users

