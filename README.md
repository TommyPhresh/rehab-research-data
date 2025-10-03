# https://rehab-research.com data pipeline

**Summary**
Pipeline to update, format, and publish the master dataset which serves as the source of truth for the search engine hosted at rehab-research.com

**Process Outline**

(1) Pull raw data from sources (currently we have 35 sources, goal is 60 by Christmas)

(2) Pre-process and generate unique IDs (enables fuzzy matching to prevent duplicate efforts in vectorization; only pull new/updated opportunities)

(3) De-duplicate using unique IDs

(4) Upsert into master dataset

(5) Process into search engine format
    
