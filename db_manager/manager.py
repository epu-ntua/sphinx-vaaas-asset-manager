from functools import partial

from Models.models import Asset
from utils.utils import get_main_logger
from mongoengine import connect
from config.config import get_config
from db_manager.assets_manager import _create_asset, _get_all_assets, _get_asset, _update_asset, _delete_asset, _search_asset, _get_asset_by_mac

l = get_main_logger('dm_manager')
c = get_config()


class Connection:
    def __enter__(self):
        try:
            self.conn = connect(db=c.get('db_name'), username=c.get('username'),
                                password=c.get('password'),
                                host=c.get('db_url') + ':' + c.get('db_port'),
                                retryWrites=False, alias='default')
            # l.debug(f'Connected to database{_get_db()}')
            return self.conn
        except Exception as e:
            l.exception(e.__str__())

    def __exit__(self, exc_type, exc_val, exc_tb):
        # l.debug('Closing DB connection')
        self.conn.close()

    @staticmethod
    def run_command(func):
        with Connection() as conn:
            return func()


class DBManager:
    def __init__(self):
        pass

    @staticmethod
    def create_asset(payload: dict):
        # return Connection.run_command_kwargs(_create_task, payload)
        return Connection.run_command(partial(_create_asset, payload))

    @staticmethod
    def get_all_assets():
        return Connection.run_command(_get_all_assets)

    @staticmethod
    def get_asset(asset_id: str):
        return Connection.run_command(partial(_get_asset, asset_id))

    @staticmethod
    def get_asset_by_mac(mac: str):
        return Connection.run_command(partial(_get_asset_by_mac, mac))

    @staticmethod
    def update_asset(asset_id: str, payload: dict):
        return Connection.run_command(partial(_update_asset, asset_id, payload))

    @staticmethod
    def delete_asset(asset_id: str):
        return Connection.run_command(partial(_delete_asset, asset_id))

    @staticmethod
    def search_asset(payload):
        return Connection.run_command(partial(_search_asset, payload))
