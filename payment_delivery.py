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

class GCashPayment(PaymentMethod):
    def __init__(self, amount: float, mobile_number: str):
        super().__init__(amount)
        self.__mobile_number = mobile_number

    def process_payment(self) -> bool:
        print(f"Processing GCash payment of ₱{self._amount:.2f} via {self.__mobile_number}...")
        return True

class CashOnDeliveryPayment(PaymentMethod):
    def process_payment(self) -> bool:
        print(f"Payment of ₱{self._amount:.2f} will be collected upon delivery (COD).")
        return True

class StandardDelivery(DeliveryService):
    def calculate_fee(self) -> float:
        return 50.00

class ExpressDelivery(DeliveryService):
    def calculate_fee(self) -> float:
        return 120.00
