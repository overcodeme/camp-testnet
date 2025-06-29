from eth_account import Account
from utils.logger import logger
from utils.file_manager import load_yaml, load_txt, load_json
from colorama import Fore, Style
from actions.faucet import fetch_faucet
import aiohttp
import random


settings = load_yaml('config.yaml')
ATTEMPTS = settings['ATTEMPTS']

class CampClient:
    def __init__(self, wallet: Account, proxy=None):
        self.wallet = wallet
        self.session = aiohttp.ClientSession(proxy=proxy if proxy else None)
        self.headers = None


    async def run_faucet(self):
        for _ in range(ATTEMPTS):
            try:
                await fetch_faucet(self.wallet.address, self.session)
                return
            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred while running faucet: {e}')