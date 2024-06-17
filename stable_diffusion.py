import asyncio
import os
import torch
from PIL import Image

# model
model_id = "stabilityai/stable-diffusion-3-medium"
# model_id = "stabilityai/stable-diffusion-2-1"
print('loading model:', model_id)

# v2
if model_id == 'stabilityai/stable-diffusion-2-1':
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    torch_dtype = torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# v3
elif model_id == 'stabilityai/stable-diffusion-3-medium':
    from diffusers import StableDiffusion3Pipeline
    torch_dtype = torch.float16
    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers")

else:
    exit(f'wrong model {model_id}')

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

    test_payload = {
        "model_id": model_id,
        "pos_prompt": "ultra realistic astronaut riding a horse on mars, normal bodies, normal limbs, high quality, spacious desert, moon is seen at the sky ",
        "neg_prompt": "disfigured, cartoon, anime, painting, low resolution",
        # "width": 1024,
        # "height": 800,
        "steps_num": 5,
        "safety_checker": "yes",
        "seed": 3
    }

    img = asyncio.run(sd_gen(payload=test_payload))
    img.show()
    save_img(img, f'folder', f'img.jpg')
