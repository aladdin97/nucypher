"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""


import pytest
from web3.contract import Contract


ALGORITHM_SHA256 = 1
BASE_PENALTY = 100
PENALTY_HISTORY_COEFFICIENT = 10
PERCENTAGE_PENALTY_COEFFICIENT = 8
REWARD_COEFFICIENT = 2

secret = (123456).to_bytes(32, byteorder='big')


@pytest.fixture()
def escrow(testerchain):
    escrow, _ = testerchain.interface.deploy_contract('MinersEscrowForMiningAdjudicatorMock')
    return escrow


@pytest.fixture(params=[False, True])
def adjudicator_contract(testerchain, escrow, request):
    contract, _ = testerchain.interface.deploy_contract(
        'MiningAdjudicator',
        escrow.address,
        ALGORITHM_SHA256,
        BASE_PENALTY,
        PENALTY_HISTORY_COEFFICIENT,
        PERCENTAGE_PENALTY_COEFFICIENT,
        REWARD_COEFFICIENT)

    if request.param:
        secret_hash = testerchain.interface.w3.keccak(secret)
        dispatcher, _ = testerchain.interface.deploy_contract('Dispatcher', contract.address, secret_hash)

        # Deploy second version of the government contract
        contract = testerchain.interface.w3.eth.contract(
            abi=contract.abi,
            address=dispatcher.address,
            ContractFactoryClass=Contract)

    return contract
