# pyVerusClient
Python class for interacting with verusd

RPC commands that have not been tested yet are commented out, they were roughed/stubbed out, but many that haven't gotten attention yet won't work. PRs welcome for tested/fixed calls.

Call an RPC command as a method on an instantiation of the class. The object returned is either a single value or an object with accessor methods for the values returned.

## Example usage
```python
from verus_client import VerusClient

verus = VerusClient(network="testnet",rpc_user="username_from_conf_file",rpc_password="password_from_conf_file")

verus.getinfo()
```
