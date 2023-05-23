
# #Run processing DWIE to traduction 

echo "run processing traduction DWIE to FRENCH CORPUS"

     
#convert data to tsv format
echo "convert data to tsv format"
for i in {1..4};  
    do (  
        echo "$i"
        PATH_SAVER="../data/dwie_fr/$i/"
        PATH_DATA="../data/dwie/annos_with_content"
        PATH_SAVER_TRANSLATE="../data/dwie_fr/$i/translate_v1/"
        PATH_FINAL_SPLIT="../data/dwie_fr/$i/split_official_eval_v2/"
        mkdir -p $PATH_SAVER_TRANSLATE 
        mkdir -p $PATH_FINAL_SPLIT
        
        echo "preprocess english data to tsv data and remove footer and none from ontologie"
        python preprocessing.py -i $PATH_DATA -o $PATH_SAVER -d $i
        
        echo "remove footer"
        python remove_footer.py -i $PATH_SAVER'train.txt' -b $PATH_SAVER'train.txt' -o $PATH_SAVER'train_without_footer_none.txt' -d $i -r True
        python remove_footer.py -i $PATH_SAVER'test.txt' -b $PATH_SAVER'test.txt' -o $PATH_SAVER'test_without_footer_none.txt' -d $i -r True
        
        echo "convert to english tsv data to bio format"       
        python convert_to_bio.py -i $PATH_SAVER'test_without_footer_none.txt' -o $PATH_SAVER'test_without_footer_none_bio.txt'
        python convert_to_bio.py -i $PATH_SAVER'train_without_footer_none.txt' -o $PATH_SAVER'train_without_footer_none_bio.txt'
     )
done

echo "preprocessing Alignment V1"

for i in {1..4};  
    do (  
        echo "$i"
        PATH_SAVER="../data/dwie_fr/$i/"
        PATH_DATA="../data/dwie/annos_with_content"
        PATH_SAVER_TRANSLATE="../data/dwie_fr/$i/translate_v1/"
        PATH_FINAL_SPLIT="../data/dwie_fr/$i/split_official_eval_v2/"
        
        if (($i!=1)); then
        # La traduction reste la meme du coup je copie vers les autres fichiers pour ne pas perdre de temps a relancer la trad
        cp ../data/dwie_fr_deep_V3/1/translate_v1/train_fr.txt ../data/dwie_fr_deep_V3/1/translate_v1/test_fr.txt $PATH_SAVER_TRANSLATE
        elif (($i==1)); then
        echo "translate data"
        python translate.py -i $PATH_SAVER -o $PATH_SAVER_TRANSLATE
        fi
        echo "align english entities to french tsv annotation"
        
        echo "Alignment V1"

        python align.py -i $PATH_SAVER -o $PATH_SAVER_TRANSLATE

        echo "remove footer and none and theirs child class from entities"
        python remove_footer.py -i $PATH_SAVER'train.txt' -b $PATH_SAVER_TRANSLATE'train_fr_NER.txt'  -o $PATH_SAVER_TRANSLATE'train_fr_NER_without_footer_none.txt' -d $i
        python remove_footer.py -i $PATH_SAVER'test.txt' -b $PATH_SAVER_TRANSLATE'test_fr_NER.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_without_footer_none.txt' -d $i

        echo "convert data to BIO format"
        python convert_to_bio.py -i $PATH_SAVER_TRANSLATE'train_fr_NER_without_footer_none.txt' -o $PATH_SAVER_TRANSLATE'train_fr_NER_without_footer_none_bio.txt'
        python convert_to_bio.py -i $PATH_SAVER_TRANSLATE'test_fr_NER_without_footer_none.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_without_footer_none_bio.txt'
        

        if (($i==4)); then
        echo "dictionary construction into V4 for V2 the V4 dictionary is built once it takes time due to the translation, then it is adapted to the level of ontologies cf the script dict_to_onto..._levels_..."
        python prepare_data_to_align.py -i $PATH_SAVER -o $PATH_SAVER_TRANSLATE
        elif (($i==1)); then
        echo "construction of the dictionary only on the last and finest ontology and then adapt it to the others"
        fi
    )
done

echo "Alignment V2"
for i in {4..1};  
    do (
        echo "$i"
        PATH_SAVER="../data/dwie_fr/$i/"
        PATH_DATA="../data/annos_with_content"
        PATH_SAVER_TRANSLATE="../data/dwie_fr/$i/translate_v1/"
        PATH_FINAL_SPLIT="../data/dwie_fr/$i/split_official_eval_v2/"
        
        echo "Adapting the onto 4 dictionary to higher level ontologies"
        python dict_to_ontology_levels.py -i $PATH_SAVER_TRANSLATE -d $i
        echo "annoter avec le dictionnaire post_processing Alignment"
        python dictionnary_group_search_post_processing_alignment.py -i $PATH_SAVER_TRANSLATE'train_fr_NER.txt' -b $PATH_SAVER_TRANSLATE'train_fr.txt' -o $PATH_SAVER_TRANSLATE'train_fr_NER_V2.txt' -j $PATH_SAVER_TRANSLATE'train_fr_NER.json'
        python dictionnary_group_search_post_processing_alignment.py -i $PATH_SAVER_TRANSLATE'test_fr_NER.txt' -b $PATH_SAVER_TRANSLATE'test_fr.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_V2.txt' -j $PATH_SAVER_TRANSLATE'test_fr_NER.json'
        
        echo "Annotate the dictionary file by applying a post processing of the articles"
        python post_processing_alignment_articles.py -i $PATH_SAVER_TRANSLATE'train_fr_NER_V2.txt' -b $PATH_SAVER_TRANSLATE'train_fr.txt' -o $PATH_SAVER_TRANSLATE'train_fr_NER_V2_articles.txt' -d $i
        python post_processing_alignment_articles.py -i $PATH_SAVER_TRANSLATE'test_fr_NER_V2.txt' -b $PATH_SAVER_TRANSLATE'test_fr.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_V2_articles.txt' -d $i


    )
done

echo "post processing V3 + remove the footers and add a Bio version"
for i in {1..4};  
    do (
        echo "$i"
        PATH_SAVER="../data/dwie_fr/$i/"
        PATH_DATA="../data/annos_with_content"
        PATH_SAVER_TRANSLATE="../data/dwie_fr/$i/translate_v1/"
        PATH_FINAL_SPLIT="../data/dwie_fr/$i/split_official_eval_v2/"
        
        
        echo "post processing annotate the equivalent of ontology 4 in level $i to avoid articles('le, la,les etc...') being annotated when they are between two different entities in onto 4"
        if (($i!=4)); then
        python last_ontologie_to_generique.py -i $PATH_SAVER_TRANSLATE'train_fr_NER_V2_articles.txt'  -b $PATH_SAVER_TRANSLATE'train_fr.txt' -d $i -o $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles.txt' -j $PATH_SAVER_TRANSLATE'train_fr_NER.json' -o4 '../data/dwie_fr/4/translate_v1/train_fr_NER_V2_articles.txt'
        python last_ontologie_to_generique.py -i $PATH_SAVER_TRANSLATE'test_fr_NER_V2_articles.txt' -b $PATH_SAVER_TRANSLATE'test_fr.txt' -d $i -o $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles.txt' -j $PATH_SAVER_TRANSLATE'test_fr_NER.json' -o4 '../data/dwie_fr/4/translate_v1/test_fr_NER_V2_articles.txt'
        elif (($i==4)); then
        echo "No need to use the script because it's level 4 here (the last ontology level) last_ontologie_to_generique"
        cp $PATH_SAVER_TRANSLATE'test_fr_NER_V2_articles.txt' $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles.txt'
        cp $PATH_SAVER_TRANSLATE'train_fr_NER_V2_articles.txt' $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles.txt'
        fi

        echo "remove footer and none (and theirs child class) from entities "
        python remove_footer.py -i $PATH_SAVER'test.txt' -b $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles_without_footer_none.txt' -d $i
        python remove_footer.py -i $PATH_SAVER'train.txt' -b $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles.txt'  -o $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles_without_footer_none.txt' -d $i
        echo "convert txt file to BIO format"
        python convert_to_bio.py -i $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles_without_footer_none.txt' -o $PATH_SAVER_TRANSLATE'train_fr_NER_V3_articles_without_footer_none_bio.txt'
        python convert_to_bio.py -i $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles_without_footer_none.txt' -o $PATH_SAVER_TRANSLATE'test_fr_NER_V3_articles_without_footer_none_bio.txt'


    )
done


echo "build tree arborescence folder for google drive"
for i in {1..4};  
    do (
        echo "$i"
        PATH_SAVER_DRIVE="../data/drive-corpus-dwie-fr/sans_footer_none/niv_$i/"
        mkdir -p $PATH_SAVER_DRIVE 
        mkdir -p $PATH_SAVER_DRIVE"anglais/bio/"
        
        mkdir -p $PATH_SAVER_DRIVE"bio_V1/"
        mkdir -p $PATH_SAVER_DRIVE"bio_V2/"
        mkdir -p $PATH_SAVER_DRIVE"V1_without_bio/"
        mkdir -p $PATH_SAVER_DRIVE"V2_without_bio/"

        PATH_SAVER_TRANSLATE="../data/dwie_fr"
        PATH_ORIGIN="../data/dwie_fr"
        cp $PATH_ORIGIN"/$i/test_without_footer_none.txt" $PATH_ORIGIN"/$i/train_without_footer_none.txt" $PATH_SAVER_DRIVE"anglais"
        cp $PATH_ORIGIN"/$i/test_without_footer_none_bio.txt" $PATH_ORIGIN"/$i/train_without_footer_none_bio.txt" $PATH_SAVER_DRIVE"anglais/bio/"


        cp $PATH_ORIGIN"/$i/translate_v1/train_fr_NER_without_footer_none_bio.txt" $PATH_ORIGIN"/$i/translate_v1/test_fr_NER_without_footer_none_bio.txt" $PATH_SAVER_DRIVE"bio_V1/"
        cp $PATH_ORIGIN"/$i/translate_v1/test_fr_NER_without_footer_none.txt" $PATH_ORIGIN"/$i/translate_v1/train_fr_NER_without_footer_none.txt" $PATH_SAVER_DRIVE"V1_without_bio/"

        cp $PATH_ORIGIN"/$i/translate_v1/test_fr_NER_V3_articles_without_footer_none_bio.txt" $PATH_ORIGIN"/$i/translate_v1/train_fr_NER_V3_articles_without_footer_none_bio.txt" $PATH_SAVER_DRIVE"bio_V2/"
        cp $PATH_ORIGIN"/$i/translate_v1/test_fr_NER_V3_articles_without_footer_none.txt" $PATH_ORIGIN"/$i/translate_v1/train_fr_NER_V3_articles_without_footer_none.txt" $PATH_SAVER_DRIVE"V2_without_bio/" 

    )
done

echo "Preprocessing Done! Ready for training!"
