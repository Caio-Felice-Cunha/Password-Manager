import string, secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)


    @classmethod
    def _get_random_string(cls, length = 25):
        random_string = ''
        for i in range(length):
            random_string += secrets.choice(cls.RANDOM_STRING_CHARS)

        return random_string

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        # Fernet requires URL-safe base64. Older standard-b64 keys still
        # decode to the same 32 bytes, so existing keys remain compatible.
        key = base64.urlsafe_b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        cls.KEY_DIR.mkdir(parents=True, exist_ok=True)

        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(length=5)}.key'

        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)

        return cls.KEY_DIR / file
    

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()

        # Re-raise InvalidToken so callers can tell a wrong key apart from a
        # stored value that happens to read like an error sentinel.
        return self.fernet.decrypt(value).decode()