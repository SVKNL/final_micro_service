from src.api.v1.routers.task import router as router_tasks
from src.api.v1.routers.user import router as router_users

all_routers = [
    router_tasks,
    router_users,
]
