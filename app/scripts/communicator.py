import requests

class Communicator:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False

    def get_data(self, url):
        """Get data from the specified URL."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def post_data(self, url, data):
        """Post JSON data to the specified URL."""
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
