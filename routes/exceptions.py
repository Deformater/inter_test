class AddressNotFound(Exception):
    def __init__(self, city: str, country: str, *args: object) -> None:
        self.city = city
        self.country = country
        super().__init__(args)

    def __str__(self) -> str:
        return f"Adress not found: {self.city}, {self.country}"


class ServiceUnavailable(Exception):
    def __init__(self, service_name: str, *args: object) -> None:
        self.service_name = service_name
        super().__init__(args)

    def __str__(self) -> str:
        return f"Service unavailable {self.service_name}"


class AllServicesUnavailable(Exception):
    def __init__(self, services_names: list[str], *args: object) -> None:
        self.service_name = services_names
        super().__init__(args)

    def __str__(self) -> str:
        return f"All services unavailable  {self.services_names}"
