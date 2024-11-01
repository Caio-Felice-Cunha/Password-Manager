from ast import Pass
from datetime import datetime
from pathlib import Path
from xml import dom 

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    def save(self):
        # Ensure that the DB_DIR directory exists
        self.DB_DIR.mkdir(parents=True, exist_ok=True)

        table_path = self.DB_DIR / f'{self.__class__.__name__}.txt'

        # Print a debug message to check if save() is being called
        print(f"Attempting to create file at: {table_path}")

        # Create the file if it doesn't exist
        if not table_path.exists():
            table_path.touch()
            print("File created successfully.")
        else:
            print("File already exists.")
        

        with open(table_path, 'a') as arq:
            arq.write("|".join(list(map(str, self.__dict__.values()))))
            arq.write('\n')

    @classmethod
    def get(cls):
        table_path = cls.DB_DIR / f'{cls.__name__}.txt'

        if not table_path.exists():
            table_path.touch()
        
        with open(table_path, 'r') as arq:
            x = arq.readlines()
        
        results = []

        atributos = vars(cls())
        
        for i in x:
            split_v = i.split('|')
            tmp_dict = dict(zip(atributos, split_v))
            results.append(tmp_dict)

        return results

class Password(BaseModel):
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()

p1 = Password(domain='Youtube', password='abcd')
p1.save()
Password.get()