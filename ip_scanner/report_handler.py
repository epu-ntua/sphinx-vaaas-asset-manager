import json

from db_manager.manager import DBManager


def handle_report(report: dict):
    if report.get('__NmapReport__').get('_hosts'):
        for host in report.get('__NmapReport__').get('_hosts'):
            if host.get('__NmapHost__').get('_status').get('state') == 'up':
                host_ip, host_mac = get_asset_ip_and_mac(host.get('__NmapHost__'))
                status = get_host_status(host.get('__NmapHost__'))
                vendor = host.get('__NmapHost__').get('_vendor') if host.get('__NmapHost__').get('_vendor') else 'N/A'
                hostnames = host.get('__NmapHost__').get('_hostnames') if host.get('__NmapHost__').get('_hostnames') else []
                _os = get_host_os(host.get('__NmapHost__'))
                services = get_asset_services(host.get('__NmapHost__'))

                _host_data = {
                    'hostnames': hostnames,
                    'ip': host_ip,
                    'mac': host_mac,
                    'status': status,
                    'vendor': vendor,
                    'os': _os,
                    'services': services,
                    'active': True
                }
                store_asset(_host_data) if not asset_exists(host_mac) else update_asset(_host_data)
            else:
                print('host is down')
    else:
        print('hosts not found')


def get_asset_ip_and_mac(host: dict):
    _ip = host.get('_ipv4_addr') if host.get('_ipv4_addr') else '0.0.0.0'
    _mac = host.get('_mac_addr') if host.get('_mac_addr') else 'ff:ff:ff:ff:ff:ff'
    return _ip, _mac


def get_host_status(host: dict):
    return True if host.get('_status').get('state') == 'up' else False


def get_host_os(host: dict):
    os_name = ''
    os_classes = []
    if host.get('_osfingerprinted'):
        if len(host.get('_extras').get('os').get('osmatches')) > 0:
            for osmatch in host.get('_extras').get('os').get('osmatches'):
                os_name = osmatch.get('osmatch').get('name')
                if len(osmatch.get('osclasses')) > 0:
                    os_classes = osmatch.get('osclasses')
        else:
            pass
        return {'os_name': os_name, 'os_classes': os_classes}
    else:
        return {'os_name': os_name, 'os_classes': os_classes}


def get_asset_services(host: dict):
    services = []
    if len(host.get('_services')) > 0:
        for service in host.get('_services'):
            if service.get('__NmapService__').get('_state').get('state') == 'open':
                services.append({'name': service.get('__NmapService__').get('_service').get('name'),
                                 'port': service.get('__NmapService__').get('_portid'),
                                 'protocol': service.get('__NmapService__').get('_protocol'),
                                 'cpe_list': service.get('__NmapService__').get('_cpelist')})
            else:
                pass
    else:
        pass
    return services


def asset_exists(mac: str):
    _asset = DBManager.get_asset_by_mac(mac)
    return True if _asset else False


def store_asset(data: dict):
    DBManager.create_asset(data)


def update_asset(data: dict):
    _asset = DBManager.get_asset_by_mac(data.get('mac'))
    DBManager.update_asset(_asset[0].id, data) if _asset else None

# testing part
# with open('report.json', 'r') as file:
#     report = json.load(file)
#     handle_report(report)
