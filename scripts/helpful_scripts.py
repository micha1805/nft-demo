from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "ganache",
    "mainnet-fork",
    "mainnet-fork-dev",
    "development",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mocks = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config if defined,
    otherwise it will deploy a mock version of that contract and return
    that mock contract.

        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract : the most recently deployed version of this contract
    """

    # the contract_name variable needs to match a key of the dictionary contract_to_mocks
    contract_type = contract_to_mocks[contract_name]

    # development context :
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # verifier si ce contrat est déjà déployé
        if len(contract_type) <= 0:  # exemple : MockV3Aggregator.length <= 0
            deploy_mocks()
        contract = contract_type[-1]
    # live context :
    else:
        # exemple : config["networks"][mainnet-fork-dev][eth_usd_price_feed]
        contract_address = config["networks"][network.show_active()][contract_name]
        # we need the address and the abi of the contract
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # exemple : contract_type = MockV3Aggregator
        # on aurait donc ceci :
        # contract = Contract.from_abi(
        #     MockV3Aggregator._name, contract_address, MockV3Aggregator.abi
        # )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=18, initial_value=2000):
    account = get_account()
    print(f"The current network is {network.show_active()}")

    print("Deploying mocks...")

    # mock link token
    print("Deploying Mock Link token")
    link_token = LinkToken.deploy({"from": account})
    print(f"Mock Link token deployed at {link_token.address}\n")

    # # mock v3Aggregator
    # print("Deploying Mock V3Aggregator")
    # mockv3_aggregator = MockV3Aggregator.deploy(
    #     decimals, initial_value, {"from": account}
    # )
    # print(f"MockV3Aggregator deployed at {mockv3_aggregator.address}\n")

    # mock vrf coordinator
    print("Deploying Mock VRF Coordinator")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"Mock VRFCoordinator deployed at {vrf_coordinator.address}\n")
    print("Mocks deployed!")


# For the following function the amount is 0.1 by defaut
# so 100_000_000_000_000_000 in 18 decimals Solidity representation
def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount_in_wei=Web3.toWei(1, "ether"),
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount_in_wei, {"from": account})
    tx.wait(1)
    print(f"Fund contract at : {contract_address}")
    return tx
