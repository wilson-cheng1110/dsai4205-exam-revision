# DSAI4205 — Big Data Analytics · Exam Revision

> **PolyU** · Dr. Ken Fong · Semester exam covers **Lectures 1–10**
> Exam = 40 % of final grade | Format: MCQ + Long Questions

---

## 📚 What's in this repo

| File / Folder | Description |
|---|---|
| `DSAI4205_Exam_Review.html` | **Start here** — full colour-coded exam notes, sticky nav, print-to-PDF ready |
| `DSAI4205_Exam_Review.docx` | Same content formatted for Word / direct printing |
| `make_docx.py` | Python script that regenerates the `.docx` from scratch (python-docx) |
| `Tutorial_1…9_*.ipynb` | Official tutorial notebooks (Pandas → Dask → Spark → NLP → PageRank → RecSys) |
| `LT1…LT10.pptx` | Original lecture slides |
| `T01…T04 Solution.pdf` | Tutorial solution PDFs |
| `data/` | Sample datasets (TSV, CSV) used in tutorials |

---

## 🗂 Course Topics (Lectures 1–10)

| # | Topic | Key Concepts |
|---|---|---|
| L1 | Introduction to Big Data | **6 V's**: Volume, Velocity, Variety, Veracity, Value, Variability |
| L2 | Path to Parallelism | MapReduce, HDFS (3-way replication, write-once), Dask |
| L3 | Apache Spark | RDD, DataFrame, Catalyst, lazy eval, narrow vs wide transforms |
| L4 | Hive / SparkSQL | Parquet vs ORC vs CSV, Data Lake vs Data Warehouse |
| L5 | NLP Basics | Tokenization, Stemming, Lemmatization, BPE, Levenshtein distance |
| L6 | LLMs & Word Embeddings | Word2Vec (Skip-gram, CBOW), Negative Sampling (SGNS) |
| L7 | Link Analysis | PageRank, power iteration, Google Matrix (β≈0.85), dead ends, spider traps |
| L8 | Graph Analytics | Degree, clustering coefficient, closeness/betweenness/harmonic centrality, BFS |
| L9 | Big Data Storage / NoSQL | ACID, **CAP theorem**, BASE, strong vs eventual consistency |
| L10 | Recommendation Systems | Collaborative filtering, Matrix Factorization, ALS, RMSE |

---

## ⚡ Quick-Start: Open the Exam Notes

```bash
# In your browser — no install needed
open DSAI4205_Exam_Review.html        # macOS
start DSAI4205_Exam_Review.html       # Windows
xdg-open DSAI4205_Exam_Review.html   # Linux
```

To regenerate the `.docx` after edits:
```bash
pip install python-docx
python make_docx.py
```

---

## 🔑 Must-Know Formulas (quick ref)

```
PageRank:           r = [βM + (1−β)(1/N)J] · r        β ≈ 0.85
PageRank (sparse):  r^(t+1) = β·M·r^t + (1−β)/N
Clustering coeff:   C(v) = 2·m_v / (d_v·(d_v−1))
Closeness:          (N−1) / Σ d(v,x)
Betweenness:        Σ σ_st(v) / σ_st
Skip-gram prob:     exp(u_o^T · v_c) / Σ_w exp(u_w^T · v_c)
Levenshtein DP:     dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
Matrix factorize:   R ≈ U·V^T  →  r̂_ui = u_i^T · v_j
```

---

## 🗂 Revision Priority (if time is short)

1. 6 V's of Big Data with examples
2. PageRank formula + power iteration + dead ends vs spider traps
3. CAP theorem — CP (RDBMS) vs AP (NoSQL) with real examples
4. Spark: RDD ops, transformations vs actions, narrow vs wide
5. Centrality formulas (closeness, betweenness, harmonic)
6. Skip-gram vs CBOW (input/output/embeddings used)
7. Levenshtein distance DP table
8. Collaborative vs content-based filtering + ALS
9. ACID vs BASE; strong vs eventual consistency
10. MapReduce 5 steps + word count; HDFS characteristics

---

## 🧪 Tutorial Code Patterns

### Word Count (T03)
```python
textRDD.flatMap(lambda x: x.split()) \
       .map(lambda x: (x.lower(), 1)) \
       .reduceByKey(add) \
       .sortBy(lambda x: x[1], ascending=False) \
       .collect()
```

### Inverted Index
```python
lines.flatMap(lambda l: [(w, l.split("||")[0].strip())
                          for w in l.split("||")[1].strip().split()]) \
     .distinct().groupByKey().mapValues(sorted).sortByKey()
```

### ALS Recommender (T09)
```python
from pyspark.ml.recommendation import ALS
als = ALS(maxIter=5, regParam=0.01,
          userCol="userId", itemCol="movieId", ratingCol="rating")
model = als.fit(training)
```

---

## 📋 Environment

- Python 3.11
- PySpark 3.x
- Dask
- NLTK / spaCy (NLP tutorials)
- `python-docx` (for regenerating the review `.docx`)

---

*Exam notes compiled from all 10 lectures, 9 tutorial notebooks, and 4 tutorial solution PDFs.*
