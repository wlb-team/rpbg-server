import json
import os

# django里的路径都是从manage.py的目录开始的
# 或者直接写死绝对路径
dir_path = os.path.dirname(os.path.abspath(__file__))
# print(dir_path)
TOKEN_FILE_PATH = os.path.join(dir_path, "token_secret.json") # prod environment
STABILITY_API_KEY = ""
HUGGING_FACE_TOKEN = ""
OPENAI_KEY = ""
if STABILITY_API_KEY == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    STABILITY_API_KEY = token_json.get("stability_key")
if HUGGING_FACE_TOKEN == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    HUGGING_FACE_TOKEN = token_json.get("hugging_face_token")
if OPENAI_KEY == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    OPENAI_KEY = token_json.get("openai_key")


REPLICATE_TOKEN = ""
if REPLICATE_TOKEN == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    REPLICATE_TOKEN = token_json.get("replicate_key")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

RUNPOD_TOKEN = ""
if RUNPOD_TOKEN == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    RUNPOD_TOKEN = token_json.get("runpod")

AIOS_KEY = ""
if AIOS_KEY == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    AIOS_KEY = token_json.get("aios_key")

vcaptcha_key = ""
if vcaptcha_key == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    vcaptcha_key = token_json.get("verify_sk")

cf_key = ""
if cf_key == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    cf_key = token_json.get("verify_cf_sk")

wx_app_secret = "" # ???
if wx_app_secret == "":
    token_json = json.load(open(TOKEN_FILE_PATH, 'r'))
    wx_app_secret = token_json.get("wx_api_secret")