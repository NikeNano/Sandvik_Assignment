# Sandvik_DataScience_TakeHome

The Code @ Sandvik take home assignment

My solution to the following problem:https://github.com/sandvikcode/data-science-take-home

## Structured of the workflow/jupyter notebooks

![alt tag]((https://github.com/NikeNano/Sandvik_Assignment/tree/master/figures/workflow.png "Figure illustrating the workflow")
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


1. Webscraping and downloading the files(zip files), also create a csv file for the preprocessing scrip - web_download_prepare.ipynb
2. R script for feature extraction from the .wav files. - sound_feature.R
3. Some further feature extraction and transformation, also some visualisation of the data. - visualisng_preprocessed_data.ipynb
4. Modelling and futher understanding of the data. - Predictive modelling.ipynb
5. Bokeh application for interactive plots and visualisation of the data - bokeh_app 
6. PDF report done in latex (online editor).

## Folders:
- Backup, this is a backup of some of the notebooks
- bokeh_app, the folder for the data visualisation application
- demo, contains an mp4 showing how the data visualisation application works
- figures, some figures used for the report
- html_notebooks, the notebooks in html, for cheking out the code
- models, the pickled models that where developed

## Requirements
The python requirements is in the requirements.txt, for R seawave and tuneR is used and required. 

## Run interactive visualisation

```
bokeh serve --show bokeh_app
```

## Report
See data-science-home.pdf 

/Niklas
