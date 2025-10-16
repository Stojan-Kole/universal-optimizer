..  _Problem_Drug_Discovery:

Drug Discovery Problem
=========================


The Drug Discovery Problem refers to the task of designing new molecular structures with potential therapeutic properties.  
It is a complex optimization problem that can be approached using computational search methods to explore a vast chemical space.  

In this particular formulation, the optimization process is guided solely by the **QED (Quantitative Estimate of Drug-likeness)** coefficient,  
which is a numerical score estimating how "drug-like" a molecule is based on structural and physicochemical properties.  
The goal is to find molecules with the highest possible QED score.


Problem Definition
------------------

- **Problem:** 
  Problem is represented with class :ref:`DrugDiscoveryProblem<py_drug_discovery_problem>`.

- **Instance:** 
  A set of candidate molecules (represented as SMILES strings) serving as the initial population for optimization.

- **Solution:** 
  A molecular structure with the highest achievable QED coefficient within the search process.

- **Measure:** 
  Maximize the QED coefficient, a real number between 0 and 1, where higher values indicate greater drug-likeness.

Applications
------------------

While real-world drug discovery involves multiple evaluation criteria,  
optimizing solely for QED can serve as a simplified proof-of-concept or benchmark for molecular optimization algorithms.  
This approach can be used in educational, experimental, or early prototyping scenarios before introducing additional objectives.


