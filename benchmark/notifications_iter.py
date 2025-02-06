import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_tool import Timer
from physicsLab import web

user = web.User(
    token="tGTf8gbQBR9P0ZnWhSILjJ5oF6UOkVdm",
    auth_code="xJwcHC7oOnlSdzUTh9NDZ0t1Q32MjPyB",
)

with Timer():
    for i, _ in enumerate(web.NotificationsIter(
        user, category_id=5
    )):
        if i == 10000:
            break

# -- outputs --
# time: 39.03123497962952
