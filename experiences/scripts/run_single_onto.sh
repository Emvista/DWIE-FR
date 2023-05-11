
#Run processing DWIE to traduction 

echo "run DWIE FRENCH CORPUS training"
PATH_TRAINING_DATA="../../data/dwie_fr/niv_"

START=$(date +%s)
#convert data to tsv format
i="2"
mkdir -p "../exps/TALN_2023_camembert_base/$i/models/NER/Flair/taggers/sota-ner-flair"
echo "###### Training for experience n°$i #######"
python ../train.py -i $PATH_TRAINING_DATA$i"/" -o "../exps/TALN_2023_camembert_base/$i/models/NER/Flair/taggers/sota-ner-flair/"
echo "###### End of training n°$i #######"


END=$(date +%s)
echo "Training finished!"
echo Execution time was `expr $END - $START` seconds.