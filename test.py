import re

with open('energy_data.txt', 'r') as file:
    data = file.read()

re_energy_all = re.compile(r'energy.*\n\n',flags=re.DOTALL)
output = re_energy_all.search(data)
output0= output.group(0)

#print(output0)

re_energy = re.compile(r'energy\d(.*?)energy\d(.*?)energy\d(.*?)\n\n(.*)',flags=re.DOTALL)

energys = re_energy.search(data)
"""
print('energy0',energys.group(1))
print('energy1',energys.group(2))
print('energy2',energys.group(3))
"""
print('energy3',energys.group(4))


re_stru = re.compile(r'(\d+)\s([\d.]+)\s(.+)\n',flags=re.MULTILINE)
a = re_stru.findall(energys.group(4))
print(a)