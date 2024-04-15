import docker
import json
import re

client = docker.from_env()

command = "cfm-predict 'CC(C)NCC(O)COC1=CC=C(CCOCC2CC2)C=C1' 0.001 /trained_models_cfmid4.0/[M+H]+/param_output.log /trained_models_cfmid4.0/[M+H]+/param_config.txt 1"
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
