cd ../tener/src/
. python/bin/activate
python extract_entities_ru.py --input ../../ner-comparison/eval.tagged.txt --output ../../ner-comparison/eval.tagged.tener.txt
deactivate
cd ../../ner-bert/
. python/bin/activate
python predict.py --input_file ../ner-comparison/eval.tagged.txt --output_file ../ner-comparison/eval.tagged.ner-bert.txt
deactivate
cd ../Slavic-BERT-NER/
. python/bin/activate
python predict.py --input_file ../ner-comparison/eval.tagged.txt --output_file ../ner-comparison/eval.tagged.slavic-bert.txt
deactivate

cd ../ner-comparison/
echo "Comparing bert-ner predictions to the reference taglist"
python compare-files.py eval.tagged.txt eval.tagged.ner-bert.txt
echo "Comparing tener predictions to the reference taglist"
python compare-files.py eval.tagged.txt eval.tagged.tener.txt
echo "Comparing slavic-bert predictions to the reference taglist"
python compare-files.py eval.tagged.txt eval.tagged.slavic-bert.txt