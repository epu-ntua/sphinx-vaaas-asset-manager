import json
from datetime import datetime
from typing import Optional

import pytz

from Models.models import Asset
from utils.utils import create_result, func_name, get_main_logger, dmsg

l = get_main_logger('assets_manager')


def _create_asset(payload) -> dict:
    print(payload)
    try:
        payload.pop('_id', None)
        # payload.pop('modified')
        result = Asset(**payload).save()
        return create_result(items=[result.to_json()], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def _get_all_assets() -> dict:
    try:
        result = Asset.objects()
        return create_result(items=[json.loads(i.to_json()) for i in result], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def _get_asset(asset_id: str) -> dict:
    try:
        assert asset_id, Exception('search string was either empty or null')
        result: Asset = Asset.objects.get(id=asset_id)
        return create_result(items=[json.loads(result.to_json())], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def _get_asset_by_mac(mac: str) -> Optional[Asset]:
    try:
        result: Asset = Asset.objects(mac=mac)
        return result
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return []


def _update_asset(asset_id: str, payload: dict) -> dict:
    try:
        # print(asset_id)
        # print(payload)
        # payload['modified'] = datetime.now(pytz.timezone('Europe/Athens'))
        print(payload)
        payload.pop('_id', None)
        payload.pop('created', None) if payload.get('created') else None
        payload['modified'] = datetime.now(pytz.timezone('Europe/Athens'))
        Asset.objects.get(id=asset_id).update(**payload)
        # payload.pop('created')
        # payload.pop('modified')
        return create_result(items=[json.loads(Asset.objects.get(id=asset_id).to_json())], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(dmsg('') + e.__str__())
        print(dmsg('') + e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def _delete_asset(asset_id: str) -> dict:
    try:
        result: Asset = Asset.objects.get(id=asset_id)
        result.delete()
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def _search_asset(payload):
    try:
        result: Asset = Asset.objects.get(**json.loads(payload))
        l.debug(dmsg('') + 'Got filtered Entity:' + str(result.id))
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        print(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)
