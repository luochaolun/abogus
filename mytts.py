import os, re, edge_tts, asyncio, random, string

class Mytts:
    def __init__(self):
        self.SAVE_DIR = "/var/www/html/defaultwww/fq/mp3/"
        self.SAVE_EXT = ".mp3"
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)

    def remove_html_tags(self, text):
        """去除字符串中的所有HTML标签"""
        return re.sub(r'<.*?>', '', text)

    def generate_random_string(self, length=10):
        letters = string.ascii_letters + string.digits
        ret = ''
        for _ in range(length):
            ret += random.choice(letters)
        return ret

    async def savetofile(self, text, aid=""):
        """Main function"""
        if aid == "":
            aid = self.generate_random_string()
        fnam = aid + self.SAVE_EXT
        savepath = self.SAVE_DIR + fnam
        if os.path.exists(savepath):
            return fnam
        txt = self.remove_html_tags(text)
        #print(txt)
        voice = "zh-CN-XiaoxiaoNeural"
        communicate = edge_tts.Communicate(text=txt, voice=voice, rate="+60%")
        #communicate.save_sync(savepath)
        #await communicate.save(savepath)
        with open(savepath, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        return fnam

    def getmp3(self, text, aid=""):
        fnam = asyncio.run(self.savetofile(text, aid))
        return fnam

#fnam = Mytts().getmp3("""<p class="yinwen">石守信等人这才听出了赵匡胤话中有话，连忙离席叩头说：“陛下何出此言？现在天命已定，谁还敢有异心？”赵匡胤神情开始严肃起来：“朕并非说诸位有什么异心，可是诸位想一想，倘若你们的部下想要富贵，一旦把黄袍加在你身上，你即使不想当皇帝，到时也身不由己了。朕就是先例呀！”</p>""")
#print(fnam)
