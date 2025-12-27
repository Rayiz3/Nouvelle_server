import torch
import trimesh
from pathlib import Path
from diffusers import ShapEPipeline
from diffusers.utils import export_to_ply

_pipe = None # Global var. for the pipeline instance to enable chaching

# Load & Cache the pipeline
def load_pipeline():
    global _pipe
    
    MODEL_DIR = Path(__file__).parent / "shap_e"
    
    if _pipe is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        _pipe = ShapEPipeline.from_pretrained(
            MODEL_DIR,
            torch_dtype=dtype,
            local_files_only=True
        ).to(device)
    
    return _pipe

# Generate a 3D mesh from a text prompt and save it as .glb file
def generate_mesh(
    prompt: str,
    output_path: str = "meshes",
    filename: str = "sample_mesh",
    guidance_scale: float = 15.0,
    num_inference_steps: int = 64,
    frame_size: int = 256,
):
    pipe = load_pipeline()
    
    output_dir = f"{output_path}/{filename}"
    
    images = pipe(
        prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        frame_size=frame_size,
        output_type="mesh"
    ).images

    export_to_ply(images[0], f"{output_dir}.ply")
    mesh = trimesh.load(f"{output_dir}.ply")
    mesh.export(f"{output_dir}.glb", file_type="glb")
    
    return f"{output_dir}.glb"


if __name__ == "__main__":
    path = generate_mesh(
        prompt="Orgrim Doomhammer",
        filename="Orgrim_Doomhammer"
    )
    print("Saved to:", path)