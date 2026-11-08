import aiohttp
from config import settings

class BitsbyAPI:
    def __init__(self):
        self.api_token = settings.BITSBY_zxc_PROJECT_API_KEY
        self.project_id = settings.BITSBY_zxc_PROJECT_ID
        self.base_url = settings.BITSBY_BASE_URL

    async def create_invoice(self, amount: float, currency: str = "USD", description: str = "", service_data: str = ""):
        headers = {"Authorization": f"Token {self.api_token}"}

        data = {
            "projectId": self.project_id,
            "amountFiat": str(amount),
            "currencyFiat": currency,
            "timeToPay": "1",
        }
        if description:
            data["description"] = description
        if service_data:
            data["serviceData"] = service_data

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/invoices/create", data=data, headers=headers) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    print(f"❌ Ошибка API Bitsby ({response.status}): {await response.text()}")
                    return None