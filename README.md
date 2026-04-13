# 📊 RNABenchmark 
by Evan CHAZALLON @ IBISC Laboratory

Workflow for incorporating the benchmark of the trRosettaRNA2 model, to an existing one.

## Installation

1. Install trRosettaRNA2 model

```bash
git clone https://github.com/YangLab-SDU/trRosettaRNA2.git
cd trRosettaRNA2
```

2. Install trRosettaRNA2 environment
```bash
mamba env create -f environment.yml
mamba activate trRNA2
```

3. Download the network weights
```bash
wget http://yanglab.qd.sdu.edu.cn/trRosettaRNA/download/params_trRNA2.tar.bz2
# If you encounter timeout or connection errors, try downloading from our Hugging Face mirror instead:
# wget https://huggingface.co/datasets/quailwwk/trRNA2/resolve/main/params_trRNA2.tar.bz2

tar -jxvf params_trRNA2.tar.bz2
```

Staying in the same folder, let's install the benchmark tool 

4. Downloading benchmarking tool
```bash
git clone https://github.com/EvanCHAZALLON/rna_benchmark.git
```

5. Install the relevant dependencies for the benchmarking tool
```bash
pip install -r requirements.txt
```


6. Run the benchmark
```bash
python launch_benchmark.py
```




## Pipeline


### 🧬 RNA 3D Structure Prediction Pipeline

- **Data Prep**: Extracting sequences that are already in the initial benchmark via RNA3DB and converting raw textual sequences into FASTA format (because trRosettaRNA2 does not handle textual sequences as input).

- **MSA Searching**: Automated generation of Multiple Sequence Alignments (outputting .a3m files).

- **Model Inference**: Running the sequences (.a3m) through the model to predict 3D structures.

  &rarr; Results: Final output of .pdb files for structural analysis.

![Prediction pipeline](https://image.noelshack.com/fichiers/2026/16/1/1776070549-first-pipeline.png)


### 📈 Benchmarking Pipeline

Post-prediction workflow for metric computation and data visualization 

- **Metrics Computation**: Automated scoring using RNAdvisor (GDT-TS, P-VALUE, INF-ALL, RMSD, etc.) for each predicted model.

- **Data Merging**: Joining newly computed metrics with initial benchmark data into a unified global dataset.

- **Data Processing**: Gathering all results (all individual merged benchmarks), followed by value normalization and averaging to ensure statistical consistency.

- **Final Plotting**: Generation of cumulative metric bar plots and individual performance analysis vs. sequence length.

![Prediction pipeline](https://image.noelshack.com/fichiers/2026/16/1/1776082032-merging-pipeline.png)


<div align="center">
<img src="https://image.noelshack.com/fichiers/2026/16/1/1776082035-plot-pipeline.png" alt="Final pipeline" width="600"/>
</div>


