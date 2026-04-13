# 📊 RNABenchmark 
by Evan CHAZALLON @ IBISC Laboratory

Workflow for benchmarking the trRosettaRNA2 model:

## 🧬 RNA 3D Structure Prediction Pipeline

- **Data Prep**: Extracting sequences that are already in the initial benchmark via RNA3DB and converting raw textual sequences into FASTA format (because trRosettaRNA2 does not handle textual sequences as input).

- **MSA Searching**: Automated generation of Multiple Sequence Alignments (outputting .a3m files).

- **Model Inference**: Running the sequences (.a3m) through the model to predict 3D structures.

  &rarr; Results: Final output of .pdb files for structural analysis.

![Initial pipeline](https://image.noelshack.com/fichiers/2026/16/1/1776070549-first-pipeline.png)
