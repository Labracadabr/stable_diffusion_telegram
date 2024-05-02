import asyncio
import os
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
device = "cuda:0" if torch.cuda.is_available else "cpu"
print(f'{device = }')
pipe = pipe.to(device)


async def sd_gen(payload: dict) -> Image:
    print('generating:', payload)

    try:
        # random seed
        generator = torch.manual_seed(payload.get('seed')) if payload.get('seed') else None
        image = await asyncio.to_thread(
            lambda: pipe(
                prompt=payload['pos_prompt'],
                negative_prompt=payload['neg_prompt'],
                generator=generator,
                num_inference_steps=int(payload['steps_num']),
                resize_method="aspect",
                # width=payload.get("width"),
                # height=payload.get("height"),
            ).images[0])
    except Exception as e:
        return e

    print('generation success')
    return image


# сохранить фото
def save_img(image, folder, file_name) -> str:
    print('saving', file_name)
    # папка
    os.makedirs(folder, exist_ok=True)

    image_path = os.path.join(folder, file_name)
    try:
        image.save(image_path)
    except:
        image[0].save(image_path)
    print('saved', image_path)
    return image_path


if __name__ == '__main__':
    x = 0
    for i in range(50, 51):
        print(i, 'i')
        if i not in (50,):
            continue

        test_payload = {
            "model_id": model_id,
            "pos_prompt": "ultra realistic astronaut riding a horse on mars, normal bodies, normal limbs, high quality, spacious desert, moon is seen at the sky ",
            "neg_prompt": "disfigured, cartoon, anime, painting, low resolution",
            # "width": 1024,
            # "height": 800,
            "steps_num": i,
            "safety_checker": "yes",
            "seed": 3
        }

        img = sd_gen(payload=test_payload)
        save_img(img, f'step_{i}')
        img.show()
