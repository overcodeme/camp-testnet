import asyncio
import curses
from eth_account import Account
from utils.file_manager import load_yaml, load_txt
from utils.logger import logger
from camp_client import CampClient
from data.const import menu_items
from utils.menu import menu
from colorama import Fore, Style
import os


settings = load_yaml('config.yaml')
wallets = load_txt('data/wallets.txt')
proxies = load_txt('data/proxies.txt')


async def handle_wallet(wallet: Account, action_name, proxy=None):
    wallet = Account.from_key(wallet)
    camp = CampClient(wallet=wallet, proxy=proxy)
    try:
        await camp.handle_account()
        action_func = getattr(camp, action_name)
        await action_func()
    except Exception as e:
        logger.error(wallet.address, f'An error occurred while handling wallet: {e}')
    finally:
        await camp.session.close()


async def main():
    if not wallets:
        print(Fore.RED + 'No wallets found' + Style.RESET_ALL)
        return

    options = menu_items
    chosen_action = options[curses.wrapper(menu)]['func']
    os.system('cls' if os.name == 'nt' else 'clear')

    tasks = []

    if proxies:
        for w, p in zip(wallets, proxies):
            tasks.append(handle_wallet(wallet=w, proxy=p, action_name=chosen_action))
    else:
        for w in wallets:
            tasks.append(handle_wallet(wallet=w, action_name=chosen_action))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())