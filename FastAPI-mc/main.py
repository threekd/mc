import docker
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class predict_parameters(BaseModel):

    smiles_or_inchi_or_file: str
    prob_thresh: int
    param_file: str
    config_file: str
    annotate_fragments: int
    output_file_or_dir: str
    apply_postproc: int
    suppress_exceptions: int



def decoding_smiles(section):

    pattern = r'(\d+)\s([\d.]+)\s([A-Za-z0-9#\+\(\)\[\]\=]+)'
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
                'm/z': float(m.group(1)),
                'intensity': float(m.group(2)),
                'other': int(m.group(3)),
                # Add any additional captures here...
            })
        energy_data[energy_level] = data_points
    return energy_data


def predict(smiles_or_inchi_or_file):


    client = docker.from_env()

    #smiles_or_inchi_or_file = 'InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3'
    prob_thresh = 0.001
    param_file = '/trained_models_cfmid4.0/[M+H]+/param_output.log'
    config_file = '/trained_models_cfmid4.0/[M+H]+/param_config.txt'
    annotate_fragments = 0
    output_file_or_dir = 'output'
    apply_postproc = 1
    suppress_exceptions = 0

    command = f"cfm-predict {smiles_or_inchi_or_file} 0.001 /trained_models_cfmid4.0/[M+H]+/param_output.log /trained_models_cfmid4.0/[M+H]+/param_config.txt 1"
    container_output = client.containers.run('wishartlab/cfmid:latest', command, remove=True)

    decoded_output = container_output.decode('utf-8')

    sections = decoded_output.strip().split('\n\n')
    energy_section = sections[0]
    smiles_section = sections[1]

    energy_data = decoding_energy(energy_section)
    seiles_data = decoding_smiles(smiles_section)
    output_data = energy_data
    output_data["structure"] = seiles_data

    return output_data


#json_output = json.dumps(decoding_energy(energy_section), indent=4)

"""
with open('energy_data.json', 'w') as f:
    f.write(json_output)
"""
class Input_item(BaseModel):
    smiles: str





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Only allow this origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return predict('InChI=1S/C11H14N2/c1-12-7-6-9-8-13-11-5-3-2-4-10(9)11/h2-5,8,12-13H,6-7H2,1H3')

@app.post("/update")
async def calculate(data: Input_item):
    result = predict(data.smiles)  # Use the 'data' instance to access 'smiles'
    return {"result": result}