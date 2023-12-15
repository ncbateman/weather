import os
import yaml

class Config:
    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Static access method to get the instance of the class.

        Args:
            testing (bool): If True, the testing configuration is loaded.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        Constructor for the Config class.

        Args:
            testing (bool): If True, the testing configuration is loaded.
        """
        if Config._instance is not None:
            raise Exception("This class is a singleton!")
        
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.app_config = {}
        self.users = {}

    def load_app_config(self, testing=False):
        """
        Load application configuration from a YAML file.

        Args:
            testing (bool): If True, the testing configuration is loaded.
        """
        config_filename = 'test-config.yaml' if testing else 'config.yaml'
        config_path = os.path.join(self.root_dir, 'config', config_filename)
        with open(config_path, 'r') as config_file:
            self.app_config = yaml.safe_load(config_file)

    def load_user_credentials(self):
        """
        Load user credentials from a YAML file.
        """
        users_config_path = os.path.join(self.root_dir, 'config', 'users.yaml')
        with open(users_config_path, 'r') as users_file:
            self.users = yaml.safe_load(users_file)

    def get_app_config(self):
        """
        Get the loaded application configuration.

        Returns:
            dict: The application configuration.
        """
        return self.app_config

    def get_user_credentials(self):
        """
        Get the loaded user credentials.

        Returns:
            dict: The user credentials.
        """
        return self.users
