from datetime import datetime
import pytz
from sanic import Sanic, Request
from sanic.response import json as sanic_json
from utils.utils import get_main_logger
import json
from db_manager.manager import DBManager
from job_scheduler.job_manager import setup_scheduler, add_job

app = Sanic('__name__')

log = get_main_logger(__name__)
manager = DBManager()
sc = setup_scheduler()
sc.start()


def setup_module():
    from ip_scanner.scanner import start_network_scan
    scan_all_params = {'id': 'scan_all_networks', 'replace_existing': True, 'trigger': 'cron', 'day': '*', 'hour': 1, 'minute': 0}
    add_job(scheduler=sc, function=start_network_scan, function_params=None, **scan_all_params)


@app.route("/")
async def home(request):
    log.info('Here is your log')
    return sanic_json({"message": "hello_world"}, status=200)


@app.get('/health')
async def health(request):
    return sanic_json({'result': 'This is the asset manager component'}, status=200)


@app.route("/assets", methods=['GET', 'POST', 'OPTIONS'])
async def entities(request):
    if request.method == 'GET':
        response = manager.get_all_assets()  # TODO add URL arguments to getAllEntities function call
        return sanic_json(response, status=200)
    elif request.method == 'POST':
        payload = json.loads(request.body)
        response = manager.create_asset(payload)
        return sanic_json(response, status=200)
    else:
        return sanic_json({"message": "method is not implemented"}, status=501)


@app.route("/assets/<asset_id>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
async def entitiesUpdate(request: Request, asset_id):
    if request.method == 'GET':
        response = manager.get_asset(asset_id)
        return sanic_json(response, status=200)
    elif request.method == 'PUT':
        payload = json.loads(request.body)
        # print(payload)
        response = manager.update_asset(asset_id=asset_id, payload=payload)
        return sanic_json(response, status=200)
    elif request.method == 'DELETE':
        response = manager.delete_asset(asset_id)
        return sanic_json(response, status=200)
    else:
        return sanic_json({"message": "method is not implemented"}, status=501)


@app.route("/assets/search", methods=['POST', 'OPTIONS'])
async def search_entities(request):
    payload = request.body
    # print(payload)
    response = manager.search_asset(payload)
    return sanic_json({"message": response}, status=200)


@app.get("/assets/scan")
async def scan(request):
    from ip_scanner.scanner import start_network_scan
    log.info('Starting network scan...')
    # Thread(target=tools['scan'].scan_all).start()
    add_job(scheduler=sc, function=start_network_scan, **{'trigger': 'date', 'run_date': datetime.now(pytz.timezone('Europe/Athens'))})
    return sanic_json({"message": " started scanning."}, 200)


if __name__ == "__main__":
    setup_module()
    app.run(host="0.0.0.0", port=8002)
