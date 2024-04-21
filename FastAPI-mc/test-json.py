import docker
import re
import json

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
    return(output_dict)


def predict():


    client = docker.from_env()

    smiles_or_inchi_or_file = 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3'
    command = f"cfm-predict {smiles_or_inchi_or_file} 0.001 /trained_models_cfmid4.0/[M+H]+/param_output.log /trained_models_cfmid4.0/[M+H]+/param_config.txt 1"
    container_output = client.containers.run('wishartlab/cfmid:latest', command, remove=True)

    decoded_output = container_output.decode('utf-8')
    with open('energy_data.txt', 'w') as f:
        f.write(decoded_output)



    return output_to_json(decoded_output)

json_output = json.dumps(predict(), indent=4)

with open('energy_data.json', 'w') as f:
    f.write(json_output)
