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
    counter = 0
    for msg in web.RelationsIter(
        user,
        user_id="6746f0d95ff382342fa09c87",
        display_type="Following",
        max_retry=2,
        max_workers=16,
    ):
        counter += 1

    print(counter)

# -- outputs --
# 59268
# time: 237.02915596961975
