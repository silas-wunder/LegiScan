# Analysis of Legiscan Legislation Data

## An application of machine leaning to real world data

Legiscan has catalogued all bills that have been introduced in any body of legislature, both state and federal, since approximately 2009. They also retain all information about how any members of that legislative body voted on bills, as well as some basic information about those representatives. This dataset has a lot of interesting information to provide, and the point of this project is to extract as much of that interesting information as possible.

The first thing that must be done is sourcing the data, which is done with a basic Python script: [downloader.py](https://github.com/silas-wunder/LegiScan/blob/master/downloader.py). This only needs to be done once a week (and in fact, running it more often will result in the API key being blacklisted by LegiScan's system), as LegiScan only updates their datasets weekly. Along with the actual data, the downloader saves the change hashes of each dataset as well as the base64 representation of the zip files. This allows the script to avoid redownloading the same material, and if any data is lost after downloading is complete, it can easily be re-extracted without having to make another API call.

Once the data is fully downloaded and extracted, we run a basic cleaning script that extracts the interesting information about each bill, voting session, and person, while dropping the rest. This, along with aggressive compression algorithms, allows us to reduce the dataset from over 18GB to under 200MB. This drops most of the superfluous and duplicated information and keeps only things that will be interesting from an analysis point of view.

Lastly, the data is fed into an analysis notebook, [basic_analysis.ipynb](https://github.com/silas-wunder/LegiScan/blob/master/basic_analysis.ipynb) where we analyze (crazy, I know) it. This analysis includes basic similarity metrics, both from pure votes and from BERTopic driven topic clustering. The analysis is discussed more in depth there.

This project still has a long ways to go before it can possibly be considered finished, and even then it will never be complete. The government introduces, votes on, and passes new bills every single day, meaning that this project needs to be updated as often as possible. Before that can happen, the topic and sentiment analysis portion must be upgraded to deal with the full dataset, instead of just a small subset. The topics should be easy enough to gather, as this information is included in the raw LegiScan data. Sentiment analysis will be harder to scale, as this process is very time consuming and costly, and we will need to devote days of GPU time to the task. On top of that, the data needs to be put into an easy to read format that allows the general public to access this information, as right now it's just in Jupyter Notebooks, which pose a fairly high barrier to entry for anyone not well versed in Python. This will most likely come in the form of a website, but that is of the least importance, mostly because designing websites is not our _forte_.
