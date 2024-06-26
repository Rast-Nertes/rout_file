from flask import Flask, jsonify, request
import importlib.util

app = Flask(__name__)


def import_module(module_name):
    spec = importlib.util.find_spec(module_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@app.route('/api/selenium/<project_name>')
def selenium_route(project_name):
    try:
        module = import_module(f'scripts.{project_name}')
        return module.wallet()

    except ModuleNotFoundError:
        return jsonify({"status": 0, "exception": f"Other project logic here."}), 500

    except Exception as e:
        return jsonify({"status": 0, "exception": f"{e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
