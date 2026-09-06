from abc import ABC, abstractmethod
import random

class PaymentMethod(ABC):
    def __init__(self, amount: float):
        self._amount = amount

    @abstractmethod
    def process_payment(self) -> bool:
        pass

class DeliveryService(ABC):
    def __init__(self, address: str):
        self._address = address
        self._tracking_number = f"TRK-{random.randint(10000, 99999)}"
        self._status = "Pending"

    @abstractmethod
    def calculate_fee(self) -> float:
        pass

    def update_status(self, new_status: str):
        self._status = new_status
        print(f"Delivery Status Updated: {self._status}")

    def track_order(self):
        print(f"Tracking Number: {self._tracking_number} | Status: {self._status} | Destination: {self._address}")
