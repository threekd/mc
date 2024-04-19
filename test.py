import json

# Load the JSON data from file
with open('energy_data.json', 'r') as file:
    data = json.load(file)

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

# The `data` variable now contains the enriched energy data structure
# You can now save this data back to a file or do whatever you need with it
print(json.dumps(data, indent=4))  # This will print the updated JSON with additional fields