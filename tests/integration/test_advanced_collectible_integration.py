import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import accounts, network
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_can_create_advanced_collectible_integration():
    # Deploy a contract, create an NFT, get a random breed back
    # ARRANGE
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for live testing (integration)")
    # ACT
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(180)
    # ASSERT
    assert advanced_collectible.tokenCounter() == 1
