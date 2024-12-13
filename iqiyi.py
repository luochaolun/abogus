import requests
import execjs
import os, re
import time
from urllib.parse import quote, unquote
import hashlib

class iqiyi:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬",
            "Cookie": self.load_cookie()
        }
        self.authkey = self.load_auth_js()
        self.cmd5js = self.load_cmd5x_js()
    def load_cookie(self):
        try:
            with open('iqycookie.txt', 'r', encoding='utf-8') as file:
                cookies = file.read().strip()
                return cookies
        except FileNotFoundError:
            print("警告：未找到iqycookie.txt文件，将继续不带Cookie进行请求。")
            return ""

    def load_auth_js(self):
        return execjs.compile(open("./js/iqiyi.js").read())

    def load_cmd5x_js(self):
        return execjs.compile(open("./js/cmd5x.js").read())

    def get_tvid(self):
        accelerator = "https://mesh.if.iqiyi.com/player/lw/lwplay/accelerator.js"
        headers = self.headers.copy()
        headers["Referer"] = self.url.split("?")[0]
        res = requests.get(accelerator, headers=headers)
        tvid = re.search('"tvid":([A-Za-z0-9]+)', res.text)
        vid = re.search('"vid":"([A-Za-z0-9]+)"', res.text)
        return tvid.group(1), vid.group(1)

    def join_params(self):
        tvid, vid = self.get_tvid()
        _time = int(time.time() * 1000)
        params = {
            "tvid": tvid,
            "bid": "600",
            "vid": vid,
            "src": "01010031010000000000",
            "vt": "0",
            "rs": "1",
            "uid": "5555743206005696",
            "ori": "pcw",
            "ps": "1",
            "k_uid": "29688c9e4ecf78f943053662a26cffbb",
            "pt": "0",
            "d": "0",
            "s": "",
            "lid": "0",
            "cf": "0",
            "ct": "0",
            "authKey": self.authkey.call("auth", self.authkey.call("auth", "") + f"{_time}{tvid}"),
            "k_tag": "1",
            "dfp": "a05c6b4142341b4d7080aaac8c74c083257560f64e24a5941f6fcb76a8557a6226",
            "locale": "zh_cn",
            "pck": "d3vm3NPQm1W0bE6CcoqPzLIm2lL6Hpucu5opX4OXrLtZpm3EsfXuQfbWte6x5xpP6qgJ4732",
            "k_err_retries": "0",
            "up": "",
            "qd_v": "a1",
            "tm": _time,
            "k_ft1": "706436220846084",
            "k_ft4": "1162321298202628",
            "k_ft5": "137573171201",
            "k_ft6": "128",
            "k_ft7": "671612932",
            "fr_300": "120_120_120_120_120_120",
            "fr_500": "120_120_120_120_120_120",
            "fr_600": "120_120_120_120_120_120",
            "fr_800": "120_120_120_120_120_120",
            "fr_1020": "120_120_120_120_120_120",
            "bop": quote(
                '{"version":"10.0","dfp":"a05c6b4142341b4d7080aaac8c74c083257560f64e24a5941f6fcb76a8557a6226"},"b_ft1":24'),
            "ut": "0"
        }
        temp = "/dash?"
        for k, v in params.items():
            temp += k + "=" + str(v) + "&"
        vf_str = self.authkey.call("addChar", temp[:-1])
        vf = hashlib.md5(vf_str.encode("utf-8")).hexdigest()
        params['vf'] = vf
        params["bop"] = unquote(params["bop"])
        return params

    def start(self, saveDir="./"):
        params = self.join_params()
        res = requests.get("https://cache.video.iqiyi.com/dash", params=params, headers=self.headers).json()
        #print(res["data"]["program"]["video"][2]["vid"])
        #print(res["data"]["program"]["video"][2]["m3u8"])
        #print(res["data"]["program"]["video"])
        #print(res)
        target_key = "m3u8"
        index_of_first_match = None
        for index, dict_ in enumerate(res["data"]["program"]["video"]):
            if target_key in dict_:
                index_of_first_match = index
                break

        if index_of_first_match is None:
            return ""

        filename = res["data"]["program"]["video"][index_of_first_match]["vid"].strip() + ".m3u8"
        filecontent = res["data"]["program"]["video"][index_of_first_match]["m3u8"].strip()
        with open(os.path.join(saveDir, filename), 'w', encoding='utf-8') as file:
            file.write(filecontent)
        return filename
'''
if __name__ == '__main__':
    fname = iqiyi("https://www.iqiyi.com/v_2f1dxvoww88.html").start()
    print(fname)
'''
