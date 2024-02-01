from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

# Determine the environment
# Default to local unless specified otherwise
is_production = os.getenv('PRODUCTION_MODE', 'False').lower() in ('true', '1', 't')

# Load the appropriate .env file based on the environment
env_file = '.env.production' if is_production else '.env.local'
load_dotenv(dotenv_path=env_file)

# You can also define some utility functions to access the environment variables more easily
def get_env_variable(var_name, default=None):
    return os.getenv(var_name, default)
