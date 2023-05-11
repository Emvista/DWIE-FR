# DWIE-FR
DWIE-FR : A new French dataset annotated with named entities


In this repository, you will find a folder `preprocessing` to reproduce our work to reproduce french dwie corpus. In the second folder, `experiences`you will find our scripts to train and evaluate our models on DWIE-FR dataset using `Flair` framework.

## Download DWIE-FR dataset
<p>link: <a>https://drive.google.com/drive/folders/1A4Q8B3VIo64Iz5pto4_3csk_5eTwZ09C?usp=share_link</a></p>

## Reproducing our works
### Preprocessing

#### Packages installation
* python=3.10

```
conda env create --file environment.yml
```
#### Run preprocessing
```
cd preprocessing
./run.sh
```


### Training Flair models on DWIE-FR

#### Packages installation
* python=3.10

```
conda env create --file environment.yml
```
#### Run preprocessing
```
cd experiences
./scripts/run_onto_dwie.sh
```
* cf [DWIE-FR/experiences/README.md](experiences/README.md), please check the readme to get more details

