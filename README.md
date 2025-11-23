# Stock Forecasting with Sentiment Analysis using LSTM and IndoBERT

This repository explores how **market sentiment** extracted from news or social media can be combined with **time-series models (LSTM, 1D-CNN, Ensemble LSTM+1D-CNN)** to forecast stock price movements in the Indonesian market. Sentiment is computed using **IndoBERT**, while historical price data is modeled with deep learning.

> 🚧 **Status:** Work in progress – code, experiments, and documentation are still being developed.

---

## Table of Contents

- [Background](#background)
- [Project Goals](#project-goals)
- [Approach](#approach)
- [Repository Structure](#repository-structure)
- [Data](#data)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Current & Planned Experiments](#current--planned-experiments)
- [Results](#results)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contact](#contact)

---

## Background

Stock prices are influenced not only by **historical price patterns**, but also by **market sentiment** reflected in news and online text.  
This project aims to:

- Use **IndoBERT** to quantify sentiment from Indonesian texts (e.g. news, articles, or social media).
- Combine sentiment features with **price time-series** to improve short-term stock forecasting.
- Evaluate whether adding sentiment can outperform price-only models.

---

## Project Goals

1. **Build a sentiment analysis pipeline** using IndoBERT for Indonesian financial text.
2. **Train LSTM-based models** for stock price / return prediction.
3. **Fuse sentiment and price features** into a single forecasting model.
4. **Compare performance**:
   - Price-only model vs.
   - Price + sentiment model.
5. Document findings in a clear and reproducible way.

---

## Approach

High-level pipeline:

1. **Data Collection**
   - Scrape or load historical stock prices.
   - Collect related news or text data over the same time range.

2. **Sentiment Analysis (IndoBERT)**
   - Preprocess text (cleaning, tokenization).
   - Use IndoBERT to generate sentiment scores or embeddings.
   - Aggregate sentiment per day (e.g. mean score per day).

3. **Feature Engineering**
   - Time-series features: returns, moving averages, volatility, etc.
   - Sentiment features: daily sentiment score, positive/negative ratio, etc.
   - Align features by date.

4. **Forecasting Model (LSTM)**
   - Use the time-series models to predict next-day price or return.
   - Compare:
     - **Model A:** Only price-based features.
     - **Model B:** Price + sentiment features.
  - Compare all of the time-series models
5. **Evaluation**
   - Metrics such as RMSE, MAE, MAPE (for regression) or accuracy/F1 (for direction).
   - Visualize predictions vs. actuals.

---

## Repository Structure

> Note: Some folders / notebooks are still under development.

```text
Stock-Forecasting-with-sentiment-analysis/
├── Datasets/             # Raw and processed price & text data
├── Figures/              # Plots and visualizations (performance, comparisons, etc.)
├── Investment-Strategies/# Notebooks/notes on trading or investment strategies (optional)
├── Model/                # LSTM and related modeling notebooks/scripts
├── Publications/         # Reports, writeups, or paper drafts
├── Scrapping/            # Scripts or notebooks for data scraping
├── Sentiment-Analysis/   # IndoBERT sentiment notebooks and utilities
└── README.md             # Project documentation (this file)
