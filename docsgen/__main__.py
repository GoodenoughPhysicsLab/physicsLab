from . import webapi

if __name__ == "__main__":
    webapi.main()
else:
    raise RuntimeError("this module is not supposed to be imported")
