import re

with open('energy_data.txt', 'r') as file:
    data = file.read()

re_energy_all = re.compile(r'energy.*\n\n',flags=re.DOTALL)
output = re_energy_all.search(data)
output0= output.group(0)

#print(output0)

re_energy = re.compile(r'^energy\d(.*?)energy\d(.*?)energy\d(.*)',flags=re.DOTALL)

energys = re_energy.search(output0)
print(energys.group(0))
print('energy0',energys.group(1))
