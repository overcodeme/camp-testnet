from aiohttp import ClientSession
import asyncio
import random


class hCaptchaSolver:
    def __init__(self, api_key, proxy=None):
        self.api_key = api_key
        self.session = ClientSession(proxy)
        self.task_id = None
    
    async def create_captcha_task(self, sitekey, page_url):
        url = f'http://api.solvecaptcha.com/in.php?key={self.api_key}&method=hcaptcha&sitekey={sitekey}&pageurl={page_url}/register&json=1'

        async with self.session.get(url) as response:
            data = await response.json()
            self.task_id = data['request']
            
    async def get_captcha_result(self):
        url = f'http://api.solvecaptcha.com/res.php?key={self.api_key}&action=get&id={self.task_id}'
        while True:
            async with self.session.get(url) as response:
                data = await response.text()
                print(data)
                if 'CAPCHA_NOT_READY' in data:
                    await asyncio.sleep(random.randint(15, 30))
                    continue
                return data.split('|')[1]