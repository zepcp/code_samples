# Generic Tools

Setup
----------
Install Python [Libraries](https://pypi.org/)

    pip install -r requirements.txt

Usage
----------
Ethereum web3 manager

    from web3_manager import Web3Manager

    web3py = Web3Manager()
    web3py.to_wei(<amount>)
    web3py.to_checksum(<address>)
    web3py.get_sync_status()
    web3py.get_gas_price()
    web3py.get_balance(<address>)
    web3py.get_transaction(<txid>)
    web3py.get_receipt(<txid>)
    web3py.has_been_mined(<txid>)
    web3py.get_contract_instance(<address>, <abi>)
    web3py.call_function(<contract_instance>, <function>, <*arguments>)
    web3py.get_events_from_receipt(<contract_instance>, <event>, <receipt>)
    web3py.get_events(<contract_instance>, <event>, <from_block>, <to_block>)
    web3py.send_eth(<sender>, <private_key>, <receiver>, <amount_in_wei>)
    web3py.launch_function(<contract_instance>, <function>, <sender>, <private_key>, <*arguments>)
