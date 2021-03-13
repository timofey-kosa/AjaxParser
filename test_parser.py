import pytest

test_data = [("10FA0E00", {'field1': 'Low',
                             'field2': '00',
                             'field3': '01',
                             'field4': '00',
                             'field5': '00',
                             'field6': '01',
                             'field7': '00',
                             'field8': 'Very High',
                             'field9': '00',
                             'field10': '00'}),
            ]

#Format settings - array [sett_byte1 as dict {bit: [size, 'field_name']}, sett_byte2, sett_byte3, sett_byte4]
device_settings = [{0: [3, 'field1'],
                    3: [1, 'field2'],
                    4: [1, 'field3'],
                    5: [3, 'field4']},
                   {0: [1, 'field5'],
                    1: [1, 'field6'],
                    2: [1, 'field7'],
                    3: [3, 'field8'],
                   },
                   {0: [1, 'field9'],
                    5: [1, 'field10']
                   },
                   {}
                  ]

field1 = {'0': 'Low',
          '1': 'reserved',
          '2': 'reserved',
          '3': 'reserved',
          '4': 'Medium',
          '5': 'reserved',
          '6': 'reserved',
          '7': 'High',
          }
field4 = {'0': '00',
          '1': '10',
          '2': '20',
          '3': '30',
          '4': '40',
          '5': '50',
          '6': '60',
          '7': '70',
          }
field8 = {'0': 'Very Low',
          '1': 'reserved',
          '2': 'Low',
          '3': 'reserved',
          '4': 'Medium',
          '5': 'High',
          '6': 'reserved',
          '7': 'Very High',
          }


def get_data_from_payload(payload):
    hex_string = ([x for x, y in payload])[0]
    hex_int = int(hex_string, 16)
    bin_num = f'{hex_int:0>32b}'
    bin_num = bin_num[:24]
    bin_num = bin_num[::-1]
    """
    Две строчки выше - вынужденный костыль. Единственный возможный способ получить по входным значениям выходные, это:
    После перевода 10FA0E00 в двоичную систему, выкинуть пустой байт, пронумеровать оставшиеся байты слева направо, а биты 
    отсчитывать справа налево. Если этому есть логическое объяснение хотелось бы услышать. 
    """
    byte3 = bin_num[0:8]
    byte2 = bin_num[8:16]
    byte1 = bin_num[16:]
    byte_pack = [byte1, byte2, byte3]
    parsed_data = {}

    for i, k in enumerate(device_settings):
        keys = k.keys()
        for key in keys:
            var = list(device_settings[i].get(key))
            size = var[0]
            if size == 1:
                temp = byte_pack[i]
                temp = f'0{temp[key:key+size]}'
                """
                Откуда на выходе должен был взяться 0 перед каждым одиночным битом я тоже не понял, но дорисовал.
                """
            else:
                temp = byte_pack[i][key:key+size]
                temp = int(temp, 2)
                if var[1] == 'field1':
                    temp = field1.get(str(temp))
                elif var[1] == 'field4':
                    temp = field4.get(str(temp))
                elif var[1] == 'field8':
                    temp = field8.get(str(temp))
            parsed_data.update({var[1]: temp})

    return parsed_data

@pytest.mark.parametrize('data', [test_data])
def test_parsing_expected_results(data):
    assert get_data_from_payload(data) == ([y for x, y in data])[0], 'Results not match'