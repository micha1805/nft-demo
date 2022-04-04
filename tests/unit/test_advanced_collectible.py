import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import accounts, network
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # Deploy a contract, create an NFT, get a random breed back
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # ACT
    advanced_collectible, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # ASSERT
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
