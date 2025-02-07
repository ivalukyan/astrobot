import json
import logging
from redis.asyncio import Redis
from pydantic import BaseModel, EmailStr
from datetime import datetime


redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)


class User(BaseModel):
    id: int
    name: str | None = None
    phone: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    approved: bool | None = None
    date_joined: datetime | None = None

    async def save_to_redis(self):
        await redis_client.set(f"user:{self.id}", self.model_dump_json())
        logging.info(f"User {self.id} saved to redis")

    @staticmethod
    async def get_from_redis(self):
        user_data = await redis_client.get(f"user:{self.id}")
        if user_data:
            return User(**json.loads(user_data))
        return None

    async def update_in_redis(self, **kwargs):
        existing_user = await self.get_from_redis(self.id)
        if not existing_user:
            logging.info(f"User {self.id} does not exist")
            return None

        updated_user = existing_user.model_dump() | kwargs
        await redis_client.set(f"user:{self.id}", json.dumps(updated_user))
        logging.info(f"User {self.id} updated from redis")

        return User(**updated_user)

    @classmethod
    async def exist_in_redis(cls, user_id: int) -> bool:
        return await redis_client.exists(f"user:{user_id}") > 0
