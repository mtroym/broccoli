from web3.contract.contract import Contract

def make_contract(contract_conf: dict):
    if "network" not in contract_conf or \
        "contract_address" not in contract_conf or \
        "abis" not in contract_conf:
        raise ValueError("contract config not complete")
    
    return 


class ContractWarpper(object):
    def __init__(self, contract_conf: dict) -> None:
        self.network, self.contract_address, self.abis = \
            make_contract(contract_conf=contract_conf)
        
        self.contract = Contract(address=self.contract_address, abis=self.abis)
