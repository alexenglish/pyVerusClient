#!/usr/bin/env python3
import json
import requests

class VerusResponseData:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.response = None

    def __repr__(self):
        contents = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({contents})"

class VerusClient:
    def __init__(self, host='127.0.0.1', network='mainnet', rpc_user='username', rpc_password='password'):
        """ Initialize the client. host: hostname where the daemon is running.
        network: 'mainnet' or 'testnet'
        rpc_user and rpc_password: credentials for RPC access.
        """
        
        self.host = host
        self.network = network.lower()
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

        if self.network == 'mainnet':
            self.port = 27486
            self.native_currency = 'vrsc'
        elif self.network == 'testnet':
            self.port = 18843
            self.native_currency = 'vrsctest'
        else:
            raise ValueError("Network must be 'mainnet' or 'testnet'")

        self.url = f"http://{self.host}:{self.port}/"

    def _rpc_request(self, method, params):
        """
        Internal method to send an RPC request.
        """
        payload = {
            "jsonrpc": "1.0",
            "id": "python-client",
            "method": method,
            "params": params
        }
        headers = {"content-type": "text/plain"}
        response = requests.post(
            self.url,
            auth=(self.rpc_user, self.rpc_password),
            data=json.dumps(payload),
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        if result.get("error") is not None:
            raise Exception(f"RPC Error: {result['error']}")
        return result

    def _handle_response(self, response):
        """
        Process the JSON RPC response
        """
        res = response.get("result")
        if isinstance(res, dict):
            #res['response'] = res
            data = VerusResponseData(**res)
            data.response = res
            return data
        else:
            return res

    #RPC Calls

    def getinfo(self):
        """
        Returns an object containing various state info.
        """
        response = self._rpc_request("getinfo", [])
        return self._handle_response(response)

    def getwalletinfo(self):
        """
        Returns an object containing wallet information.
        """
        response = self._rpc_request("getwalletinfo", [])
        return self._handle_response(response)

    def help(self, command=None):
        """
        Returns help text for all commands or a specified command.
        """
        params = [command] if command is not None else []
        response = self._rpc_request("help", params)
        return self._handle_response(response)

    def stop(self):
        """
        Stops the Verus daemon.
        """
        response = self._rpc_request("stop", [])
        return self._handle_response(response)

    def getnewaddress(self):
        """
        Returns a new address from the keypool and marks it as used.
        """
        response = self._rpc_request("getnewaddress", [])
        return self._handle_response(response)

    def validateaddress(self, address):
        """
        Returns a new address from the keypool and marks it as used.
        """
        response = self._rpc_request("validateaddress", [address])
        return self._handle_response(response)


#    def getaddressbalance(self, addresses):
#        """
#        Returns the balance for one or more addresses.
#        addresses: list of base58check encoded addresses.
#        """
#        params = [{"addresses": addresses}]
#        response = self._rpc_request("getaddressbalance", params)
#        return self._handle_response(response)
#
#    def getaddressdeltas(self, addresses, start=None, end=None, chainInfo=False, friendlynames=False, verbosity=0):
#        """
#        Returns all changes (deltas) for an address.
#        """
#        param = {"addresses": addresses, "chainInfo": chainInfo, "friendlynames": friendlynames, "verbosity": verbosity}
#        if start is not None:
#            param["start"] = start
#        if end is not None:
#            param["end"] = end
#        response = self._rpc_request("getaddressdeltas", [param])
#        return self._handle_response(response)
#
#    def getaddressmempool(self, addresses, friendlynames=False, verbosity=0):
#        """
#        Returns all mempool deltas for an address.
#        """
#        param = {"addresses": addresses, "friendlynames": friendlynames, "verbosity": verbosity}
#        response = self._rpc_request("getaddressmempool", [param])
#        return self._handle_response(response)
#
#    def getaddresstxids(self, addresses, start=None, end=None):
#        """
#        Returns the transaction IDs for one or more addresses.
#        """
#        param = {"addresses": addresses}
#        if start is not None:
#            param["start"] = start
#        if end is not None:
#            param["end"] = end
#        response = self._rpc_request("getaddresstxids", [param])
#        return self._handle_response(response)
#
#    def getaddressutxos(self, addresses, chainInfo=False, friendlynames=False, verbosity=0):
#        """
#        Returns all unspent outputs (UTXOs) for an address.
#        """
#        param = {"addresses": addresses, "chainInfo": chainInfo, "friendlynames": friendlynames, "verbosity": verbosity}
#        response = self._rpc_request("getaddressutxos", [param])
#        return self._handle_response(response)
#
#    def getsnapshot(self, top=None):
#        """
#        Returns a snapshot of (address, amount) pairs.
#        """
#        params = [top] if top is not None else []
#        response = self._rpc_request("getsnapshot", params)
#        return self._handle_response(response)
#
#    # BLOCKCHAIN calls
#
#    def coinsupply(self, height=None):
#        """
#        Returns coin supply information at a given block height.
#        """
#        params = [height] if height is not None else []
#        response = self._rpc_request("coinsupply", params)
#        return self._handle_response(response)
#
    def getbestblockhash(self):
        """
        Returns the hash of the best (tip) block in the longest chain.
        """
        response = self._rpc_request("getbestblockhash", [])
        return self._handle_response(response)

    def getblock(self, hash_or_height, verbosity=1):
        """
        Returns block data.
        - If verbosity=0, returns hex-encoded block data.
        - If verbosity=1, returns a JSON object.
        - If verbosity=2, includes detailed transaction data.
        """
        response = self._rpc_request("getblock", [hash_or_height, verbosity])
        return self._handle_response(response)

#    def getblockchaininfo(self):
#        """
#        Returns an object containing various state info regarding blockchain processing.
#        """
#        response = self._rpc_request("getblockchaininfo", [])
#        return self._handle_response(response)
#
    def getblockcount(self):
        """
        Returns the number of blocks in the best valid chain.
        """
        response = self._rpc_request("getblockcount", [])
        return self._handle_response(response)

#    def getblockdeltas(self, blockhash):
#        """
#        Returns detailed information (deltas) about a given block.
#        """
#        response = self._rpc_request("getblockdeltas", [blockhash])
#        return self._handle_response(response)
#
    def getblockhash(self, index):
        """
        Returns the hash of the block at the given index.
        """
        response = self._rpc_request("getblockhash", [index])
        return self._handle_response(response)

#    def getblockhashes(self, high, low, options=None):
#        """
#        Returns an array of block hashes within the given timestamp range.
#        """
#        if options is None:
#            options = {"noOrphans": True, "logicalTimes": True}
#        response = self._rpc_request("getblockhashes", [high, low, options])
#        return self._handle_response(response)
#
#    def getblockheader(self, blockhash, verbose=True):
#        """
#        Returns information about a block header.
#        """
#        response = self._rpc_request("getblockheader", [blockhash, verbose])
#        return self._handle_response(response)
#
#    def getchaintips(self):
#        """
#        Returns information about all known tips in the block tree.
#        """
#        response = self._rpc_request("getchaintips", [])
#        return self._handle_response(response)
#
#    def getchaintxstats(self, nblocks=None, blockhash=None):
#        """
#        Computes statistics about the total number and rate of transactions in the chain.
#        """
#        params = []
#        if nblocks is not None:
#            params.append(nblocks)
#        if blockhash is not None:
#            params.append(blockhash)
#        response = self._rpc_request("getchaintxstats", params)
#        return self._handle_response(response)
#
#    def getdifficulty(self):
#        """
#        Returns the proof-of-work difficulty as a multiple of the minimum.
#        """
#        response = self._rpc_request("getdifficulty", [])
#        return self._handle_response(response)
#
#    def getmempoolinfo(self):
#        """
#        Returns details on the current state of the transaction memory pool.
#        """
#        response = self._rpc_request("getmempoolinfo", [])
#        return self._handle_response(response)
#
#    def getrawmempool(self, verbose=False):
#        """
#        Returns all transaction IDs in the memory pool.
#        If verbose is True, returns a JSON object with detailed info.
#        """
#        response = self._rpc_request("getrawmempool", [verbose])
#        return self._handle_response(response)
#
#    def getspentinfo(self, txid, index):
#        """
#        Returns the transaction ID and index where an output is spent.
#        """
#        response = self._rpc_request("getspentinfo", [{"txid": txid, "index": index}])
#        return self._handle_response(response)
#
#    def gettxout(self, txid, n, includemempool=False):
#        """
#        Returns details about an unspent transaction output.
#        """
#        response = self._rpc_request("gettxout", [txid, n, includemempool])
#        return self._handle_response(response)
#
#    def gettxoutproof(self, txids, blockhash=None):
#        """
#        Returns a hex-encoded proof that the specified transaction(s) were included in a block.
#        """
#        params = [txids] if blockhash is None else [txids, blockhash]
#        response = self._rpc_request("gettxoutproof", params)
#        return self._handle_response(response)
#
#    def gettxoutsetinfo(self):
#        """
#        Returns statistics about the UTXO set.
#        """
#        response = self._rpc_request("gettxoutsetinfo", [])
#        return self._handle_response(response)
#
#    # KV calls
#
#    def kvsearch(self, key):
#        """
#        Searches for a key stored via the kvupdate command.
#        """
#        response = self._rpc_request("kvsearch", [key])
#        return self._handle_response(response)
#
#    def kvupdate(self, key, value, days, passphrase=None):
#        """
#        Stores a key/value pair.
#        """
#        params = [key, value, days]
#        if passphrase is not None:
#            params.append(passphrase)
#        response = self._rpc_request("kvupdate", params)
#        return self._handle_response(response)
#
#    # Control / Daemon calls
#
#    def processupgradedata(self, upgradedata):
#        """
#        Processes upgrade data.
#        upgradedata: a dictionary containing keys such as upgradeid, minimumdaemonversion,
#                    activationheight, and activationtime.
#        """
#        response = self._rpc_request("processupgradedata", [upgradedata])
#        return self._handle_response(response)
#
#    def verifychain(self, checklevel=3, numblocks=288):
#        """
#        Verifies the blockchain database.
#        """
#        response = self._rpc_request("verifychain", [checklevel, numblocks])
#        return self._handle_response(response)
#
#    def verifytxoutproof(self, proof):
#        """
#        Verifies that a txoutproof points to a transaction in a block.
#        """
#        response = self._rpc_request("verifytxoutproof", [proof])
#        return self._handle_response(response)
#
#    def z_gettreestate(self, hash_or_height):
#        """
#        Returns information about the tree state for the given block.
#        """
#        response = self._rpc_request("z_gettreestate", [hash_or_height])
#        return self._handle_response(response)
#

#    # Generating / Mining calls
#
#    def generate(self, numblocks):
#        """
#        Mines blocks immediately (only available on regtest).
#        """
#        response = self._rpc_request("generate", [numblocks])
#        return self._handle_response(response)
#
    def getgenerate(self):
        """
        Returns whether the daemon is set to mine/mint coins.
        """
        response = self._rpc_request("getgenerate", [])
        return self._handle_response(response)

    def setgenerate(self, generate, genproclimit=None):
        """
        Sets mining/minting on or off.
        generate: boolean; genproclimit: number of processor threads (or 0 for staking).
        """
        params = [generate]
        if genproclimit is not None:
            params.append(genproclimit)
        response = self._rpc_request("setgenerate", params)
        return self._handle_response(response)

    def getmininginfo(self):
        """
        Returns whether the daemon is set to mine/mint coins.
        """
        response = self._rpc_request("getmininginfo", [])
        return self._handle_response(response)

#    # CROSSCHAIN calls
#
#    def MoMoMdata(self, symbol, kmdheight, ccid):
#        """
#        Returns MoMoM data.
#        """
#        response = self._rpc_request("MoMoMdata", [symbol, kmdheight, ccid])
#        return self._handle_response(response)
#
#    def assetchainproof(self, txid):
#        """
#        Returns an assetchain proof for the given transaction ID.
#        """
#        response = self._rpc_request("assetchainproof", [txid])
#        return self._handle_response(response)
#
#    def calc_MoM(self, height, MoMdepth):
#        """
#        Calculates MoM (Merkle of Merkle) data.
#        """
#        response = self._rpc_request("calc_MoM", [height, MoMdepth])
#        return self._handle_response(response)
#
#    def getNotarisationsForBlock(self, blockHash):
#        """
#        Returns notarisation transactions for the given block.
#        """
#        response = self._rpc_request("getNotarisationsForBlock", [blockHash])
#        return self._handle_response(response)
#
#    def height_MoM(self, height):
#        """
#        Returns height-specific MoM data.
#        """
#        response = self._rpc_request("height_MoM", [height])
#        return self._handle_response(response)
#
#    def migrate_completeimporttransaction(self, importTx):
#        """
#        Processes a cross-chain import transaction.
#        """
#        response = self._rpc_request("migrate_completeimporttransaction", [importTx])
#        return self._handle_response(response)
#
#    def migrate_converttoexport(self, rawTx, dest_symbol, export_amount):
#        """
#        Converts a raw transaction to a cross-chain export.
#        """
#        response = self._rpc_request("migrate_converttoexport", [rawTx, dest_symbol, export_amount])
#        return self._handle_response(response)
#
#    def migrate_createimporttransaction(self, burnTx, payouts):
#        """
#        Creates an import transaction from a burn transaction and payouts.
#        """
#        response = self._rpc_request("migrate_createimporttransaction", [burnTx, payouts])
#        return self._handle_response(response)
#
#    def scanNotarisationsDB(self, blockHeight, symbol, blocksLimit=1440):
#        """
#        Scans the notarisations database for a given symbol starting at a block height.
#        """
#        response = self._rpc_request("scanNotarisationsDB", [blockHeight, symbol, blocksLimit])
#        return self._handle_response(response)
#
#    def z_getpaymentdisclosure(self, txid, js_index, output_index, message=None):
#        """
#        Generates a payment disclosure for a given joinsplit output.
#        """
#        params = [txid, js_index, output_index]
#        if message is not None:
#            params.append(message)
#        response = self._rpc_request("z_getpaymentdisclosure", params)
#        return self._handle_response(response)
#
#    def z_validatepaymentdisclosure(self, paymentdisclosure):
#        """
#        Validates a payment disclosure.
#        """
#        response = self._rpc_request("z_validatepaymentdisclosure", [paymentdisclosure])
#        return self._handle_response(response)
#
#    # ADDITIONAL CALLS
#
    def estimateconversion(self, amount, from_currency, to_currency, via=None):
        param_obj = {
            "currency": from_currency,
            "convertto": to_currency,
            "amount": amount
        }

        if via:
            param_obj["via"] = via

        # Now pass a single dict (which _rpc_request will encode as JSON)
        response = self._rpc_request("estimateconversion", [param_obj])
        return self._handle_response(response)

    def getcurrency(self, currency):
        """
        Returns details for a specified currency.
        """
        response = self._rpc_request("getcurrency", [currency])
        return self._handle_response(response)

    def getcurrencystate(self, currency, n=None, conversiondatacurrency=None):
        """
        Returns the state of the specified currency.
        Parameters:
        currency: currency name or ID.
        n: (optional) an additional numeric parameter.
        connectedchainid: (optional) the connected chain ID.
        """
        params = [currency]
        if n is not None:
            params.append(n)
        else:
            params.append("")

        if conversiondatacurrency is not None:
            params.append(conversiondatacurrency)

        response = self._rpc_request("getcurrencystate", params)
        return self._handle_response(response)

#    def getcurrencyconverters(self):
#TODO: add overloaded options
#        """
#        Returns a list of available currency converters.
#        """
#        response = self._rpc_request("getcurrencyconverters", [])
#        return self._handle_response(response)

    def getimports(self, currency, heightstart=None, heightend=None):
        """
        Returns a list of import transactions.
        Parameters:
        currency: the chain or currency name for which to fetch the exports
        startheight: (optional) return imports above this block height
        endheight: (optional) return imports below this block height
        """
        params = [currency]
        if heightstart is not None:
            params.append(heightstart)
        else:
            params.append("")

        if heightend is not None:
                params.append(heightend)

        response = self._rpc_request("getimports", [currency])
        return self._handle_response(response)

    def getexports(self, curency, heightstart=None, heightend=None):
        """
        Returns a list of export transactions.
        Parameters:
        currency: the chain or currency name for which to fetch the imports
        startheight: (optional) return exports above this block height
        endheight: (optional) return exports below this block height
        """

        params = [currency]
        if heightstart is not None:
            params.append(heightstart)
        else:
            params.append("")

        if heightend is not None:
                params.append(heightend)

        response = self._rpc_request("getexports", [])
        return self._handle_response(response)

#    def listtransactions(self, count=10, skip=0):
#        """
#        Returns a list of transactions.
#        Parameters:
#        count: number of transactions to return.
#        skip: number of transactions to skip.
#        """
#        response = self._rpc_request("listtransactions", [count, skip])
#        return self._handle_response(response)
#
    def getrawtransaction(self, txid, verbose=True):
        """
        Returns the raw transaction data for the given transaction ID.
        Parameters:
        txid: the transaction ID.
        verbose: if True, returns a JSON object; if False, returns raw hex.
        """

        verbose_flag = 1 if verbose else "" 

        response = self._rpc_request("getrawtransaction", [txid, verbose_flag])
        return self._handle_response(response)

    def getidentity(self, identity):
        """
        Returns details for a specified identity.
	Parameters:
        identity: name (@-terminated) or i-address)
        """

        response = self._rpc_request("getidentity", [identity])
        return self._handle_response(response)

#    def updateidentity(self, identityid, new_data):
#        """
#        Updates an identity with new data.
#        new_data: a dictionary containing the fields to update.
#        """
#        response = self._rpc_request("updateidentity", [identityid, new_data])
#        return self._handle_response(response)
#
#    def registeridentity(self, identity_data):
#        """
#        Registers a new identity.
#        identity_data: a dictionary containing identity details.
#        """
#        response = self._rpc_request("registeridentity", [identity_data])
#        return self._handle_response(response)
#
#    def registernamecommitment(self, name, commitment):
#        """
#        Registers a name commitment.
#        """
#        response = self._rpc_request("registernamecommitment", [name, commitment])
#        return self._handle_response(response)
#
#    def revokeidentity(self, identityid):
#        """
#        Revokes the specified identity.
#        """
#        response = self._rpc_request("revokeidentity", [identityid])
#        return self._handle_response(response)
#
#    def recoveridentity(self, identityid, recovery_data):
#        """
#        Recovers an identity using provided recovery data.
#        recovery_data: a dictionary containing necessary recovery parameters.
#        """
#        response = self._rpc_request("recoveridentity", [identityid, recovery_data])
#        return self._handle_response(response)
#
#    def setidentitytimelock(self, identityid, timelock):
#        """
#        Sets a timelock for the specified identity.
#        """
#        response = self._rpc_request("setidentitytimelock", [identityid, timelock])
#        return self._handle_response(response)
#
#    def makeoffer(self, offer_data):
#        """
#        Creates a new offer.
#        offer_data: a dictionary containing offer details.
#        """
#        response = self._rpc_request("makeoffer", [offer_data])
#        return self._handle_response(response)
#
#    def takeoffer(self, offerid, offer_data):
#        """
#        Accepts an existing offer.
#        Parameters:
#        offerid: the identifier of the offer.
#        offer_data: a dictionary containing any required details.
#        """
#        response = self._rpc_request("takeoffer", [offerid, offer_data])
#        return self._handle_response(response)
#
#    def getoffers(self):
#        """
#        Returns a list of current offers.
#        """
#        response = self._rpc_request("getoffers", [])
#        return self._handle_response(response)
#
#    def closeoffers(self, offerid):
#        """
#        Closes the offer with the specified offer ID.
#        """
#        response = self._rpc_request("closeoffers", [offerid])
#        return self._handle_response(response)
#
#    def sendcurrency(self, fromaddress, currency, amount, toaddress, extra_params=None):
#        """
#        Sends currency from the wallet to a specified address.
#        Parameters:
#        currency: the currency name or ID.
#        amount: the amount to send.
#        toaddress: the destination address.
#        extra_params: (optional) a dictionary of additional parameters.
#        """
#
#        params = [currency, amount, toaddress]
#        if extra_params is not None:
#            params.append(extra_params)
#        response = self._rpc_request("sendcurrency", params)
#        return self._handle_response(response)
