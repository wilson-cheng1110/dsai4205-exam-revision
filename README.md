# DSAI4205 — Big Data Analytics · Exam Revision

> **PolyU** · Dr. Ken Fong · Semester exam covers **Lectures 1–10**
> Exam = 40% of final grade | Format: 22 MCQ + Long Questions | ~10% programming (RDD only)

---

## 📁 Revision Files — Start Here

| File | What it is | Best used for |
|---|---|---|
| `DSAI4205_Exam_Review.html` | Full interactive notes (L1–L10 + code + summary + Dr. Fong's tips). Collapsible sections, search, dark mode, progress checkboxes. | Active recall — open in browser, tick off topics as you go |
| `DSAI4205_Exam_Review.docx` | Same content as HTML. 1,200+ paragraphs, 57 tables, 208 subsections. Every concept has a green ELI5 plain-English explanation. | Offline reading on phone/tablet, printing |
| `DSAI4205_Exam_Focus.docx` | Dr. Fong's 146 exam review slides extracted + orange "EXAM TIP" callouts from the Apr 11 lecture transcript. Grouped by lecture. | Last-day focused revision — only what's confirmed in scope |
| `DSAI4205_Mock_Exam.docx` | Full mock exam — 22 MCQ + 6 long questions (100 marks total). Blank answer boxes and empty DP tables. | Timed practice under exam conditions |
| `DSAI4205_Mock_Exam_ANSWERS.docx` | Complete answer key with full working shown in green. | Self-marking after the mock |

---

## 🎯 Confirmed Exam Format (Dr. Fong, Apr 11 lecture)

| Component | Details |
|---|---|
| Section A | 22 MCQ, 1 mark each |
| Section B | Long questions — scenario analysis, computation, explanation |
| Programming | ~10% of Section B. **RDD only** — not DataFrame, not SparkSQL |
| Past paper | On BEPA. Note: Sem 1 had 30% programming + L10 in long Q. **This semester is different.** |

### What's in the long question vs MCQ only

| Lecture | Long Q? | MCQ? | Notes |
|---|---|---|---|
| L1 — 6 V's | **YES** | YES | Scenario passage → identify V's + propose solutions. Not bare definitions. |
| L2 — HDFS | Possibly | YES | 3-way replication, fault tolerance |
| L2 — Dask | NO | 1–2 Qs | map_overlap, lazy, chunk size trade-offs |
| L3 — MapReduce | **YES ★** | YES | Mapper → shuffle → reducer. Know intermediate formats. |
| L3 — RDD | **YES (10% prog)** | YES | Revise Tutorial 3. Skeleton with TO-DO gaps. |
| L3/L4 — DataFrame | NO | 3–4 Qs | Catalyst, key ops vs RDD |
| L5 — NLP | **YES** | YES | BPE (vocab size = 10), Levenshtein DP table, stemming vs lemmatization |
| L6 — Embeddings | Conceptual | YES | No equations. Skip-gram vs CBOW ideas, why softmax, M definition. |
| L7 — PageRank | **YES ★** | YES | Build M matrix, power iteration, dead end + spider trap fixes |
| L8 — Graph | **YES ★** | YES | Density, CC, betweenness (vertex only). Edge betweenness **NOT tested**. |
| L9 — NoSQL/CAP | NO | YES | CAP theorem, BASE, strong vs eventual consistency |
| L10 — RecSys | Not this sem | Possibly | Was in long Q Sem 1 — not confirmed this semester |

### Dr. Fong's direct warnings (come up every semester)

| Mistake | Rule |
|---|---|
| Levenshtein DP table | **Source word at TOP (columns). Target word at LEFT (rows).** Wrong orientation = wrong entire question. |
| PageRank adjacency matrix | **Source node at TOP (columns). Destination at LEFT (rows).** Column sums must equal 1. |
| CBOW window size M | M = **half**-window. 2 words each side = M=2, not M=4. |
| MapReduce shuffle | Must mention the **shuffle/sort** step between mapper and reducer. It's automatic but you must describe it. |
| Edge betweenness | **NOT tested.** Only vertex betweenness is in scope. |

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
| L8 | Graph Analytics | Degree, clustering coefficient, closeness/betweenness/harmonic centrality |
| L9 | Big Data Storage / NoSQL | ACID, **CAP theorem**, BASE, strong vs eventual consistency |
| L10 | Recommendation Systems | Collaborative filtering, Matrix Factorization, ALS, RMSE |

---

## 🔑 Must-Know Formulas

```
PageRank:          r = β·M·r + (1−β)/N
Clustering coeff:  C(v) = 2·m_v / (d_v·(d_v−1))
Closeness:         (N−1) / Σ d(v,x)
Harmonic:          Σ 1/d(v,x)   ← use when graph is disconnected
Betweenness:       Σ σ_st(v) / σ_st   ← vertex only
Graph density:     2|E| / N(N−1)
Levenshtein DP:    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                   (if chars match: dp[i][j] = dp[i-1][j-1], no cost)
```

---

## 📖 How to Revise

### Suggested order (time-efficient)
`L7 → L5 → L8 → L3 → L6 → L1 → L9 → L4 → L2 → L10`

### Step-by-step approach

**1. Read `DSAI4205_Exam_Focus.docx` first**
This is Dr. Fong's own review slides with transcript tips attached. Everything in here is confirmed in scope. Start with this before the full notes.

**2. Open `DSAI4205_Exam_Review.html` for active recall**
Use the checkboxes to tick off topics. Use the search bar to find a concept quickly. The red "Exam Format & Dr. Fong's Tips" section at the bottom of the sidebar has the confirmed scope table.

**3. Do the numerical traces from memory**
Cover the answer and redo without looking:
- PageRank power iteration on a 3-node graph (β=0.8, 2 iterations)
- Fill a Levenshtein DP table (e.g. MART → KARMA)
- MapReduce word count: trace mapper → shuffle → reducer outputs
- BPE merge steps until vocabulary reaches size 10
- Clustering coefficient for a given node
- Betweenness centrality for a small graph (vertex only)

**4. Know the "why" for justification questions**
- Why Spark > MapReduce? → in-memory RDD lineage vs disk I/O after every stage
- Why teleportation in PageRank? → fixes spider traps (absorb all rank) and dead ends (rank leaks to zero)
- Why BPE? → handles unknown/rare words by falling back to subword tokens
- Why lemmatization > stemming? → always produces valid English word
- Why AP over CP for social apps? → availability > consistency (Instagram likes can be slightly stale)

**5. Attempt the mock exam under timed conditions**
Open `DSAI4205_Mock_Exam.docx`. Give yourself 2 hours. Then compare against `DSAI4205_Mock_Exam_ANSWERS.docx`.

**6. Revise Tutorial 3 for the programming component (10%)**
Questions are skeleton code with TO-DO gaps — not blank-page coding. Know:
`textFile → flatMap → map → reduceByKey → takeOrdered`

---

## 🧪 Key Code Patterns

### RDD Word Count (T03 — likely exam template)
```python
sc.textFile("file.txt") \
  .flatMap(lambda line: line.lower().split()) \
  .map(lambda w: (w, 1)) \
  .reduceByKey(lambda a, b: a + b) \
  .takeOrdered(5, key=lambda x: -x[1])
```

### Inverted Index (take-home = past exam question)
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

## ⚡ Quick-Start

```bash
# Open interactive notes in browser (no install needed)
start DSAI4205_Exam_Review.html        # Windows
open  DSAI4205_Exam_Review.html        # macOS

# Regenerate DOCX after editing the HTML
pip install python-docx beautifulsoup4
python gen_docx.py

# Regenerate mock exam
pip install python-docx
python gen_mock_exam.py
```

---

*Notes compiled from 10 lectures, 9 tutorial notebooks, 4 tutorial solution PDFs, Dr. Fong's 146-slide exam review deck, and the Apr 11 lecture transcript.*
