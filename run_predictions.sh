#!/bin/bash

seq_extension_list="aln bla cm db out sto fasta msa"
temp_extension_list="a2m sto txt"

total_files=$(ls -1 benchmark/fasta_sequences/*.fasta 2>/dev/null | wc -l)
current_count=0

for file in benchmark/fasta_sequences/*.fasta; do
    current_count=$((current_count + 1))
    
    file_name=$(basename "$file" .fasta)

    echo "-------------------------------------------------------"
    echo "[!] Process : $current_count / $total_files"
    echo "[!] Running for $file_name..."
    echo "-------------------------------------------------------"


    if [ -f "benchmark/output/$file_name.pdb" ]; then
        echo "Prediction already made, so skipping."
        continue
    fi

    bash scripts/search_MSA.sh "benchmark/fasta_sequences/$file_name.fasta" benchmark/msa_sequences/ library/rnacentral_99_rep_seq.fasta 8
    

    if [ -f "benchmark/msa_sequences/seq.a3m" ]; then
        mv benchmark/msa_sequences/seq.a3m "benchmark/msa_sequences/$file_name.a3m"
    fi

    # Nettoyage des extensions de séquence
    for ext in $seq_extension_list; do
        rm -f "benchmark/msa_sequences/seq.$ext"
    done

    for ext in $temp_extension_list; do
        rm -f "benchmark/msa_sequences/temp.$ext"
    done

    python -m trRNA2.predict -i "benchmark/msa_sequences/$file_name.a3m" -o benchmark/output
    
    rm -f "benchmark/output/model_1_2D.npz"
    rm -f "benchmark/output/model_1_unrelaxed.pdb"

    if [ -f "benchmark/output/model_1_relaxed200.pdb" ]; then
        mv benchmark/output/model_1_relaxed200.pdb "benchmark/output/$file_name.pdb"
    fi
    
    if [ -f "benchmark/output/plddt.csv" ]; then
        mv benchmark/output/plddt.csv "benchmark/output/$file_name.csv"
    fi

    echo "[!] Prediction done for $file_name ($current_count/$total_files)"
done

echo "Done ! $total_files files have been processed."

python rna_benchmark.py