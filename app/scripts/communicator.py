import requests

class Communicator:
    def __init__(self):
        # Initialize session, set base URL or headers if needed
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL certificate verification

    def get_data(self, url):
        """Get data from the specified URL."""
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def post_data(self, url, data):
        """Post JSON data to the specified URL."""
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
