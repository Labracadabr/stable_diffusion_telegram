import os
from datetime import datetime
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image

# model
model_id = "stabilityai/stable-diffusion-2-1"
print('loading model:', model_id)
torch_dtype = torch.float32
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# device: gpu or cpu
if torch.cuda.is_available:
    device = "cuda:0"
else:
    device = "cpu"
print(f'{device = }')
pipe = pipe.to(device)


def sd_gen(payload: dict) -> Image:
    print('generating:', payload)

    try:
        # random seed
        generator = torch.manual_seed(payload.get('seed')) if payload.get('seed') else None
        image = pipe(
            prompt=payload['pos_prompt'],
            negative_prompt=payload['neg_prompt'],
            generator=generator,
            num_inference_steps=int(payload['steps_num']),
            resize_method="aspect",
            # width=payload.get("width"),
            # height=payload.get("height"),
        ).images[0]
    except Exception as e:
        return e

    print('generation success')
    return image


# сохранить фото с датой
def save_img(image, name) -> str:
    print('saving', name)
    output_dir = 'output_images'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_path = os.path.join(output_dir, f"{name}_{timestamp}.png")
    try:
        image.save(image_path)
    except:
        image[0].save(image_path)
    print('saved', image_path)
    return image_path


if __name__ == '__main__':
    test_payload = {
        "model_id": model_id,
        "pos_prompt": "realistic red sport car in urban surrounding",
        "neg_prompt": "disfigured, cartoon, anime, painting, sepia, b&w",
        # "width": 1024,
        # "height": 800,
        "steps_num": "5",
        "safety_checker": "yes",
        "seed": 1
    }

    img = sd_gen(payload=test_payload)
    save_img(img, 'sd-2-1')
    img.show()
