
#Run processing DWIE to traduction 

echo "run DWIE FRENCH CORPUS training"
PATH_TRAINING_DATA="../../data/dwie_fr/niv_"

START=$(date +%s)
#convert data to tsv format
for i in {4..1};  
    do (  

        mkdir -p "./TALN_2023_camembert-base/$i/models/NER/Flair/taggers/sota-ner-flair"
        echo "###### Training for experience n°$i #######"
        python train.py -i $PATH_TRAINING_DATA$i"/bio_V2" -o "./TALN_2023_camembert-base/$i/models/NER/Flair/taggers/sota-ner-flair/"
        echo "###### End of training n°$i #######"

     )
done

END=$(date +%s)
echo "Training finished!"
echo Execution time was `expr $END - $START` seconds.