# https://rehab-research.com data pipeline

**Summary**
Pipeline to update, format, and publish the master dataset which serves as the source of truth for the search engine hosted at rehab-research.com

**Process Outline**
    * Pull raw data from sources (currently we have 35 sources, goal is 60 by Christmas)
    * Pre-process and generate unique IDs (enables fuzzy matching to prevent duplicate efforts in vectorization; only pull new/updated opportunities)
    * De-duplicate using unique IDs
    * Upsert into master dataset
    * Process into search engine format

