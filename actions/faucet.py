from utils.captcha import hCaptchaSolver
from utils.logger import logger
from utils.file_manager import load_yaml
import aiohttp


settings = load_yaml('config.yaml')

async def fetch_faucet(wallet_address, session = aiohttp.ClientSession):
    url = 'https://faucet-go-production.up.railway.app/api/claim'
    solver = hCaptchaSolver(api_key=settings['SOLVECAPTCHA_KEY'])
    await solver.create_captcha_task(
        sitekey='5b86452e-488a-4f62-bd32-a332445e2f51',
        page_url='faucet.campnetwork.xyz'
    )
    captcha_token = await solver.get_captcha_result()
    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4',
        'content-type': 'application/json',
        'h-captcha-response': captcha_token,
        'origin': 'https://faucet.campnetwork.xyz',
        'priority': 'u=1, i',
        'referer': 'https://faucet.campnetwork.xyz/',
        'sec-ch-ua': '"Chromium";v="133", "Google Chrome";v="133", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }

    data = {
        'address': wallet_address
    }

    try:
        async with session.post(url=url, headers=headers, json=data) as response:
            if response.status == 200:
                logger.success(wallet_address, f'Successfully claimed faucet: {await response.json()}')
            else:
                logger.error(wallet_address, f'Error while fetching faucet: {await response.text()}')
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while fetching faucet: {e}')
    finally: 
        await session.close()