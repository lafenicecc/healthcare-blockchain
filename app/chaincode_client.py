from hyperledger.client import Client
from config import fabric_url, chaincode_name

CHAINCODE_LANG_GO = 1
CHAINCODE_LANG_NODE = 2
CHAINCODE_CONFIDENTIAL_PUB = 0
CHAINCODE_CONFIDENTIAL_CON = 1
DEFAULT_CHAINCODE_CONFIDENTIALITY = 0


class ChaincodeClient(object):
    def __init__(self, fabric_url, chaincode_name=""):
        self.fabric_url = fabric_url
        self.client = Client(base_url=fabric_url)
        self.chaincode_name = chaincode_name
        self.chaincode_type = CHAINCODE_LANG_GO

    def set_chaincode_name(self, chaincode_name):
        self.chaincode_name = chaincode_name

    def deploy(self, chaincode_path,
               function,
               args,
               type=CHAINCODE_LANG_GO):
        try:
            resp = self.client.chaincode_deploy(
                chaincode_path=chaincode_path,
                function=function,
                args=args,
                type=type,
            )
            if resp['result']['status'] != 'OK':
                raise
            self.set_chaincode_name(resp['result']['message'])
            self.chaincode_type = type
            return True

        except Exception as e:
            print(e)
            return False

    def invoke(self, function, args):
        try:
            resp = self.client.chaincode_invoke(
                chaincode_name=self.chaincode_name,
                function=function,
                args=args
            )
            if resp['result']['status'] != 'OK':
                raise
            return True

        except Exception as e:
            print(e)
            return False


    def query(self, function, args):
        try:
            resp = self.client.chaincode_query(
                chaincode_name=self.chaincode_name,
                function=function,
                args=args
            )
            if resp['result']['status'] != 'OK':
                raise
            return resp['result']['message']

        except Exception as e:
            print(e)
            return None


CC = ChaincodeClient(fabric_url, chaincode_name)
