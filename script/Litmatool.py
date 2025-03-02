import json, subprocess
import numpy as np
import scipy.stats as stats

json_data = json.load(open('../lang/zh_cn.json', 'r', encoding='utf-8'))


def convert_units(number):
    units = {'箱': 54 * 27 * 64, '盒': 27 * 64, '组': 64, '个': 1}
    result = ""
    for unit, value in units.items():
        if number >= value:
            count = number // value
            result += f"{count}{unit}"
            number %= value
    return result if result else "0个"

def cn_translate(id, key: bool = True, types = "Blocks") -> object:
    '''

    :param id: Object ID translate
    :param key: Justify is translate from value to key
    :param type: transfer dist type
    :return: Object Chinese name
    '''
    return json_data[types].get(id, id) if key else json_data[types][id]

def manual_install_pk():
    try:
        result = subprocess.run(['install.bat'], check=True, capture_output=True, text=True)
        print("Packages install successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

def find_keys_by_value_in_list(dictionary, target_value):
    return [key for key, value_list in dictionary.items() if target_value in value_list]

def Category_Tran(data):
    for key, value_list in json_data["Category"].items():
        for prop in data.split("_"):
            if prop in value_list:
                return key
    return ""

def statistics(data):
    print(data)
    if not data: return []
    mean = np.mean(data)
    median = np.median(data)
    mode = stats.mode(data)
    std_dev = np.std(data, ddof=1)
    IQR = np.percentile(data, 75)-np.percentile(data, 25)
    return [IQR,mean,median,mode,std_dev]

def id_tran_name(id: object) -> object:
    """

    :rtype: object
    """
    return id.split(':')[1]

if __name__ == "__main__":
    pass