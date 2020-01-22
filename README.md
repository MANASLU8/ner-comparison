## Compare performance of NER engines
To start comparison  
```sh
python compare.py --reference_file eval.tagged.txt --hypotheses_dir .
```
The script will consider that recognition results are stored in files having names like `eval.target.ner-bert.txt` or `eval.ner-bert.target.txt` if the reference file's name is `eval.tagged.txt`.
![sample-results](https://raw.githubusercontent.com/MANASLU8/ner-comparison/master/images/sample-results.jpg)
To replace labels in all files:  
```sh
sed -i ':a;N;$!ba;s/Loc\n/Location\n/g' */*.txt
```