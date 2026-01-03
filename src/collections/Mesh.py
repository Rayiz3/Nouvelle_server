from pydantic import BaseModel

class Mesh(BaseModel):
    user_id: str
    prompt: str
    iconMeshUrl: str
    
    def to_mongo_dict(self):
        return {
            'user_id': self.user_id,
            'prompt': self.prompt,
            'iconMeshUrl': self.iconMeshUrl,
        }