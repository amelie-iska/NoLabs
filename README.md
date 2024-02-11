<div align="center" id="top"> 
  <img src="media/NoLabs logo.png" alt="NoLabs" />
</div>

<h1 align="center">NoLabs</h1>
<h2 align="center">Open source biolab</h2>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/BasedLabs/nolabs?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/BasedLabs/nolabs?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/BasedLabs/nolabs?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/BasedLabs/nolabs?color=56BEB8">
</p>

## About ##

NoLabs is an open source biolab with support of web visualisation and hosting.

The goal of the project is to accelerate bio research via making inference models easy to use for everyone. We are currenly supporting protein biolab (predicting useful protein properties such as solubility, localisation, Gene ontology, folding etc.) and drug discovery biolab (construct ligands and test binding to target proteins). 

We are working on expanding both and adding a cell biolab and genetic biolab, and we will appreciate your support and contributions. Let's accelerate bio research!

<img src="media/NoLabs_Architecture.png" width="100%">


## Features ##

**Drug discovery lab (State of the art):**
- Drug-target interaction prediction, high throughput virtual screening (HTVS) based on [uMol](https://github.com/patrickbryant1/Umol)
- Automatic pocket prediction via [P2Rank](https://github.com/rdk/p2rank)
- Automatic MSA generation via [HH-suite3](https://github.com/soedinglab/hh-suite)

<br>
<img src="media/dti.gif" width="100%">

**Protein lab:**

- Prediction of subcellular localisation via fine-tuned [ritakurban/ESM_protein_localization](https://huggingface.co/ritakurban/ESM_protein_localization) model (to be updated with a better model)
- Prediction of folded structure via [facebook/esmfold_v1](https://huggingface.co/facebook/esmfold_v1)
- Gene ontology prediction for 200 most popular gene ontologies
- Protein solubility prediction

<br>
<img src="media/localisation.gif" width="100%">

**Protein design Lab:**
- Protein generation via [RFDiffusion](https://github.com/RosettaCommons/RFdiffusion)

<br>
<img src="media/protein_design.gif" width="100%">

**Conformations Lab:**
- Conformations via [OpenMM](https://github.com/openmm/openmm) and [GROMACS](https://github.com/gromacs/gromacs)

## Starting ##

```bash
# Clone this project
$ git clone https://github.com/BasedLabs/nolabs
```

```bash
$ docker compose up
```
OR if you want to run a single feature

```bash
$ docker compose -up nolabs [gene_ontology|localisation|protein_design|solubility|conformations]
```

Server will be available on http://localhost:9000

## Microservices ##

We also provide an individual docker container backed by FastAPI for each feature. Check /microservices folder. You can use them individually as API.



## Technologies ##

The following tools were used in this project:

- [Pytorch](https://pytorch.org/)
- [Jax](https://jax.readthedocs.io/en/latest/index.html)
- [Transformers](https://huggingface.co/transformers)
- [FastAPI](https://pypi.org/project/Flask/)
- [Docker](https://www.docker.com/)

## Requirements ##

**[Recommended for laptops]** If you are using a laptop, use ```--test``` argument (no need to have a lot of compute):
- RAM > 16GB
- [Optional] GPU memory >= 16GB (REALLY speeds up the inference)

**[Recommended for powerful workstations]** Else, if you want to host everything on your machine and have faster inference:
- RAM > 30GB
- [Optional] GPU memory >= 40GB (REALLY speeds up the inference)

Made by <a href="https://github.com/jaktenstid" target="_blank">Igor</a> and <a href="https://github.com/timurishmuratov7" target="_blank">Tim</a>

&#xa0;

<a href="#top">Back to top</a>
