if __name__ != "__main__":
    raise RuntimeError("this module is not supposed to be imported")

from . import webapi
from . import elements

webapi.main()
elements.main()
