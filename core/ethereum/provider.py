from web3 import Web3, HTTPProvider

import os

class ProviderWarpper:
    def __init__(self, conf: dict) -> None:
        
        self.description = conf.get("description", "-")
        self.endpoint_uri = conf.get("endpoint") \
            .replace("$ALCHEMY_API_KEY", os.getenv("ALCHEMY_API_KEY"))

        self.rpc: Web3 = Web3(HTTPProvider(
            endpoint_uri=self.endpoint_uri, request_kwargs={"timeout": 60}))
        
        self.chain_id = self.rpc.eth.chain_id # remote chain id
        
        self.name = conf.get("name", conf.get(
            "chain_id", "evm_chain-{}".format(self.chain_id)))
        
        assert self.chain_id == conf.get("chain_id"), \
            "chain id not match, remote: {}, config: {}".format(self.chain_id, conf.get("chain_id"))


class Web3RPCProvider(object):
    def __init__(self, network_conf: dict) -> None:
        self.Rpcs = dict()
        assert "networks" in network_conf, \
            "network config error, missing value `networks`"
            
        for conf in network_conf.get("networks", []):
            p = ProviderWarpper(conf)
            self.Rpcs[p.name] = p
            



if __name__ == "__main__":
    import json
    import dotenv
    dotenv.load_dotenv(".env", verbose=True)
    rpcs = Web3RPCProvider(json.load(open("configs/networks.json", "r")))
    for rpc_name, rpc in rpcs.Rpcs.items():
        print(rpc.name, rpc.chain_id, rpc.endpoint_uri)