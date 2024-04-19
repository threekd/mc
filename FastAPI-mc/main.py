import docker
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

def decoding_smiles(section):

    pattern = r'(\d+)\s([\d.]+)\s([A-Za-z0-9#\+\-\(\)\[\]\=]+)'
    matches = re.findall(pattern, section)

    smiles_data = []
    for match in matches:
        index, mol_weight, smiles = match
        smiles_data.append({"index": int(index), "molecular_weight": float(mol_weight), "SMILES": smiles})
    return smiles_data

def decoding_energy(section):

    energy_pattern = re.compile(r'(energy\d+)(.*?)(?=energy\d+|$)', re.DOTALL)
    data_point_pattern = re.compile(r'(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+).*')

    energy_data = {}
    for energy_level, data_block in energy_pattern.findall(section):
        data_points = []
        for m in data_point_pattern.finditer(data_block):
            data_points.append({
                'mass': float(m.group(1)),
                'intensity': float(m.group(2)),
                'fragment_id': int(m.group(3)),
                # Add any additional captures here...
            })
        energy_data[energy_level] = data_points
    return energy_data


def predict(predict_input):


    client = docker.from_env()

    #smiles_or_inchi_or_file = 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3'
    prob_thresh = 0.001
    param_file = f'/trained_models_cfmid4.0/{predict_input.AdductType}/param_output.log'
    config_file = f'/trained_models_cfmid4.0/{predict_input.AdductType}/param_config.txt'
    annotate_fragments = 0
    output_file_or_dir = 'output'
    apply_postproc = 1
    suppress_exceptions = 0

    command = f"cfm-predict {predict_input.smiles_or_inchi_or_file} 0.001 {param_file} {config_file} 1"
    container_output = client.containers.run('wishartlab/cfmid:latest', command, remove=True)

    decoded_output = container_output.decode('utf-8')

    sections = decoded_output.strip().split('\n\n')
    energy_section = sections[0]
    smiles_section = sections[1]

    energy_data = decoding_energy(energy_section)
    seiles_data = decoding_smiles(smiles_section)
    output_data = energy_data
    output_data["structure"] = seiles_data

    return match_fregment(output_data)

def match_fregment(data):

    # Create a dictionary to map structure index to its data
    structure_mapping = {struct['index']: struct for struct in data['structure']}

    # Function to enrich energy fragments with structure data
    def enrich_fragments(energy_data):
        for fragment in energy_data:
            # Find the corresponding structure data using fragment_id
            structure = structure_mapping.get(fragment['fragment_id'])
            
            # Add the molecular_weight and SMILES data to the fragment
            if structure:
                fragment['molecular_weight'] = structure['molecular_weight']
                fragment['SMILES'] = structure['SMILES']

    # Enrich fragments in all energy levels
    for energy_key in ['energy0', 'energy1', 'energy2']:
        enrich_fragments(data[energy_key])
    return data

#json_output = json.dumps(decoding_energy(energy_section), indent=4)

"""
with open('energy_data.json', 'w') as f:
    f.write(json_output)
"""
class Input_item(BaseModel):
    smiles_or_inchi_or_file: str
    AdductType: str





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allow this origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
async def calculate(predict_input: Input_item):
    result = predict(predict_input)
    return {"result": result}