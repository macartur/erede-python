import httpx
import erede

from erede.Transaction import Transaction
from erede.RedeError import RedeError


class TransactionService:
    GET = "get"
    POST = "post"
    PUT = "put"

    def __init__(self, store):
        """

        :type store: `erede.Store.Store`
        """
        self.store = store

    async def execute(self):
        raise NotImplementedError("Not implemented")

    def get_uri(self):
        return "{}/transactions".format(self.store.environment.endpoint)

    async def send_request(self, method, body=None):
        user_agent = "{} Store/{}".format(erede.eRede.USER_AGENT,
                                          self.store.filliation)

        headers = {'User-Agent': user_agent,
                   "Accept": "application/json",
                   "Content-Type": "application/json"}

        client = httpx.AsyncClient()
        auth = (self.store.filliation, self.store.token)
        response = await getattr(client, method)(self.get_uri(),
                                                 auth=auth,
                                                 data=body,
                                                 headers=headers)
        if response.status_code >= 400:
            error = response.json()
            raise RedeError(error.get("returnMessage", "opz"),
                            error.get("returnCode", 0))
        return Transaction.unserialize(response.json())
