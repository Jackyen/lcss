# lcss



# How to use this program
## Required
* you need to install python3
* use command `pip3 install requirements.txt`  install the package
* put your dataset  near the main.py

## Excute
* python3 main.py [function] [length]
** function means lcss(step1) or lcss2(step2)
** length is belong to lcss2 , means how many cluster it read 
Ex. 
```
## execute the first step
python. main.py lcss   

## execute
python. main.py lcss2 3   
```

## Explain
* lcss
  * need to prepare dataset
  * and its output will be located in `out` folder
* lcss2 
  * need to put your cluster in to `in` folder
  * and naming convension should be 0.csv, 2.csv, etc. 