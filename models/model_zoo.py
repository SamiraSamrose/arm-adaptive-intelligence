import os
import json
from typing import Dict, List, Optional

class ModelZoo:
    """
    Manages available pre-trained models
    """
    
    def __init__(self, models_dir: str = "models/pretrained"):
        self.models_dir = models_dir
        self.manifest_path = os.path.join(models_dir, "model_manifest.json")
        self.models = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """
        Loads model manifest
        """
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {"models": []}
    
    def list_models(self) -> List[Dict]:
        """
        Lists all available models
        """
        return self.models.get("models", [])
    
    def get_model(self, name: str) -> Optional[Dict]:
        """
        Gets model by name
        """
        for model in self.models.get("models", []):
            if model["name"] == name:
                return model
        return None
    
    def get_model_path(self, name: str) -> Optional[str]:
        """
        Gets full path to model file
        """
        model = self.get_model(name)
        if model:
            return os.path.join(self.models_dir, model["filename"])
        return None
    
    def add_model(self, model_info: Dict):
        """
        Adds a new model to the manifest
        """
        if "models" not in self.models:
            self.models["models"] = []
        
        self.models["models"].append(model_info)
        
        with open(self.manifest_path, 'w') as f:
            json.dump(self.models, f, indent=2)
    
    def get_recommended_models(self, task: str) -> List[Dict]:
        """
        Gets recommended models for a task
        """
        task_mapping = {
            "image_classification": ["MobileNetV2", "ResNet18"],
            "object_detection": ["YOLOv5s"],
            "text_embedding": ["TinyBERT"],
            "speech_recognition": ["Whisper-tiny"]
        }
        
        recommended_names = task_mapping.get(task, [])
        return [m for m in self.list_models() if m["name"] in recommended_names]

if __name__ == '__main__':
    zoo = ModelZoo()
    print("Available models:")
    for model in zoo.list_models():
        print(f"- {model['name']}: {model['description']}")