from binascii import unhexlify


def parse_input_string(str):
    data = unhexlify(str)
    print(len(data))
    preset = data[0]
    rgb = data[1:6]
    timing = data[7]
    print(preset, rgb, timing)

test_data = input("enter a hex string")
parse_input_string(test_data)