"""Supplier information associated with products."""


class Supplier:
    """A supplier can exist independently and be referenced by many products."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = str(supplier_id).strip()
        self.__name: str = str(name).strip()
        self.__contact_email: str = str(contact_email).strip()

        if not self.__supplier_id:
            raise ValueError("Supplier ID cannot be empty.")
        if not self.__name:
            raise ValueError("Supplier name cannot be empty.")
        if not self.__contact_email:
            raise ValueError("Supplier contact email cannot be empty.")

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
            f"Email: {self.__contact_email}"
        )
