# Parameters values from medical reports

In this assessment I will process parameters, values and units found in text data extracted via OCR from laboratory test results or medical records.

## Challenges overcome

- **Managing unstructured text data**: Convert the X1.json file to dictionary mapping synonyms to parameter names.

- **Managing missing and even values**: I have to replace some even values, like replacing "o" by "0" to accurately process number values.

- **Managing duplicate values**: Discarding duplicates using defaultdict(list) function and getting the last value in each array.

- **Find a correct model to process the text data**: My first approach was using NLP, but when I tried to normalize and skip stop words, many words, as well as numeric values were discarded. So, I implement a rule-based model using regular expressions to overcome this challenge. I use 4 regular expressions:

	    Scientific notation: \s+(\d*\.*\d+\s*x10[\*|°]?\d+)\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)
	![Scientific notation](https://i.imgur.com/zB8MZHX.png)

      Range: [\(|\{]?(\d+\.?\d*[-\s]+\d+\.?\d*)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)
	![Range](https://i.imgur.com/JQu8bEV.png)      

      Greater or less: \s+[\(|\{]?([>|<]\s?\d*\.*\d+)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)
	![Greater or less](https://i.imgur.com/lARNd7o.png)

      Number: \s+(\d*\.*\d+)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)
	![Number](https://i.imgur.com/DZ5dWYB.png)


- **Managing validations**: Sometimes a line text passes a regular expression, but I have to make an additional validation, like when I found a parameter's value that it is already included in the parameter name or synonym i.e. I found 27.29 and the synonym is "CA 27.29".

  

  

  

## Remaining challenges

  

- **Tokenize into lines**: I process each line as a token, but I know in the medical reports some commentaries or table-based results are out of the process of each line of text. So, it will be better to elaborate on other tokenization processes.

- **Missing parameters values**: For example in the file **0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt** there is a line with **"Lipase (6-70) U/L 32 29 38"** that should be extracted, but in the X1.json the parameter or synonym **"Lipase"**, literally, is not included, so that value is missing in my solution. These are their following synonym that I should use with other technique process:

		{"Abbreviation": "LPSE", "Synonyms": ["Pancreatic Lipase", "Serum Lipase", "Lipase Enzyme", "Lipolytic Enzyme", "LPSE Test", "Lipase Assay", "Pancreatic Enzyme", "Gastric Lipase", "Digestive Enzyme", "Pancreatic Esterase"]}

## Execution
Run the following command to execute the solution

    python .\parameters-by-test-results.py

> Replace the line 18 with the file text that you want to process. (Now it is "0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt")

## Output example

![Dictionary output](https://i.imgur.com/RC4AOvu.png)


## Tools

- [regex101: build, test, and debug regex](https://regex101.com/)
