import re

with open('energy_data.txt', 'r') as file:
    data = file.read()

def output_to_json1(output_str:str):


    re_energy_and_fragment = re.compile(r'energy0(.*?)energy1(.*?)energy2(.*?)\n\n(.*)',flags=re.DOTALL)

    energy_and_fragment = re_energy_and_fragment.search(output_str)
    if energy_and_fragment:
        energy0 = energy_and_fragment.group(1)
        energy1 = energy_and_fragment.group(2)
        energy2 = energy_and_fragment.group(3)
        id_fragment = energy_and_fragment.group(4)

        re_mass_intensity = re.compile(r'^([\d.]+)\s([\d.]+)', flags=re.MULTILINE)
        re_fragment_id_value = re.compile(r'^[\d.]+\s[\d.]+\s(.*)', flags=re.MULTILINE)
        re_fragment = re.compile(r'^([\d.]+)\s([\d.]+)\s(.*)', flags=re.MULTILINE)

        mass_intensity0 = re_mass_intensity.findall(energy0)
        mass_intensity1 = re_mass_intensity.findall(energy1)
        mass_intensity2 = re_mass_intensity.findall(energy2)

        fragment_id_value = re_fragment_id_value.findall(re_fragment_id_value)

        fragment = re_fragment.findall(id_fragment)


def output_to_json(output_str:str):

    output_dict = {}

    re_energy_and_fragment = re.compile(r'energy0(.*?)energy1(.*?)energy2(.*?)\n\n(.*)',flags=re.DOTALL)

    energy_and_fragment = re_energy_and_fragment.search(output_str)
    if energy_and_fragment:
        energys = energy_and_fragment.groups()[:3]
        fragments = energy_and_fragment.groups()[3:4]

        for num, energy in enumerate(energys):
            mass_intensity_other_dict = {}

            re_mass_intensity_other = re.compile(r'^([\d.]+)\s([\d.]+)\s(.*)', flags=re.MULTILINE)
            mass_intensity_other = re_mass_intensity_other.findall(energy)
            for item in mass_intensity_other:
                mass = item[0]
                intensity = item[1]
                other = item[2]

                mass_intensity_other_dict[f'{mass}'] = [intensity,other]
            output_dict[f'energy{num}'] = mass_intensity_other_dict
        print(output_dict)


        


output_to_json(data)