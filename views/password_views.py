import string, secrets
import hashlib
import base64
from pathlib import Path

class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    @classmethod    
    def _get_random_string(cls, length = 25):
        string = ''
        for i in range(length):
            string += secrets.choice(cls.RANDOM_STRING_CHARS)

        return string

    @classmethod
    def create_key(cls):
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64decode(hasher)
        print(key)

    @classmethod
    def archive_key(cls, key):
        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(length=5)}.key'

        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key.encode()) 


FernetHasher.archive_key('abc')