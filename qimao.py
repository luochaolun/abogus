# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
import re, random, hashlib, requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

headers_dict = {}
sign_key = 'd3dGiJc651gSQ8w1'

# 替换非法字符
def rename(name):
    # 定义非法字符的正则表达式模式
    illegal_characters_pattern = r'[\/:*?"<>|]'

    # 定义替换的中文符号
    replacement_dict = {
        '/': '／',
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': '“',
        '<': '＜',
        '>': '＞',
        '|': '｜'
    }

    # 使用正则表达式替换非法字符
    sanitized_path = re.sub(illegal_characters_pattern, lambda x: replacement_dict[x.group(0)], name)

    return sanitized_path

# 定义解密函数
def decrypt(data, iv):
    # print(f"Decrypting data: {data}")
    # print(f"Using iv: {iv}")
    key = bytes.fromhex('32343263636238323330643730396531')
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(bytes.fromhex(data)), AES.block_size)
    return decrypted.decode('utf-8')


# 定义qimao函数
def decrypt_qimao(content):
    # print(f"Decrypting content: {content}")
    txt = b64decode(content)
    iv = txt[:16].hex()
    # print(f"IV: {iv}")
    fntxt = decrypt(txt[16:].hex(), iv).strip().replace('\n', '<br>')
    return fntxt


def get_headers(book_id):
    version_list = [
        '73720', '73700',
        '73620', '73600',
        '73500',
        '73420', '73400',
        '73328', '73325', '73320', '73300',
        '73220', '73200',
        '73100', '73000', '72900',
        '72820', '72800',
        '70720', '62010', '62112',
    ]

    random.seed(book_id)

    version = random.choice(version_list)

    headers = {
        "AUTHORIZATION": "",
        "app-version": f"{version}",
        "application-id": "com.****.reader",
        "channel": "unknown",
        "net-env": "1",
        "platform": "android",
        "qm-params": "",
        "reg": "0",
    }

    # 获取 headers 的所有键并排序
    keys = sorted(headers.keys())

    # 生成待签名的字符串
    sign_str = ''.join([k + '=' + str(headers[k]) for k in keys]) + sign_key

    # 生成签名
    headers['sign'] = hashlib.md5(sign_str.encode()).hexdigest()

    return headers

def get_qimao(book_id, chapter_id, sign):
    if book_id not in headers_dict:
        headers_dict[book_id] = get_headers(book_id)
    headers = headers_dict[book_id]
    response = requests.get(f"https://api-ks.wtzw.com/api/v1/chapter/content?"
                            f"id={book_id}&chapterId={chapter_id}&sign={sign}",
                            headers=headers)
    return response.json()

def asset_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("assets"), relative_path)

def getQmArticleCont(book_id, chapter_id):
    param_string = f"chapterId={chapter_id}id={book_id}{sign_key}"
    sign = hashlib.md5(param_string.encode()).hexdigest()
    encrypted_content = get_qimao(book_id, chapter_id, sign)

    chapter_content = ""
    if "data" in encrypted_content and "content" in encrypted_content["data"]:
        encrypted_content = encrypted_content['data']['content']
        chapter_content = decrypt_qimao(encrypted_content)
        chapter_content = re.sub('<br>', '\n', chapter_content)
        #chapter_content = '<p>' + re.sub('<br>', '</p><p>', chapter_content) + '</p>'

    return chapter_content
'''
book_id = 1830570
chapter_id = 17240572810189
thisArtCont = getQmArticleCont(book_id, chapter_id)
print(thisArtCont)
'''
