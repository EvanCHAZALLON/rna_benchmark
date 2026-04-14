# Importing libraries
import os
import json

'''
Definitions
'''

# Directories definition
DATASET_FILE = 'split.json'
NATIVE_ELEMENTS_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'orphans', 'native')
METRICS_MERGED_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_merged')
OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'output')
ROSETTA_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_trRosettaRNA2')
FASTA_SEQ_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'fasta_sequences')
MSA_SEQ_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'msa_sequences')
FIGURES_BASE_DIR = os.path.join(os.getcwd(), 'figures')
DATA_OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'data_output')

'''
Utils functions
'''

# Creates base directories
def setup_directories():
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

  if not os.path.isdir(DATA_OUTPUT_BASE_DIR):
    os.mkdir(DATA_OUTPUT_BASE_DIR)

  if not os.path.isdir(FIGURES_BASE_DIR):
    os.mkdir(FIGURES_BASE_DIR)



'''
Utils functions
'''

# Converts sequence in the original dataset to .fasta files so the model can handle them
# Finds all the files in the benchmark/orphans/native directory, i.e. the files present in the original benchmark
def converts_to_fasta(data: list, collection_name: str):
  collection_items = list(data[collection_name].items())

  # Looping through all the dataset, with elements and sub-elements into components of input collection_name (train/test set)
  for component in collection_items:
    component_name = component[0]
    component_data = component[1]

    for parent in component_data.items():
      parent_data = parent[1]

      for children in parent_data.items():
        children_name = children[0]
        children_data = children[1]

        # If the file is not existing in benchmark/orphans/native, it means it hasn't been tested on the original benchmark,
        # so we skip it.
        if not os.path.isfile(f'{NATIVE_ELEMENTS_BASE_DIR}/{children_name.lower()}.pdb'):
          continue

        sequence = children_data['sequence']
        with open(f"benchmark/fasta_sequences/{children_name.lower()}.fasta", "w") as f:
          f.write(f">{children_name}\n")
          f.write(sequence)



'''
Program begins here
'''

with open(DATASET_FILE, 'r') as file:
  data = json.load(file)

converts_to_fasta(data, 'test_set')
converts_to_fasta(data, 'train_set')

os.system('sh run_predictions.sh')