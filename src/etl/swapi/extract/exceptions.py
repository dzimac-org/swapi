class SWAPIClientError(Exception):
    pass


class SWAPIConnectionError(Exception):
    pass


class SWAPIResponseStatusError(SWAPIClientError):
    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f"Couldn't fetch data, response status code: {status_code}")


class SWAPIResponseDataError(SWAPIClientError):
    pass
