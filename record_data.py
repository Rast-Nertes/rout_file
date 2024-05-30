import importlib.util
import json
import sys
from flask import Flask, request
from random import randint
import socket

app = Flask(__name__)


def import_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise ModuleNotFoundError(f"Module '{module_name}' not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def selenium_route(project_name):
    try:
        module = import_module(f'scripts.{project_name}')
        with app.app_context():
            result_script = module.wallet()
            result_script_file_input = result_script.get_json()

            with open(f'{project_name}.json', 'w') as f:
                json.dump(result_script_file_input, f, indent=4)
                print(f"Данные успешно записаны в файл '{project_name}.json'")

            return result_script_file_input, 200

    except ModuleNotFoundError:
        return {"status": 0, "exception": "Module not found."}, 500

    except Exception as e:
        return {"status": 0, "exception": f"{e}"}, 500


def find_free_port():
    while True:
        port = randint(1000, 9000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python record_data.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    port = find_free_port()

    result, status_code = selenium_route(project_name)
    print(json.dumps(result))

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    sys.exit(status_code)
