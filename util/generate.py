import time
from stability_sdk.interfaces.gooseai.generation import generation_pb2 as generation
from stability_sdk import client
import requests
import json
from v1.util.token_store import STABILITY_API_KEY, HUGGING_FACE_TOKEN # prod
# from token_store import STABILITY_API_KEY, HUGGING_FACE_TOKEN # test __main__
import replicate

# stability.ai SDK
# pip3 install stability-sdk
# https://github.com/Stability-AI/stability-sdk
rpc_client = client.StabilityInference(key=STABILITY_API_KEY, verbose=True)
# print(STABILITY_API_KEY)

def generate(prompt_en):
    # 另一个免费的替代品：https://lightning.ai/muse/view/null
    start = time.time()
    answers = rpc_client.generate(str(prompt_en))
    end = time.time()
    print("stability sdk cost(milli seconds): {}".format(end*1e3-start*1e3))
    # extract image from grpc resp
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                # ext = mimetypes.guess_extension(artifact.mime)
                contents = artifact.binary
    return contents


def chill_watcher_generate(prompt: str) -> str:
    # 每分钟$0.01
    # 计费模式：构建镜像不收费，但是模型初始化就开始收费了，一般初始化需要8min=$0.08，然后至少一个实例一直跑
    url = "https://ve32z1bqqdw86kaj.us-east-1.aws.endpoints.huggingface.cloud"
    form_data = {
        "inputs": {
            "prompt": prompt,
        }
    }
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+HUGGING_FACE_TOKEN,
    }
    start = time.time()
    resp = requests.post(url, headers=header, json=form_data)
    end = time.time()
    print("chill watcher inference cost(milli seconds): {}".format(end*1e3-start*1e3))
    if resp.status_code != 200:
        print("chill watcher error: ", resp.content)
        return ""
    print("chill watcher req success")
    resp_data = json.loads(resp.content)
    # if "img_data" not in resp_data.keys():
    #     print("chill watcher error: ", resp.content)
    #     return ""
    # img_b64_str = resp_data["img_data"]
    return resp_data


def replicate_chill_watcher_generate(prompt: str) -> str:
    # 每秒 $0.00055
    # 单次生成大概$0.02+，~=一元钱生成7次；计费模式：构建镜像&初始化都不收费，只有跑模型的时间计费，一次计算大概30s
    start = time.time()
    output = replicate.run(
        "wolverinn/chill_watcher:53d24c51f11d93e26f88cc53a00b5c392e5eb62272e07c46152af66a14e27cae",
        input={"prompt": prompt}
    )
    end = time.time()
    print("chill watcher replicate cost(milli seconds): {}".format(end*1e3-start*1e3))
    print("chill resp: ", output)
    return output


def lightning_chill_watcher_generate(prompt: str) -> str:
    # 每小时$1.5
    # 计费模式：启动app收费，启动大概花$0.18约8min，之后一直按时间计费，对扩容很友好
    url = "https://wsoqr-01gwy9mc1gzh3b4ce9b708vp31.litng-ai-03.litng.ai/predict"
    form = {
        "prompt": prompt,
    }
    start = time.time()
    resp = requests.post(url, json=form)
    end = time.time()
    print("chill watcher lightning cost(milli seconds): {}".format(end*1e3-start*1e3))
    if resp.status_code != 200:
        print("chill watcher error: ", resp.content)
        return ""
    print("chill watcher req success")
    resp_data = json.loads(resp.content)
    # if "img_data" not in resp_data.keys():
    #     print("chill watcher error: ", resp.content)
    #     return ""
    # img_b64_str = resp_data["img_data"]
    return resp_data


# https://replicate.com/huage001/adaattn
def style_transfer(img_data, style_img) -> str:
    start = time.time()
    # 输入有两个图像的时候，必须使用open("XX.png", 'rb')的方式打开传进来才行，否则会有奇怪的报错（replicate的报错不一定是远端代码的问题，而有可能只是格式没对）
    output_uri = replicate.run(
        "wolverinn/image-style-transfer-pytorch:8ea4cd5a7ca52805610df6a41c43178ba1e2dd310ac051b898974b2d459911b7",
        input={
            "content": img_data,
            "style": style_img,
        }
    )
    end = time.time()
    print("style_transfer replicate cost(milli seconds): {}".format(end*1e3-start*1e3))
    print("style_transfer resp uri: ", output_uri)
    return output_uri


# https://replicate.com/jagilley/controlnet-canny/api
model = replicate.models.get("jagilley/controlnet-canny")
version = model.versions.get("aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613")

def control_net_canny(prompt: str, img_data) -> str:
    inputs = {
        # Input image
        'image': img_data,

        # Prompt for the model
        'prompt': prompt,

        # Number of samples (higher values may OOM)
        'num_samples': "1",

        # Image resolution to be generated
        'image_resolution': "512",

        # Canny line detection low threshold
        # Range: 1 to 255
        'low_threshold': 100,

        # Canny line detection high threshold
        # Range: 1 to 255
        'high_threshold': 200,

        # Steps
        'ddim_steps': 20,

        # Scale for classifier-free guidance
        # Range: 0.1 to 30
        'scale': 9,

        # Seed
        # 'seed': ...,

        # Controls the amount of noise that is added to the input data during
        # the denoising diffusion process. Higher value -> more noise
        'eta': 0,

        # Additional text to be appended to prompt
        'a_prompt': "best quality, extremely detailed",

        # Negative Prompt
        'n_prompt': "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
    }

    # https://replicate.com/jagilley/controlnet-canny/versions/aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613#output-schema
    resp = version.predict(**inputs)
    # print(resp)
    if len(resp) < 2:
        return ""
    return resp[1]

if __name__ == "__main__":
    replicate_chill_watcher_generate("1girl, delicate, smiling")
    # control_net_canny("ocean, water", None)