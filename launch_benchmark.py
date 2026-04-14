import json
import os

FILENAME = 'split.json'
COLLECTION = 'test_set'

NATIVE_ELEMENTS_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'orphans', 'native')

count = 0

METRICS_MERGED_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_merged')
OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'output')
ROSETTA_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_trRosettaRNA2')

FASTA_SEQ_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'fasta_sequences')
MSA_SEQ_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'msa_sequences')

if not os.path.isdir(METRICS_MERGED_BASE_DIR):
  os.mkdir(METRICS_MERGED_BASE_DIR)

if not os.path.isdir(OUTPUT_BASE_DIR):
  os.mkdir(OUTPUT_BASE_DIR)

if not os.path.isdir(ROSETTA_BASE_DIR):
  os.mkdir(ROSETTA_BASE_DIR)

if not os.path.isdir(FASTA_SEQ_BASE_DIR):
  os.mkdir(FASTA_SEQ_BASE_DIR)

if not os.path.isdir(MSA_SEQ_BASE_DIR):
  os.mkdir(MSA_SEQ_BASE_DIR)


with open(FILENAME, 'r') as file:
  data = json.load(file)

data_collection = data[COLLECTION]

collection_items = list(data_collection.items())


for component in collection_items:
  component_name = component[0]
  component_data = component[1]

  for parent in component_data.items():
    parent_data = parent[1]

    for children in parent_data.items():
      children_name = children[0]
      children_data = children[1]

      if not os.path.isfile(f'{NATIVE_ELEMENTS_BASE_DIR}/{children_name.lower()}.pdb'):
          continue

      sequence = children_data['sequence']
      count = count + 1

      with open(f"benchmark/fasta_sequences/{children_name.lower()}.fasta", "w") as f:
        f.write(f">{children_name}\n")
        f.write(sequence)



os.system('sh run_predictions.sh')