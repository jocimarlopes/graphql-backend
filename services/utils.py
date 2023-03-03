import base64

def isBase64(data):
    try:
        base64.b64encode(base64.b64decode(data))
        return True
    except Exception:
        return False