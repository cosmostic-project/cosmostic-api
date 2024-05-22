from mojang import API, errors
from functools import lru_cache


class Mojang:
    def __init__(self):
        self.api = API()

    @lru_cache(maxsize=200)
    def get_uuid(self, username:str):
        """
        Get the UUID associated with a given username from the Mojang API.

        Parameters:
            username (str): The username to lookup the UUID for.

        Returns:
            str: The UUID associated with the username.
            None: If the username is not found.
        """
        try:
            uuid = self.api.get_uuid(username)
        except errors.NotFound:
            return None
        
        return uuid

    @lru_cache(maxsize=200)
    def get_username(self, uuid:str):
        """
        Get mojang username by uuid
        
        Parameters:
            uuid (str): The UUID to lookup the username for.
        
        Returns:
            str: The username associated with the UUID.
            None: If the UUID is not found.
        """
        try:
            username = self.api.get_username(uuid)
        except errors.NotFound:
            return None
        
        return username

    @lru_cache(maxsize=200)
    def get_profile(self, uuid:str):
        """
        Get mojang profile by uuid
        
        Parameters:
            uuid (str): The UUID to get the profile for.
        
        Returns:
            dict: The profile information including UUID, username, cape URL, and skin URL.
            None: If the profile is not found.
        """
        profile = self.api.get_profile(uuid)

        return None if not profile else {
            'uuid': profile.id,
            'username': profile.name,
            'cape_url': profile.cape_url,
            'skin_url': profile.skin_url
        }