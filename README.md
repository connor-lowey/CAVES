![alt text](https://github.com/connor-lowey/CAVES/blob/main/caves_logo.png)

# Introduction
*In silico* methods for immune epitope prediction have become essential for vaccine and therapeutic design, but manual intra-species comparison of putative epitopes remains challenging and subject to human error. **CAVES** (**C**omparative **A**nalysis of **V**ariant **E**pitope **S**equences) is an novel tool created to automate comparative epitope analyses. 

CAVES utilizes two levels of comparisons to organize putative epitopes from two closely related sequences (sequence A and B) into multiple informative categories. **Level-one** (L1) shows the extent to which the two epitope profiles match by directly comparing files of epitope predictions, while **Level-two** (L2) compares each sorted category from L1 against files of database search results to determine if the putative epitopes have been experimentally confirmed in published literature.  
In both levels, epitopes are sorted into categories of **exact matches**, **partial matches**, or **novel epitopes**.

# Resources
* **Website**: https://github.com/connor-lowey/CAVES
* **Publication**: Publication pending
* **Sample dataset**: https://github.com/connor-lowey/CAVES/tree/main/sample_dataset

# Installation
CAVES runs through a graphical user interface on Windows operating systems. The software is downloadable as a zipped file containing the standalone executable program with all required dependencies precompiled.

# Running CAVES
## Level-one input files
In Level-one (L1), CAVES takes epitope prediction results directly from tools hosted by the Immune Epitope Database-Analysis Resource (IEDB-AR, http://tools.iedb.org/main/) and looks for all possible match combinations. 

**IEDB-AR compatible tools**:
* TepiTool (T cell epitope prediction, class I or II) http://tools.iedb.org/tepitool/
* B cell linear epitope prediction tool http://tools.iedb.org/bcell/
&nbsp;

&nbsp;

Epitopes should be predicted for sequence A and B using the same tool and parameters for fair comparison.  
Results from TepiTool can be downloaded as a **CSV** file and uploaded directly into CAVES.  
Results from the B cell tool must be copied and pasted into a spreadsheet software (download option not available), and saved as a **CSV** file for upload to CAVES.

## Level-two input files
In Level-two (L2), CAVES incorporates search results from the IEDB database of experimentally confirmed epitopes (https://www.iedb.org/) to determine which of the predicted epitopes have experimental validity in literature. 

A search on the IEDB website should be performed for each of the two sequences used for epitope predictions (sequence A and B). 

**Requirements**:
* Amino acid sequence pasted into the ***Linear peptide*** box 
* ***Substring*** option selected from the dropdown menu
&nbsp;

&nbsp;

Each search should use the same parameters for fair comparison, and match the type of epitopes predicted earlier (ie. T cell, B cell, MHC class, etc).
Results can be downloaded as a **CSV** file and uploaded directly into CAVES.

## Multiple sequence alignment file
CAVES uses a multiple sequence alignment (MSA) file to perform an **insertions/deletions** (indel) **search**, as CAVES uses sequence positional data during its comparative process. 

MSA files can be generated with any alignment program that uses the standard dash (-) gap character.
* **MAFFT** online server (https://mafft.cbrc.jp/alignment/server/)  

Results can be downloaded as a **FASTA** file and uploaded directly into CAVES.
&nbsp;

&nbsp;

Sequence order **MUST** be:
1. Sequence A
2. Sequence B
3. IEDB database parent protein(s)

*Hint*: Set MAFFT ***Output order*** parameter to ***Same as input***.
&nbsp;

&nbsp;

**To get the IEDB parent protein sequence**:  
* Within each downloaded IEDB database search results file, navigate to the ***Parent Protein Accession*** column
* Copy the **NCBI accession** number
* Go to the NCBI website ( https://www.ncbi.nlm.nih.gov/)  and **search the accession** to find the corresponding database entry
* Copy/download sequence in **FASTA** format

	
*Hint*: If sequence A and B IEDB queries produce the same parent protein, this only needs to be included in the MSA once.  
If sequence A and B produce different parent proteins, list as ***Sequence A parent protein*** before ***Sequence B parent protein***.

# CAVES optional parameters
## Minimum peptide length
Expects a numeric value indicating the minimum length of amino acids that should be included in CAVES comparisons. Any epitopes that fall below this threshold will be ignored by CAVES.

The IEDB-AR TepiTool sets the epitope length as part of its own parameters.  
The B cell linear epitope prediction tool does not allow users to set prediction length, in which case the CAVES threshold may be applicable.

***Default threshold is one amino acid (i.e. includes all epitopes).***

## Level selection
Choice of running only L1 or L2 rather than the full CAVES comparison.

**L1 only**: compares two files of epitope predictions (no comparison to database search results)
* MSA requires sequence A and sequence B
	
**L2 only**: compares a single file of epitope predictions to a file of database search results
* MSA requires sequence A and database parent protein

***Default setting will run CAVES full analysis (L1 and L2).***

## Results file
Option to name the CAVES results file and choose the directory in which to save it. 

***If left blank, a default name will be assigned and the file will be written in the same directory as the CAVES executable (dist).***

# CAVES output
Results are written as a multi-sheet **.xlsx** file, labelled with the following short-hand naming convention:

**L1** = Level-one results  
**L2** = Level-two results  
**E** = Exact matches  
**P** = Partial matches  
**N** = Novel epitopes  

L2 names will combine the L1 category used for comparison against the database epitopes, along with the L2 category produced as a result.
* Ex. **L1E_L2E** will contain epitopes that found an exact match between sequence A and B in L1, and then found an exact match with a database epitope in L2

For details on matching criteria, please refer to our publication and the associated supplementary materials: Publication pending

# Legal
Copyright 2021 Connor Lowey   
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License at:  
https://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Contact
**Katherine Li**: lik3456@myumanitoba.ca  
**Connor Lowey**: connor.lowey@gmail.com
