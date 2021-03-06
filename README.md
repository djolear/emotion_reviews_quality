# Emotion, Consumer Reviews, and Product Quality

This repository contains code for a project examining the relationship between emotion in Amazon.com reviews and Consumer Reports quality scores.

### Results

For a high-level description of the project and our findings, please [click here](https://github.com/djolear/emotion_reviews_quality/blob/main/results/main.md).

### Dataset Details

To generate this dataset, we collected data from the Consumer Reports website for all products that were likely to be sold on Amazon.com (e.g., excluding cars, washing machines). Next, we created a webscraper to scrape product information and user reviews for these products from Amazon.com.

### Folder Structure

1. The **data_collection** folder contains code for scraping data from Amazon.com and Consumer Reports.
2. The **preprocessing** folder contains code for cleaning the data and preparing it for analyses.
3. The **analysis** folder contains scripts and markdowns showcasing the statistical analyses.
4. The **results** folder contains markdowns that describe our findings.
5. The **plots** folder contains scripts and markdowns for producing visualizations.

### Data Sources

This project uses data from several sources:

1. [Consumer Reports](https://www.consumerreports.org/cro/index.htm)
2. [Amazon.com](https://smile.amazon.com/)
3. [Valence Aware Dictionary for sEntiment Reasoning](https://github.com/cjhutto/vaderSentiment)