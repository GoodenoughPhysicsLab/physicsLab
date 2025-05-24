import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_tool import Timer
from physicsLab import web

if not os.path.exists("images") or not os.path.isdir("images"):
    os.mkdir("images")

user = web.token_login(
    token="tGTf8gbQBR9P0ZnWhSILjJ5oF6UOkVdm",
    auth_code="xJwcHC7oOnlSdzUTh9NDZ0t1Q32MjPyB",
)

with Timer():
    counter = 0
    for img in web.AvatarsIter(
        user,
        target_id="62fb41236851afa7c6db7929",
        category="User",
        max_workers=32,
    ):
        with open(f"images/{counter}.png", 'wb') as f:
            f.write(img)
        counter += 1

    print(counter)

# -- outputs --
# 313
# time: 21.524598360061646
