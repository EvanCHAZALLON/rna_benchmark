# Importing libraries
import os

# Data handling
import numpy as np
import pandas as pd
import json
import shutil

# Signal treatment
import statsmodels.api as sm

# Data viz
import matplotlib.pyplot as plt
import seaborn as sns

# RNAdvisor tool
from rnadvisor.enums.list_dockers import DESCENDING_METRICS
from rnadvisor.rnadvisor_cli import RNAdvisorCLI

'''
Definitions
'''

# Directories definition
OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'output')
NATIVE_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'orphans', 'native')
ROSETTA_METRICS_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_trRosettaRNA2')
CLEMENT_METRICS_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_benchmark_clement')
MERGED_METRICS_BASE_DIR = os.path.join(os.getcwd(), 'benchmark', 'metrics_merged')
FIGURES_BASE_DIR = os.path.join(os.getcwd(), 'figures')
DATA_OUTPUT_BASE_DIR = os.path.join(os.getcwd(), 'data_output')

# Metrics definition
BENCHMARKED_METRICS = ['GDT-TS', 'P-VALUE', 'INF-ALL', 'MCQ', 'TM-score', 'lDDT', 'RMSD', 'BARNABA-eRMSD']
DESCENDING_METRICS = ['RMSD', 'P-VALUE', 'MCQ', 'BARNABA-eRMSD']

# Models definition
BENCHMARKED_MODELS = ['rhofold', 'alphafold3', 'rnajp', 'rnacomposer', 'trrosettarna2']

# String definitions
SEPARATOR = '--------------------------'

'''
Utils functions
'''

# Normalize all data points for a metric, depending if this metric is ascending or descending
def normalize_metric(data, metric):
    new_list = np.zeros(len(data))

    for i, el in enumerate(data):
        x_scaled = el/np.nanmax(data)

        new_list[i] = x_scaled
        if metric in DESCENDING_METRICS:
            new_list[i] = 1 - x_scaled

    return new_list


# Creates subdirectories for all .pdb predictions files for RNAdvisor to work properly [otherwise compares native file with all files of the same directory as the prediction]
def create_all_sub_directories():
    if not os.path.isdir(DATA_OUTPUT_BASE_DIR): os.mkdir(DATA_OUTPUT_BASE_DIR)

    for file in os.listdir(OUTPUT_BASE_DIR):
        if file.endswith('.pdb'):
            if not os.path.isdir(os.path.join(OUTPUT_BASE_DIR, file.split('.pdb')[0])):
                filename = os.fsdecode(file).split('.pdb')[0]
                os.mkdir(OUTPUT_BASE_DIR + '/' + filename)
                shutil.copy(f'{OUTPUT_BASE_DIR}/{filename}.pdb', OUTPUT_BASE_DIR + '/' + filename) # Copying the .pdb file into the newly created directory

                print(f'[INFO] Created folder for file {file}.')


# Retrieve sequence length with file name into RNA3DB JSON dataset
def find_length_by_name(name: str):
    # Opening the JSON dataset to retrive lengths into it
    with open('split.json', 'r') as f:
        data = json.load(f)

    # Clement's benchmark is only focusing on component 0
    component_0 = data['test_set']['component_0']

    # Browsing elements (el) and sub-elements (el2) to retrieve sequence length
    for el in component_0:
        for el2 in component_0[el]:
            if el2.lower() == name.lower():
                return component_0[el][el2]['length']

    # Return length of zero by default
    return 0


# Compares Clement's benchmark files with our predictions in the directory benchmark/output/ to find missing files
def get_missing_files():
    missing_elements = []
    missing_string = ''

    missing_count = 0
    total_count = 0

    for file in os.listdir(NATIVE_BASE_DIR):
        filename = os.fsdecode(file).split('.pdb')[0]
        total_count = total_count + 1

        if not os.path.isfile(f'{OUTPUT_BASE_DIR}/{filename}.pdb'):
            missing_count = missing_count + 1
            missing_elements.append(filename)
            missing_string = missing_string + filename + '.pdb, '

    print(SEPARATOR)
    print(f'[ALERT] Missing files: {missing_count}/{total_count}')
    print(f'[ALERT] Missing files are: {missing_string}')
    print(SEPARATOR)

    return missing_elements, missing_count



'''
Benchmarking functions
'''

# Computing metrics for all files that aren't missing, using RNAdvisor
def compute_metrics():
    for file in os.listdir(os.fsencode(NATIVE_BASE_DIR)):
        rna_name = os.fsdecode(file).split('.pdb')[0]

        if rna_name in missing_elements:
            print(f'[WARNING] Skipping {rna_name} because missing prediction file .pdb')
            continue

        if os.path.isfile(f'{ROSETTA_METRICS_BASE_DIR}/{rna_name}_inter.csv'):
            # print(f'[INFO] Already computed metrics for {rna_name}, so skipping.')
            continue

        pred_path = f'{OUTPUT_BASE_DIR}/{rna_name}/{rna_name}.pdb'
        output_path = f'{ROSETTA_METRICS_BASE_DIR}/{rna_name}_inter.csv'
        native_path = f'{NATIVE_BASE_DIR}/{rna_name}.pdb'

        # Usage of RNAdvisor tool to compute different metrics for each prediction
        rnadvisor_cli = RNAdvisorCLI(
            pred_dir=pred_path,
            native_path=native_path,
            out_path=None,
            scores=['RMSD', 'P-VALUE', 'INF', 'DI', 'MCQ', 'TM-SCORE', 'CAD', 'BARNABA', 'CLASH', 'GDT-TS', 'lDDT', 'LCS-TA'],
            params={'mcq_threshold': 10, 'mcq_mode': 2}
        )
        df_results, df_time = rnadvisor_cli.predict()

        df_results = df_results.rename(index={f'{rna_name}.pdb': f'normalized_trrosettarna2_{rna_name}.pdb'})
        df_results.index.name = None

        df_results.to_csv(f'{ROSETTA_METRICS_BASE_DIR}/{rna_name}_inter.csv')
        print(f'[INFO] Success! Computed metrics for {rna_name}.')

        # Cleaning all docker containers, otherwise they remain idle and take some storage
        os.system('docker rm -v -f $(docker ps -qa)')


# Concatenation of Clement's metrics and our trRosettaRNA2 metrics in benchmark/metrics_merged/, for each file of prediction in benchmark/output/
def merge_benchmarks():
    for file in os.listdir(ROSETTA_METRICS_BASE_DIR):
        if file.endswith('.csv'):
            filename = os.fsdecode(file).split('_inter')[0]

            # Retrieving Clement's metrics
            clement_path = os.path.join(CLEMENT_METRICS_BASE_DIR, f'{filename}.csv')
            clement_data = pd.read_csv(clement_path, index_col=[0])

            # Retrieving trRosettaRNA2 metrics which were computed just before
            rosetta_data = pd.read_csv(f'{ROSETTA_METRICS_BASE_DIR}/{filename}_inter.csv', index_col=[0])
            rosetta_data = rosetta_data.rename(columns={'lddt': 'lDDT'})

            # Concatenation of the dataframes, to have a all-in-one benchmark
            final_df = pd.concat([clement_data, rosetta_data])
            final_df.to_csv(f'{MERGED_METRICS_BASE_DIR}/{filename}.csv')


# Normalizing metrics, averaging them, and exporting them into distinct .csv files and dataframes
def analyze_and_export_metrics():
    # For each model, we have all metrics keys, and each contain metric data for all predictions
    scores = {model: {metric: [] for metric in BENCHMARKED_METRICS} for model in BENCHMARKED_MODELS}

    # Creation of a list containing (in the right order) the length of the sequence for each prediction file
    length_list = []

    # Collecting each metric of each prediction for each model, and putting it into the above dictionary
    for file in os.listdir(MERGED_METRICS_BASE_DIR):
        if file.endswith('.csv'):
            df = pd.read_csv(f'{MERGED_METRICS_BASE_DIR}/{file}', index_col=[0])

            length_list.append(find_length_by_name(file.split('.csv')[0]))

            for index, row in df.iterrows():
                model_name = index.split('_')[1]

                if model_name in BENCHMARKED_MODELS:
                    for metric, value in row.items():
                        if metric in BENCHMARKED_METRICS:
                            scores[model_name][metric].append(value)


    # For convenience, inputting the list containing (in the right order) the length of each prediction file
    for model in BENCHMARKED_MODELS:
        scores[model]['length'] = length_list

    metrics_df = pd.DataFrame(scores)
    metrics_df.to_csv(f'{DATA_OUTPUT_BASE_DIR}/all_metrics_all_models.csv') # Exporting raw metrics data, not normalized and not averaged

    normalized_averaged_metrics = {model: {metric: 0.0 for metric in BENCHMARKED_METRICS} for model in BENCHMARKED_MODELS}

    # Computing normalization and average of all the metrics
    for model in BENCHMARKED_MODELS:
        for metric in BENCHMARKED_METRICS:
            scores[model][metric] = normalize_metric(scores[model][metric], metric)         # Normalizing each metric computed
            normalized_averaged_metrics[model][metric] = np.nanmean(scores[model][metric])  # Average over normalized metrics, and putting it into the new dictionary


    normalized_averaged_metrics_df = pd.DataFrame(normalized_averaged_metrics)
    normalized_averaged_metrics_df.to_csv(f'{DATA_OUTPUT_BASE_DIR}/all_metrics_all_models_normalized.csv')

    return metrics_df, normalized_averaged_metrics_df



'''
Plotting functions
'''

# Plotting function: cumulative barplot benchmark
def plot_benchmark(normalized_averaged_metrics_df: pd.DataFrame):
    if not os.path.isdir(FIGURES_BASE_DIR): os.mkdir(FIGURES_BASE_DIR)

    normalized_averaged_metrics_df['total'] = normalized_averaged_metrics_df.sum(axis=1)
    f_df_sorted = normalized_averaged_metrics_df.sort_values('total', ascending=True).drop(columns=['total'])

    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'

    fig, ax = plt.subplots(figsize=(12, 8))

    f_df_sorted.plot(kind='barh', stacked=True, ax=ax, colormap='viridis', edgecolor='white', linewidth=0.5, width=0.6)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('#333333')
        ax.spines[spine].set_linewidth(1.2)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('Cumulative Normalized Score Metrics', fontsize=13, labelpad=10)
    ax.set_ylabel('Models', fontsize=13)

    ax.xaxis.grid(True, linestyle='--', alpha=0.4, color='gray')
    ax.legend(title='Metrics', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

    ax.set_xlim([0.0, len(BENCHMARKED_METRICS)])
    plt.tight_layout()

    plt.savefig(f'{FIGURES_BASE_DIR}/BENCHMARK_RNA3DB.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()


def plot_length_benchmarks(metrics_df: pd.DataFrame):
    length_array = metrics_df['length'].iloc[0]

    for metric in metrics_df:
        if metric != 'length':
            fig, ax = plt.subplots(figsize=(8, 5))

            ax.set_ylabel(f'Metric: {metric}')
            ax.set_xlabel('Sequence length')
            ax.set_title('Metric performance v.s. sequence length')

            for model, data in metrics_df[metric].items():
                data = pd.DataFrame({'length': length_array, 'data': data})  # Otherwise JSON can't load nan values
                data = data[data['data'] != np.nan]
                data = data.groupby(by='length', as_index=False).mean()

                x = np.array(data['length'])
                y = np.array(data['data'])

                lowess = sm.nonparametric.lowess
                z = lowess(y, x, frac=0.15)

                sns.lineplot(x=z[:, 0], y=z[:, 1], label=model, ax=ax, linewidth=2.5)

            plt.savefig(f"{FIGURES_BASE_DIR}/{metric}_vs_length.png", dpi=300, bbox_inches='tight')



'''
Program begins here
'''

# Checking which files are missing compared to Clement's benchmark
missing_elements, missing_count = get_missing_files()

# Creating subdirectories for each prediction for RNAdvisor convenience
create_all_sub_directories()

# Computing metrics for trRosettaRNA2 from our predictions in benchmark/output
compute_metrics()

# Merging of Clement's benchmark AND my benchmark for trRosettaRNA2 metrics
merge_benchmarks()

# Computing metrics and exporting them into .csv files using merged benchmark data generated before
metrics_df, normalized_averaged_metrics_df = analyze_and_export_metrics()

# Plotting the final benchmark
plot_benchmark(normalized_averaged_metrics_df.T)
plot_length_benchmarks(metrics_df.T)