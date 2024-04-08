# solana-webwallet/external_services/solana/solana.py

import time
import traceback
from typing import Tuple, Dict, List, Optional, Any

import base58
import httpx
from solana.rpc.api import Keypair
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction_status import TransactionConfirmationStatus

# Константа для определения URL-адреса узла Solana в тестовой сети Devnet
#SOLANA_NODE_URL = "https://api.testnet.solana.com"
SOLANA_NODE_URL = "https://api.devnet.solana.com"

# Константа для определения соотношения между лампортами и SOL. 1 SOL = 10^9 лампортов.
LAMPORT_TO_SOL_RATIO = 10 ** 9

# Константа для определения длины шестнадцатеричного представления приватного ключа в символах.
PRIVATE_KEY_HEX_LENGTH = 64

# Константа для определения длины двоичного представления приватного ключа в байтах.
PRIVATE_KEY_BINARY_LENGTH = 32

# Константа, определяющая длительность существования кеша для истории транзакций (в секундах).
# Здесь установлено значение 3600 секунд (1 час).
TRANSACTION_HISTORY_CACHE_DURATION = 3600
# Создание клиента для подключения к тестовой сети
client = Client(SOLANA_NODE_URL)

# Создаем словарь для кэширования результатов запросов истории транзакций
transaction_history_cache: Dict[str, Tuple[List, float]] = {}


def create_solana_wallet() -> Tuple[str, str]:
    """
        Generate a new Solana wallet.
        Returns:
            Tuple[str, str]: A tuple containing the public address and private key of the generated wallet.
        Raises:
            Exception: If there's an error during the wallet creation process.
    """
    try:
        # Генерация нового кошелька
        keypair = Keypair()
        # Получение публичного адреса кошелька
        wallet_address = str(keypair.pubkey())
        # Получение приватного ключа кошелька и преобразование в шестнадцатеричное представление
        private_key = keypair.secret().hex()

        # Возвращаем публичный адрес кошелька и приватный ключ кошелька как кортеж
        return wallet_address, private_key

    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        #logger.error(f"Failed to create Solana wallet: {e}\n{detailed_error_traceback}")
        # Поднятие нового исключения с подробной информацией
        raise Exception(f"Failed to create Solana wallet: {e}")

def get_wallet_address_from_private_key(private_key: str) -> str:
    """
        Gets the wallet address from the private key.

        Args:
            private_key (str): A string containing the presumed private key.

        Returns:
            str: The wallet address as a string.
    """
    # Создание объекта Keypair из закрытого ключа, преобразованного из шестнадцатеричной строки в байтовый формат.
    # Метод from_seed используется для создания ключевой пары на основе семени (seed), которое представляет собой
    # закрытый ключ в байтовом формате.
    # Мы используем метод bytes.fromhex для преобразования шестнадцатеричной строки в байтовый формат.
    keypair = Keypair.from_seed(bytes.fromhex(private_key))

    # Получение публичного адреса кошелька из объекта Keypair
    wallet_address = str(keypair.pubkey())

    # Возвращение адреса кошелька в виде строки
    return wallet_address


def is_valid_wallet_address(address: str) -> bool:
    """
        Checks whether the input string is a valid Solana wallet address.

        Args:
            address (str): A string containing the presumed wallet address.

        Returns:
            bool: True if the address is valid, False otherwise.
    """
    try:
        # Создание объекта PublicKey из строки адреса.
        # Метод from_string используется для создания объекта PublicKey из строки, содержащей адрес кошелька.
        # Этот метод позволяет создать объект PublicKey, который может быть использован для проверки подписей
        # или других операций, связанных с публичным ключом кошелька.
        Pubkey.from_string(address)

        # Если создание объекта PublicKey прошло успешно, значит адрес валиден
        return True
    except ValueError:
        # Если возникает ошибка, значит адрес невалиден, возвращаем False
        return False


def is_valid_private_key(private_key: str) -> bool:
    """
        Checks whether the input string is a valid Solana private key.

        Args:
            private_key (str): A string containing the presumed private key.

        Returns:
            bool: True if the private key is valid, False otherwise.
    """
    try:
        # Проверяем длину приватного ключа Solana
        # Если длина ключа 64 символа, это hex-представление
        if len(private_key) == PRIVATE_KEY_HEX_LENGTH:
            # Преобразование строки, содержащей приватный ключ, в байтовый формат с помощью метода fromhex,
            # а затем создание объекта Keypair из этих байтов.
            # Этот метод используется для создания объекта Keypair, который может быть использован для
            # подписывания транзакций или выполнения других операций, связанных с приватным ключом.
            Keypair.from_seed(bytes.fromhex(private_key))

        # Если длина ключа 32 символа, это представление в бинарном формате
        elif len(private_key) == PRIVATE_KEY_BINARY_LENGTH:
            # Преобразование строки, содержащей приватный ключ, в байтовый формат с помощью метода fromhex,
            # а затем создание объекта Keypair из этих байтов.
            # Этот метод используется для создания объекта Keypair из приватного ключа с использованием его seed.
            Keypair.from_seed(bytes.fromhex(private_key))
        else:
            # Если длина ключа не соответствует ожидаемой длине, возвращаем False
            return False
        # Если создание объекта Keypair прошло успешно, значит приватный ключ валиден
        return True
    except ValueError:
        # Если возникает ошибка, значит приватный ключ невалиден, возвращаем False
        return False


def is_valid_amount(amount: str | int | float) -> bool:
    """
        Checks if the value is a valid amount.

        Arguments:
        amount (str | int | float): The value of the amount to be checked.

        Returns:
        bool: True if the amount value is valid, False otherwise.
    """
    # Проверяем, является ли аргумент amount экземпляром int или float.
    if isinstance(amount, (int, float)):
        return True
        # Если amount не является int или float, пытаемся преобразовать его в float.
    try:
        float(amount)
        return True
    except ValueError:
        return False


def get_sol_balance(wallet_addresses:str):
    """
    Asynchronously retrieves the SOL balance for the specified wallet addresses.

    Args:
        wallet_addresses (Union[str, List[str]]): The wallet address or a list of wallet addresses.
        client: The Solana client.

    Returns:
        Union[float, List[float]]: The SOL balance or a list of SOL balances corresponding to the wallet addresses.
    """
    try:
        # Если передан одиночный адрес кошелька
        if isinstance(wallet_addresses, str):
            balance = (client.get_balance(Pubkey.from_string(wallet_addresses))).value
            # Преобразование лампортов в SOL
            sol_balance = balance / LAMPORT_TO_SOL_RATIO
            #logger.debug(f"wallet_address: {wallet_addresses}, balance: {balance}, sol_balance: {sol_balance}")
            return sol_balance
        # Если передан список адресов кошельков
        elif isinstance(wallet_addresses, list):
            sol_balances = []
            for address in wallet_addresses:
                balance = (client.get_balance(Pubkey.from_string(address))).value
                # Преобразование лампортов в SOL
                sol_balance = balance / LAMPORT_TO_SOL_RATIO
                sol_balances.append(sol_balance)
            return sol_balances
        else:
            raise ValueError("Invalid type for wallet_addresses. Expected str or list[str].")
    except Exception as error:
        detailed_error_traceback = traceback.format_exc()
        #logger.error(f"Failed to get Solana balance: {error}\n{detailed_error_traceback}")
        raise Exception(f"Failed to get Solana balance: {error}\n{detailed_error_traceback}")


def transfer_coins(sender_private_key: str, recipient_address: str, amount: float) -> bool:
    """
        function to transfer coins between wallets.

        Args:
            sender_address (str): Sender's address.
            sender_private_key (str): Sender's private key.
            recipient_address (str): Recipient's address.
            amount (float): Amount of tokens to transfer.

        Raises:
            ValueError: If any of the provided addresses is invalid or the private key is invalid.

        Returns:
            bool: True if the transfer is successful, False otherwise.
    """
    # Проверяем, является ли адрес отправителя действительным
    sender_address = get_wallet_address_from_private_key(private_key=sender_private_key)
    if not is_valid_wallet_address(sender_address):
        raise ValueError("Invalid sender address")

    # Проверяем, является ли адрес получателя действительным
    if not is_valid_wallet_address(recipient_address):
        raise ValueError("Invalid recipient address")

    # Проверяем, является ли приватный ключ отправителя действительным
    if not is_valid_private_key(sender_private_key):
        raise ValueError("Invalid sender private key")

    if not is_valid_amount(amount):
        raise ValueError("Invalid amount")

    # Создаем пару ключей отправителя из приватного ключа
    sender_keypair = Keypair.from_seed(bytes.fromhex(sender_private_key))

    # Создаем транзакцию для перевода монет
    txn = Transaction().add(
        transfer(
            TransferParams(
                from_pubkey=sender_keypair.pubkey(),
                to_pubkey=Pubkey.from_string(recipient_address),
                # Количество лампортов для перевода, преобразованное из суммы SOL.
                lamports=int(amount * LAMPORT_TO_SOL_RATIO),
            )
        )
    )
    # Отправляем транзакцию клиенту
    send_transaction_response = client.send_transaction(txn, sender_keypair)
    # Подтверждаем транзакцию
    confirm_transaction_response =  client.confirm_transaction(send_transaction_response.value)

    if hasattr(confirm_transaction_response, 'value') and confirm_transaction_response.value[0]:
        if hasattr(confirm_transaction_response.value[0], 'confirmation_status'):
            confirmation_status = confirm_transaction_response.value[0].confirmation_status
            if confirmation_status:
                #logger.debug(f"Transaction confirmation_status: {confirmation_status}")
                if confirmation_status in [TransactionConfirmationStatus.Confirmed,
                                           TransactionConfirmationStatus.Finalized]:
                    return True
    return False


def decode_solana_address(encoded_address: str) -> Optional[Any]:
    """
        Decodes a Solana address from Base58 format.

        Arguments:
        encoded_address (str): The encoded Solana address in Base58 format.

        Returns:
        str or None: The decoded Solana address as a string or None in case of error.
    """
    try:
        # Декодируем адрес из формата Base58
        decoded_bytes = base58.b58decode(encoded_address)
        # Преобразуем байтовые данные в строку
        decoded_address = decoded_bytes.decode('utf-8')
        return decoded_address
    except Exception as e:
        print(f"Failed to decode Solana address: {e}")
        return None


async def get_transaction_history(wallet_address: str) -> list[dict]:
    """
        Retrieves transaction history for a given Solana wallet address.

        Arguments:
        wallet_address (str): The Solana wallet address.

        Returns:
        list[dict]: A list of dictionaries representing transactions in JSON format.
    """
    try:
        # Проверяем, были ли уже получены данные для этого адреса кошелька и время их сохранения
        cached_data = transaction_history_cache.get(wallet_address)
        if cached_data is not None:
            transaction_history, cache_time = cached_data
            # Проверяем, не истекло ли время действия кеша
            if time.time() - cache_time <= TRANSACTION_HISTORY_CACHE_DURATION:
                # Возвращаем кэшированные данные
                return transaction_history

        # Получение истории транзакций кошелька
        transaction_history = []

        # Декодируем строку Base58 в байтовый формат
        pubkey_bytes = base58.b58decode(wallet_address)
        # Создаем объект Pubkey из байтового представления
        pubkey = Pubkey(pubkey_bytes)

        while True:
            try:
                # Получение истории транзакций для текущего адреса
                signature_statuses = (
                    await http_client.get_signatures_for_address(pubkey)
                ).value

                # Проходим по всем статусам подписей в результате
                for signature_status in signature_statuses:
                    # Получаем транзакцию по подписи
                    transaction = (await http_client.get_transaction(signature_status.signature)).value
                    # Добавляем полученную транзакцию в историю транзакций
                    transaction_history.append(transaction)

                # Кэшируем полученные данные для последующих запросов
                transaction_history_cache[wallet_address] = (transaction_history, time.time())

                # Возвращаем список истории транзакций
                return transaction_history

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    # Если получена ошибка "429 Too Many Requests", вернем None
                    return []
                else:
                    raise e

    except Exception as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(
            f"Failed to get transaction history for Solana wallet {wallet_address}: {e}\n{detailed_error_traceback}")
        return []

if __name__=='__main__':
    wallet_private_key = 'ddc3d3d2d3c7a2fdee21a41179d1261abacd83b6db35d9cc6268a675cc330261'
    address = (get_wallet_address_from_private_key(wallet_private_key))  # HS1WR95BrHq6CkM2gP299rwngcGNo5aLTAjgeGypyGPp

    helper = 'C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt'  # helper C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt

    print(get_sol_balance(address), get_sol_balance('C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt'))
    transfer_coins('ddc3d3d2d3c7a2fdee21a41179d1261abacd83b6db35d9cc6268a675cc330261',
                   'C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt', 0.0000001)
    print(get_sol_balance(address), get_sol_balance('C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt'))