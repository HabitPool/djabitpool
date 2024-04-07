# solana_wallet_telegram_bot/config_data/config.py

from typing import Union

# Константа для определения URL-адреса узла Solana в тестовой сети Devnet
SOLANA_NODE_URL = "https://api.testnet.solana.com"
# SOLANA_NODE_URL = "https://api.devnet.solana.com"

# Константа для определения соотношения между лампортами и SOL. 1 SOL = 10^9 лампортов.
LAMPORT_TO_SOL_RATIO = 10 ** 9

# Константа для определения длины шестнадцатеричного представления приватного ключа в символах.
PRIVATE_KEY_HEX_LENGTH = 64

# Константа для определения длины двоичного представления приватного ключа в байтах.
PRIVATE_KEY_BINARY_LENGTH = 32

# Константа, определяющая длительность существования кеша для истории транзакций (в секундах).
# Здесь установлено значение 3600 секунд (1 час).
TRANSACTION_HISTORY_CACHE_DURATION = 3600

