import re
import json

with open('energy_data.txt', 'r') as file:
    data = file.read()

def output_to_json(output_str:str):

    output_dict = {}

    re_energy_and_fragment = re.compile(r'energy0(.*?)energy1(.*?)energy2(.*?)\n\n(.*)',flags=re.DOTALL)

    energy_and_fragment = re_energy_and_fragment.search(output_str)
    if energy_and_fragment:
        fragment_dict = {}
        energys = energy_and_fragment.groups()[:3]
        fragment = energy_and_fragment.group(4)

        re_id_mass_smiles = re.compile(r'^([\d]+)\s([\d.]+)\s(.*)', flags=re.MULTILINE)
        id_mass_smiles = re_id_mass_smiles.findall(fragment)
        for item in id_mass_smiles:
            id = item[0]
            mass = item[1]
            smiles = item[2]
            fragment_dict[f'{id}'] = [mass,smiles]

        for num, energy in enumerate(energys):
            mass_intensity_other_dict = {}

            re_mass_intensity_other = re.compile(r'^([\d.]+)\s([\d.]+)\s(.*)', flags=re.MULTILINE)
            mass_intensity_other = re_mass_intensity_other.findall(energy)
            for item in mass_intensity_other:
                other_dict = {}
                mass = item[0]
                intensity = item[1]
                other = re.findall(r'[\d.]+',item[2])
                half_len_other = len(other)//2
                for i in range(half_len_other):
                    other_dict[f'{other[i]}'] = other[half_len_other+i]
                main_SMILES = fragment_dict[other[0]]
                
                mass_intensity_other_dict[f'{mass}'] = [intensity,main_SMILES,other_dict]

            output_dict[f'energy{num}'] = mass_intensity_other_dict

        output_dict['fragment'] = fragment_dict
        print(output_dict)


    

    output_json = json.dumps(output_dict, indent=4)
    return output_json




with open('energy_data.json', 'w') as f:
    f.write(output_to_json(data))
        