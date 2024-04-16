import docker
import json
import re

client = docker.from_env()

smiles_or_inchi_or_file = 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3'
prob_thresh = 0.001
param_file = '/trained_models_cfmid4.0/[M+H]+/param_output.log'
config_file = '/trained_models_cfmid4.0/[M+H]+/param_config.txt'
annotate_fragments = 1
output_file_or_dir = 'output.txt'
apply_postproc = 1
suppress_exceptions = 0

command = "cfm-predict {smiles_or_inchi_or_file} {prob_thresh} {param_file} {config_file} {annotate_fragments} {output_file_or_dir} {apply_postproc} {suppress_exceptions}"
container_output = client.containers.run('wishartlab/cfmid:latest', command, remove=True)

decoded_output = container_output.decode('utf-8')

sections = decoded_output.strip().split('\n\n')
first_section = sections[0]
second_section = sections[1]

def decoding_smiles(section):

    pattern = r'(\d+)\s([\d.]+)\s([A-Za-z0-9#\+\(\)\[\]\=]+)'
    matches = re.findall(pattern, section)

    json_data = []
    for match in matches:
        index, mol_weight, smiles = match
        json_data.append({"index": int(index), "molecular_weight": float(mol_weight), "SMILES": smiles})
    return json_data

def decoding_energy(section):

    energy_pattern = re.compile(r'(energy\d+)(.*?)(?=energy\d+|$)', re.DOTALL)
    data_point_pattern = re.compile(r'(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+).*')

    energy_data = {}
    for energy_level, data_block in energy_pattern.findall(section):
        data_points = []
        for m in data_point_pattern.finditer(data_block):
            data_points.append({
                'm/z': float(m.group(1)),
                'intensity': float(m.group(2)),
                'other': int(m.group(3)),
                # Add any additional captures here...
            })
        energy_data[energy_level] = data_points
    energy_data["structure"] = decoding_smiles(second_section)
    return energy_data

def decoding_smiles(section):

    pattern = r'(\d+)\s([\d.]+)\s([A-Za-z0-9#\+\(\)\[\]\=]+)'
    matches = re.findall(pattern, section)

    json_data = []
    for match in matches:
        index, mol_weight, smiles = match
        json_data.append({"index": int(index), "molecular_weight": float(mol_weight), "SMILES": smiles})
    return json_data

json_output = json.dumps(decoding_energy(first_section), indent=4)

with open('energy_data.json', 'w') as f:
    f.write(json_output)
