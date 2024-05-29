from flask import Flask, jsonify
import importlib.util
import json

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
        result_script = module.wallet()
        result_script_file_input = result_script.json

        with open(f'{project_name}.json', 'w') as f:
            json.dump(result_script_file_input, f, indent=4)
            print(f"Данные успешно записаны в файл '{project_name}.json'")

        return result_script

    except ModuleNotFoundError:
        return jsonify({"status": 0, "exception": f"Other project logic here."}), 500

    except Exception as e:
        return jsonify({"status": 0, "exception": f"{e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)