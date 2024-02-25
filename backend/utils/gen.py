import random, string


AUTH_TOKEN_ALLOWED_CHARS = string.ascii_letters + string.digits

def generate_token(length: int = 32, char_src: str = AUTH_TOKEN_ALLOWED_CHARS):
    return "".join(random.choice(char_src) for i in range(length))
