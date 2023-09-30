import argparse
import logging

settings = {
    "DEV": {
        "app_name": "vaaas",
        "logger_url": "10.0.1.220",
        "logger_port": "9898",
        "logger_protocol": "http",

        "db_name": 'vaaas',
        "db_url": "localhost",
        "db_port": '27017',
        "username": "yannis",
        "password": "yannis"
    },
    "PROD": {
        "app_name": "vaaas",
        "logger_url": "10.0.1.220",
        "logger_port": "9898",
        "logger_protocol": "http",

        "db_name": 'vaaas',
        "db_url": "127.0.0.1",
        "db_port": '27017',
        "username": "vaaas",
        "password": "vaaas"
    },
    "TEST": {
        "app_name": "vaaas",
        "logger_url": "10.0.1.220",
        "logger_port": "9898",
        "logger_protocol": "http",

        "db_name": 'vaaas',
        "db_url": "10.0.1.220",
        "db_port": '27017',
        "username": "vaaas",
        "password": "vaaas"
    }
}


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', help='Set the running mode (dev/prod)')
    options = parser.parse_args() if parser.parse_args() else {}

    # Check for errors i.e if the user does not specify the target IP Address
    # Quit the program if the argument is missing
    # While quitting also display an error message
    if not options.mode:
        # Code to handle if interface is not specified
        # parser.error("[-] Please specify the running mode (dev/prod), use --help for more info.")
        logging.error("[-] Please specify the running mode (dev/prod), use --help for more info.")
        # options.mode = 'DEV'
        # return options
    else:
        pass
    return options


def get_mode():
    options = get_args()
    if options.mode:
        assert options.mode.upper() in ['DEV', 'PROD', 'TEST']
        MODE = options.mode.upper()
    else:
        MODE = 'DEV'
    return MODE


def get_config():
    return settings[get_mode()]
