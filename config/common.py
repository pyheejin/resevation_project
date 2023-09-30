from config.constant import ERROR_DIC
from database.base_model import DefaultModel


def error_response(response: DefaultModel, error_msg: str, result_msg: str):
    if response is None:
        response = DefaultModel()

    if error_msg is None:
        return

    response.result_data = {}
    if error_msg in ERROR_DIC.keys():
        response.result_code = ERROR_DIC[error_msg][0]
        response.result_msg = f'[{result_msg}] {ERROR_DIC[error_msg][1]}'
    else:
        response.result_code = 210
        response.result_msg = f'[{result_msg}] {error_msg}'
    return response