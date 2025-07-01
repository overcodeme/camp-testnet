from eth_account import Account
from utils.logger import logger
from utils.file_manager import load_yaml, load_json, save_wallet_session_data
from utils.utils import sign_message, get_login_nonce
from data.const import headers
from actions.faucet import fetch_faucet
from datetime import datetime, timezone
import aiohttp


settings = load_yaml('config.yaml')
ATTEMPTS = settings['ATTEMPTS']
wallets_data = load_json('data/wallets_data.json')

class CampClient:
    def __init__(self, wallet: Account, proxy=None):
        self.wallet = wallet
        self.session = aiohttp.ClientSession(proxy=proxy if proxy else None)
        self.headers = headers

    async def handle_account(self):
        if not wallets_data.get(self.wallet.address):
            await self._login()

    async def _login(self):
        auth_url = 'https://loyalty.campnetwork.xyz/api/auth/callback/credentials'
        get_session_url = 'https://loyalty.campnetwork.xyz/api/auth/session'
        formatted_time = f'{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}'
        nonce = await get_login_nonce(self.wallet.address, self.session)
        message = f'loyalty.campnetwork.xyz wants you to sign in with your Ethereum account:\n{self.wallet.address}\n\nSign in to the app. Powered by Snag Solutions.\n\nURI: https://loyalty.campnetwork.xyz\nVersion: 1\nChain ID: 123420001114\nNonce: {nonce}\nIssued At: {formatted_time}Z'
        signature = await sign_message(self.wallet, message)

        data = {
            'message': {'domain': 'loyalty.campnetwork.xyz', 'address': self.wallet.address, 'statement': 'Sign in to the app. Powered by Snag Solutions.', 'uri': 'https://loyalty.campnetwork.xyz', 'version': '1', 'chainId': 123420001114, 'nonce': nonce, 'issuedAt': formatted_time},
            'accessToken': signature,
            'signature': signature,
            'walletConnectorName': 'Rabby',
            'walletAddress': self.wallet.address,
            'callbackUrl': '/protected',
            'chainType': 'evm',
            'csrfToken': nonce,
            'json': True
        }

        try:
            async with self.session.post(url=auth_url, json=data, headers=self.headers) as response:
                if response.status == 200:
                    save_wallet_session_data(self.wallet.address, 'cookies', response.cookies)
                    async with self.session.get(url=get_session_url, headers=self.headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            save_wallet_session_data(self.wallet.address, 'user_id', data['user']['id'])
                            logger.success(self.wallet.address, 'Successfully logged in')
                else:
                    logger.error(self.wallet.address, f'Error {response.status} while logging in: {await response.text()}')
        except Exception as e:
            logger.error(self.wallet.address, f'An error occurred while logging in: {e}')


    async def run_faucet(self):
        for _ in range(ATTEMPTS):
            try:
                await fetch_faucet(self.wallet.address, self.session)
                return
            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred while running faucet: {e}')