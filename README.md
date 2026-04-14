# 📊 RNABenchmark 
by Evan CHAZALLON @ IBISC Laboratory

---

Workflow for incorporating the benchmark of the trRosettaRNA2 model, to an existing one.

---

**Table of contents** 
1. [Installation](#installation)
2. [Pipeline](#pipeline)
    1. [🧬 RNA 3D Structure Prediction Pipeline](#prediction-pipeline)
    2. [📈 Benchmarking Pipeline](#benchmarking-pipeline)
3. [Useful links](#useful-links)

---

## Installation <a name="installation"></a>

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
mv rna_benchmark/* .
```

5. Install the relevant dependencies for the benchmarking tool
```bash
pip install -r requirements.txt
```
⚠️ Note: This benchmarking tool is using RNAdvisor, which is a **docker-based** library. Therefore, you'll need it installed on your machine for the benchmark to work. 


6. Run the benchmark
```bash
python launch_benchmark.py
```




## Pipeline <a name="pipeline"></a>


### 🧬 RNA 3D Structure Prediction Pipeline <a name="prediction-pipeline"></a>

- **Data Prep**: Extracting sequences that are already in the initial benchmark via RNA3DB and converting raw textual sequences into FASTA format (because trRosettaRNA2 does not handle textual sequences as input).

- **MSA Searching**: Automated generation of Multiple Sequence Alignments (outputting .a3m files).

- **Model Inference**: Running the sequences (.a3m) through the model to predict 3D structures.

  &rarr; Results: Final output of .pdb files for structural analysis.

![Prediction pipeline](https://image.noelshack.com/fichiers/2026/16/2/1776170933-screenshot-2026-04-14-at-2-48-37-pm.png)


### 📈 Benchmarking Pipeline <a name="benchmarking-pipeline"></a>

Post-prediction workflow for metric computation and data visualization 

- **Metrics Computation**: Automated scoring using RNAdvisor (GDT-TS, P-VALUE, INF-ALL, RMSD, etc.) for each predicted model.

- **Data Merging**: Joining newly computed metrics with initial benchmark data into a unified global dataset.

- **Data Processing**: Gathering all results (all individual merged benchmarks), followed by value normalization and averaging to ensure statistical consistency.

- **Final Plotting**: Generation of cumulative metric bar plots and individual performance analysis vs. sequence length.

![Benchmarking pipeline](https://image.noelshack.com/fichiers/2026/16/2/1776171010-screenshot-2026-04-14-at-2-49-44-pm.png)


<div align="center">
<img src="https://image.noelshack.com/fichiers/2026/16/1/1776082035-plot-pipeline.png" alt="Final pipeline" width="600"/>
</div>


## Useful links <a name="useful-links"></a>

- [YangLab-SDU/trRosettaRNA2](https://github.com/YangLab-SDU/trRosettaRNA2)
- [EvryRNA/rnadvisor](https://github.com/EvryRNA/rnadvisor)

- [Docker installation guide](https://docs.docker.com/engine/install/)



