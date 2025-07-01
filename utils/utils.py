from utils.logger import logger
from eth_account import Account
from eth_account.messages import encode_defunct
from aiohttp import ClientSession


async def sign_message(wallet: Account, message):
    encoded_message = encode_defunct(text=message)
    signed_message = wallet.sign_message(encoded_message)
    return f'0x{signed_message.signature.hex()}'


async def get_login_nonce(wallet_address: str, session: ClientSession):
    url = 'https://loyalty.campnetwork.xyz/api/auth/csrf'
    
    try:
        async with session.get(url=url) as response:
            if response.status == 200:
                data = await response.json()
                return data['csrfToken']
    except Exception as e:
        logger.error(wallet_address, f'Error while getting csrfToken: {await response.text()}')
        