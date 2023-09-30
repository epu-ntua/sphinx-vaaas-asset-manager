import json
import threading
from functools import partial

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from libnmap.reportjson import ReportEncoder

from utils.utils import get_main_logger, dmsg
from ip_scanner.report_handler import handle_report
from ip_scanner.networks import get_ip4_addresses
from ipaddress import IPv4Interface

log = get_main_logger('ip_scanner')


def nmap_progress(_proc: NmapProcess, network: str):
    try:
        _task = _proc.current_task
        # print(_proc.progress)
        if _task:
            #     send_socket_subject('task_progress', {
            #         task_id: {f"task_name": _task.name, "status": _task.status, "progress": _task.progress,
            #                   "remaining": _task.remaining}})
            # print(f'{_proc.progress=}')
            print(f"Scanning network: {network}. Current task: {_task.name}-> Progress: {_task.progress} / Remaining: {_task.remaining}")
            # print(f"task_name: {_task.name} -> 'status': {_task.status}, 'etc': {_task.etc}, 'progress': {_task.progress}, 'remaining': {_task.remaining}")
    except Exception as e:
        log.exception(dmsg('') + e.__str__())
        print(dmsg('') + e.__str__())


def nmap_task(target: str = '10.0.100.0/24', intensity: int = 5, thread_num=100):
    nmap_proc = NmapProcess(targets=target, options=f"-F -O -sS T{intensity} --min-parallelism {thread_num}",
                            event_callback=partial(nmap_progress, network=target))
    nmap_proc.run()
    out = NmapParser.parse(nmap_proc.stdout) if check_if_xml(nmap_proc.stdout) else None
    output_dict = json.loads(json.dumps(out, cls=ReportEncoder, indent=4))
    print(output_dict)
    handle_report(output_dict) if output_dict else None


def start_network_scan():
    networks = get_ip4_addresses()
    for net in networks:
        ifc = IPv4Interface(net.get('ip') + '/' + str(net.get('cidr')))
        if str(ifc.network.network_address) != '127.0.0.0' and str(ifc.network.network_address) != '169.254.0.0':  # and str(ifc.network.network_address) != '10.0.0.0':
            print(str(net.get('ip')) + '/' + str(net.get('cidr')))
            threading.Thread(nmap_task(target=str(ifc.network), intensity=5)).run()
            # threading.Thread(nmap_task(target='10.0.100.0/24', intensity=5)).run()


def check_if_xml(payload):
    import xml.dom.minidom
    try:
        a = xml.dom.minidom.parseString(payload)
        return True
    except xml.parsers.expat.ExpatError as e:
        print('NMAP Report is not XML')
        return False


# start_network_scan()
