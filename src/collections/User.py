from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    
    def to_mongo_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'config': {
                'color': '#ffffff',
                'stacks': [],
                'links': []
            }
        }