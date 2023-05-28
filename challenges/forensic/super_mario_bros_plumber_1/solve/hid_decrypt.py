# tshark -r test.pcapng -V | grep "HID Data" | sed 's/HID Data: //' > hid_data.txt

def parse_hid_file(file_content):
    hid_values = []
    lines = file_content.split("\n")
    
    for line in lines:
        if line.strip():
            hex_bytes = bytearray.fromhex(line.strip())
            key_index = hex_bytes[3]
            if key_index:
                hid_values.append(format(key_index, '02x'))
    
    return hid_values


filename = "hid_data.txt"

with open(filename, "r") as file:
    hid_input = file.read()

# Parse the HID input
hid_values = parse_hid_file(hid_input) 

# Create a basic HID keycode to character mapping
keycode_map = {
    '04': 'a', '05': 'b', '06': 'c', '07': 'd', '08': 'e',
    '09': 'f', '0a': 'g', '0b': 'h', '0c': 'i', '0d': 'j',
    '0e': 'k', '0f': 'l', '10': 'm', '11': 'n', '12': 'o',
    '13': 'p', '14': 'q', '15': 'r', '16': 's', '17': 't',
    '18': 'u', '19': 'v', '1a': 'w', '1b': 'x', '1c': 'y',
    '1d': 'z', '2c': ' ', '1e': '!', '1f': '@', '20': '#',
    '21': '$', '22': '%', '23': '^', '24': '&', '25': '*',
    '26': '(', '27': ')', '2d': '-', '2e': '+', '2f': '{',
    '30': '}', '31': '|', '33': ':', '34': '"', '35': '~',
    '36': '<', '37': '.', '38': '/', '28': '\n'
}

decrypted_message = ''.join([keycode_map.get(value, '?') for value in hid_values])

print("Decrypted message:")
print(decrypted_message)