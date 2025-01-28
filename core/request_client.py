import requests


class RequestSingleton:
    """
    Singleton class to manage all external service configurations.
    """
    _http_client = None

    @staticmethod
    def get_http_client():
        # Initialize the HTTP client if needed
        if RequestSingleton._http_client is None:
            RequestSingleton._http_client = requests
        return RequestSingleton._http_client

    @staticmethod
    def post(url, headers=None, data=None, json=None, timeout=10):
        """
        Wrapper for HTTP POST requests.
        """
        client = RequestSingleton.get_http_client()
        return client.post(url, headers=headers, data=data, json=json, timeout=timeout)

    @staticmethod
    def get(url, headers=None, data=None, json=None, timeout=10):
        """
        Wrapper for HTTP POST requests.
        """
        client = RequestSingleton.get_http_client()
        return client.get(url, headers=headers, data=data, json=json, timeout=timeout)


    @staticmethod
    def get_exceptions():
        """
        Expose the exceptions from the underlying HTTP client.
        """
        return requests.exceptions
