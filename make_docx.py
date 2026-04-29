from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)

# ── Style helpers ─────────────────────────────────────────────────────────
BLUE  = RGBColor(0x25, 0x63, 0xEB)
PURP  = RGBColor(0x7C, 0x3A, 0xED)
DARK  = RGBColor(0x1E, 0x29, 0x3B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LGREY = RGBColor(0xF1, 0xF5, 0xF9)
DKBLU = RGBColor(0x1E, 0x3A, 0x5F)

def set_cell_bg(cell, rgb_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), rgb_hex)
    tcPr.append(shd)

def cover():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('DSAI4205 — Big Data Analytics\nExam Review Notes')
    run.bold = True
    run.font.size = Pt(22)
    run.font.color.rgb = DKBLU
    doc.add_paragraph('PolyU · Dr. Ken Fong · Lectures 1–10 · Exam = 40% of grade\n'
                       'Format: Multiple Choice + Long Questions').alignment \
        == WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(f'  {text}  ')
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = WHITE
    # shade paragraph
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '2563EB')
    pPr.append(shd)

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = BLUE

def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = PURP

def body(text, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(indent * 0.5)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    p.add_run(text).font.size = Pt(9.5)

def bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent  = Cm(0.5 + level * 0.5)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    p.add_run(text).font.size = Pt(9.5)

def code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.5)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '1E293B')
    pPr.append(shd)

def callout(label, text, colour='DBEAFE', text_colour=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    run = p.add_run(f'{label}  {text}')
    run.font.size = Pt(9)
    if text_colour:
        run.font.color.rgb = text_colour
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), colour)
    pPr.append(shd)

def table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    hdr = t.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_bg(cell, '2563EB')
        run = cell.paragraphs[0].add_run(h)
        run.bold = True; run.font.size = Pt(8.5)
        run.font.color.rgb = WHITE
    for r, row_data in enumerate(rows):
        for c, val in enumerate(row_data):
            cell = t.rows[r+1].cells[c]
            if (r % 2) == 1:
                set_cell_bg(cell, 'F8FAFC')
            run = cell.paragraphs[0].add_run(str(val))
            run.font.size = Pt(8.5)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph()

def pg():
    doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
cover()

# ─────────────────────────────────────────────────────────────────────────
h1('L1 · Introduction to Big Data Analytics')

h2('The 6 V\'s of Big Data')
table(
    ['V', 'Definition', 'Example'],
    [
        ['Volume',      'Data amount — growing exponentially',                           '6.4B smartphone subscriptions (2022)'],
        ['Velocity',    'Speed of generation AND processing',                            '16.4B Google searches/day; real-time stock ticks'],
        ['Variety',     'Diversity of types (structured, semi-structured, unstructured)','Text, video, sensor logs, JSON, CSV simultaneously'],
        ['Veracity',    'Quality, accuracy, trustworthiness of data',                   'Measurement errors, human errors, inconsistent sources'],
        ['Value',       'Business usefulness; longer processing = less value',           'Not all collected data has business worth'],
        ['Variability', 'How fast/extent data changes; same word, multiple meanings',   'Netflix prefs shift when new releases drop'],
    ],
    [2.2, 6.5, 6.5]
)

h2('Types of Analytics')
table(
    ['Type', 'Question', 'Example'],
    [
        ['Descriptive',  'What happened?',       'Sales report last quarter'],
        ['Diagnostic',   'Why did it happen?',   'Root-cause analysis of churn'],
        ['Predictive',   'What will happen?',    'Demand forecasting'],
        ['Prescriptive', 'What should we do?',   'Route optimisation recommendation'],
    ],
    [2.5, 4, 8.7]
)

callout('★ Netflix case study:', 'Map 4 Vs to Netflix challenges (Volume→Spark storage, Velocity→Spark Streaming, Variety→SparkSQL, Veracity→validation+ML)', 'DBEAFE')

# ─────────────────────────────────────────────────────────────────────────
h1('L2 · The Path to Parallelism')

h2('MapReduce Steps')
for i, s in enumerate([
    'Input: bag of (key, value) pairs',
    'Map: each worker processes chunk, emits intermediate (key, value) pairs',
    'Shuffle: group all intermediate pairs by key → same reducer',
    'Reduce: aggregate values per key into final result',
    'Output: write final (key, value) pairs to storage',
], 1):
    bullet(f'Step {i}: {s}')

h2('Word Count (classic MapReduce)')
code('Map:    ("doc", "hello world hello") → [("hello",1),("world",1),("hello",1)]\nShuffle: ("hello",[1,1]), ("world",[1])\nReduce: ("hello",2), ("world",1)')

h2('HDFS')
bullet('Fixed-size block partitioning (default 128 MB)')
bullet('3-way replication across 3 separate nodes (fault tolerance)')
bullet('Write-once, read-many — files are immutable once written')
bullet('NameNode: master (stores metadata); DataNode: worker (stores blocks)')

h2('MapReduce vs Spark')
table(
    ['MapReduce', 'Spark'],
    [
        ['Writes intermediate to disk (slow)',      'Keeps data in memory (10–100× faster for iterative)'],
        ['Only Map + Reduce primitives',            'Rich 100+ operation library'],
        ['No iterative algorithm support',          'Efficient for ML, graph, streaming'],
    ],
    [8, 7.2]
)

h2('Dask')
bullet('Python-native parallel computing — extends NumPy/Pandas beyond RAM')
bullet('Lazy evaluation: builds task graph, executes only on .compute()')
bullet('Block algorithms: splits computation into chunks')
callout('Chunk size:', '100 MB – 1 GB per chunk recommended. Rechunking is expensive — choose upfront.', 'FFFBEB')

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('L3 · Apache Spark — RDDs & DataFrames')

h2('Core Concepts')
table(
    ['Concept', 'Description'],
    [
        ['RDD',              'Resilient Distributed Dataset — immutable, distributed, fault-tolerant via lineage, lazy'],
        ['DataFrame',        'Named-column structure; optimised by Catalyst; lazy; supports StructType/ArrayType/MapType'],
        ['Lazy evaluation',  'Transformations build a DAG; nothing executes until an Action is called'],
        ['Data lineage',     'Record of all operations to rebuild an RDD — enables fault recovery without replication'],
        ['Immutability',     'Cannot modify an RDD; always produce a new one'],
    ],
    [3.5, 11.7]
)

h2('Transformations vs Actions')
table(
    ['Category', 'Description', 'Examples'],
    [
        ['Transformation (lazy)',  'Returns new RDD/DF; no compute yet', 'map, filter, flatMap, join, union, reduceByKey, groupByKey, distinct, sortBy, cartesian, subtract, intersection'],
        ['Action (eager)',         'Triggers execution; returns value or writes', 'collect, count, show, save, first, take(n), takeOrdered, min, max, sum, mean, stdev'],
    ],
    [3.5, 5, 6.7]
)

h2('Narrow vs Wide Transformations')
table(
    ['', 'Narrow', 'Wide (Shuffle)'],
    [
        ['Mapping',    '1 input partition → 1 output partition', 'Multiple partitions → output partitions'],
        ['Network',    'No shuffle needed',                      'Network communication required'],
        ['Examples',   'filter, map, flatMap',                   'groupByKey, sortBy, join, reduceByKey'],
        ['Cost',       'Fast; pipelines stages',                 'Expensive; stage boundary in DAG'],
    ],
    [3, 6.5, 5.7]
)

h2('Key RDD Operations (quick reference)')
table(
    ['Op', 'What it does', 'Example result'],
    [
        ['map(f)',            'Apply f to every element',                       '[1,2,3] → [2,3,4]'],
        ['flatMap(f)',        'Like map but flatten output (1 level)',           '["a b","c"] → ["a","b","c"]'],
        ['filter(f)',         'Keep elements where f is True',                  '[1,2,3] filter x>2 → [3]'],
        ['reduceByKey(f)',    'Aggregate values with same key',                 '[(a,1),(a,2)] → [(a,3)]'],
        ['mapValues(f)',      'Apply f to values only; key unchanged',          '[(a,2)] → [(a,4)]  (f=x²)'],
        ['groupByKey()',      'Group values by key into iterable',              '[(a,1),(a,2)] → [(a,[1,2])]'],
        ['join(rdd2)',        'Inner join on key',                              '[(3,a)] join [(3,b)] → [(3,(a,b))]'],
        ['leftOuterJoin()',   'All keys from left; None for missing right',     '[(1,a)] → [(1,(a,None))]'],
        ['subtractByKey()',   'Keys in left not in right',                      '[(1,a),(3,b)] − [(3,c)] → [(1,a)]'],
        ['cartesian()',       'All pairs (A × B)',                              '[1,2]×[3] → [(1,3),(2,3)]'],
        ['union()',           'Combine all elements (keeps dupes)',             '[1,2]∪[3] → [1,2,3]'],
        ['intersection()',   'Only shared elements',                           '[1,2,3]∩[2,3,4] → [2,3]'],
        ['distinct()',        'Remove duplicates',                              '[1,1,2] → [1,2]'],
        ['sortBy(f)',         'Sort by key function',                           'sortBy value descending'],
        ['randomSplit([w])',  'Split RDD by weights (e.g. train/test)',         '[0.8, 0.2]'],
        ['takeOrdered(n)',    'Smallest n elements (or custom key)',            '[10,1,2,9] → [1,2]'],
        ['collect()',         '★ ACTION: return all as Python list',           'triggers computation'],
        ['count()',           '★ ACTION: number of elements',                  '3'],
        ['first()',           '★ ACTION: first element',                       '21'],
        ['take(n)',           '★ ACTION: first n elements',                    '[21,1]'],
    ],
    [3.5, 6, 5.7]
)

h2('DataFrame Key Operations')
table(
    ['Op', 'SQL equivalent', 'Note'],
    [
        ['select(col)',              'SELECT col',      'Projection'],
        ['filter() / where()',       'WHERE',           'Row filtering'],
        ['groupBy().agg()',          'GROUP BY + agg',  'Aggregation'],
        ['join(df2, condition)',     'JOIN',            'Combine two DFs'],
        ['orderBy() / sort()',       'ORDER BY',        'Sort rows'],
        ['withColumn(name, expr)',   '(computed col)',  'Add or replace column'],
        ['drop(col)',                '—',               'Remove column'],
        ['printSchema()',            'DESCRIBE',        'Show column types'],
    ],
    [4, 3.5, 7.7]
)

h2('Catalyst Optimizer')
bullet('DataFrame operations build an Abstract Syntax Tree (AST) of the logical plan')
bullet('Catalyst rewrites plan: predicate pushdown, column pruning, join reordering')
bullet('Pushes .where() filters BEFORE joins → reads less data → faster')
callout('Why DataFrames > RDDs:', 'Catalyst optimises queries automatically. RDDs execute exactly as written.', 'ECFDF5')

h2('SparkSession Setup')
code('from pyspark.sql import SparkSession\nss = SparkSession.builder\\\n     .master("local[4]")   # local[x]: x = CPU threads\n     .appName("MyApp")\\\n     .getOrCreate()\nspark = ss.sparkContext  # for RDD operations')

h2('Nested Data Types in DataFrames')
table(
    ['Type', 'Description', 'Example'],
    [
        ['StructType', 'Named fields (sub-record)',  'address: {city:"HK", zip:"000"}'],
        ['ArrayType',  'List of values',             'tags: ["big","data"]'],
        ['MapType',    'Key-value map',              'attrs: {height:170, weight:65}'],
    ],
    [3, 6, 6.2]
)

h2('Inverted Index (Take-Home Exercise)')
body('Classic IR structure: word → sorted list of document IDs containing it')
code('# Input: "D1 || word1 word2 word3"\nlines = spark.textFile("docs.txt")\ninv_index = lines\\\n  .flatMap(lambda line: [\n      (word, line.split("||")[0].strip())\n      for word in line.split("||")[1].strip().split()\n  ])\\\n  .distinct()\\\n  .groupByKey()\\\n  .mapValues(lambda docs: sorted(list(docs)))\\\n  .sortByKey()')

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('L4 · Hive, Shark & SparkSQL')

h2('Data Formats Comparison')
table(
    ['Format', 'Type', 'Best for'],
    [
        ['CSV',     'Row, text',       'Human-readable; slow analytics'],
        ['JSON',    'Semi-structured', 'Flexible schema; verbose'],
        ['Parquet', 'Columnar, binary','Analytics — column pruning + compression (preferred)'],
        ['ORC',     'Columnar, binary','Hive; great compression'],
        ['Avro',    'Row, binary',     'Streaming + schema evolution'],
    ],
    [2.5, 3.5, 9.2]
)

h2('Hive vs SparkSQL')
table(
    ['', 'Hive', 'SparkSQL'],
    [
        ['Execution engine', 'MapReduce (slow)', 'Spark in-memory (fast)'],
        ['Latency',          'High (minutes)',   'Low (seconds)'],
        ['Iterative queries','Poor',             'Excellent'],
        ['Use case',         'Batch ETL',        'Interactive + batch analytics'],
    ],
    [3.5, 5.5, 6.2]
)

h2('Data Lake vs Data Warehouse')
table(
    ['', 'Data Lake', 'Data Warehouse'],
    [
        ['Schema',      'Schema-on-read (flexible)',  'Schema-on-write (strict)'],
        ['Data',        'Raw, all formats',           'Cleaned, structured'],
        ['Ingestion',   'Fast, all data welcome',     'Slow (ETL required)'],
        ['Query speed', 'Slower (must infer schema)', 'Faster (pre-optimised)'],
        ['Risk',        '"Data swamp" without governance', 'Stale if ETL pipeline breaks'],
    ],
    [3, 5.5, 6.7]
)

# ─────────────────────────────────────────────────────────────────────────
h1('L5 · Natural Language Processing (NLP)')

h2('Text Preprocessing Pipeline')
for i, s in enumerate([
    'Data Cleaning: remove HTML, punctuation, numbers, special characters',
    'Tokenization: split text into tokens (words, subwords, or chars)',
    'Stop Word Removal: remove high-frequency, low-info words (a, an, the, is...)',
    'Stemming / Lemmatization: reduce words to root form',
    'POS Tagging: label each token (noun, verb, adjective...)',
    'Feature Extraction: convert text to numerical representation',
], 1):
    bullet(f'{i}. {s}')

callout('⚠ Stop words risk:', 'Blindly removing stop words destroys "President of University of Hong Kong", "Let it be", "flights to London". Use Named Entity Recognition (NER) to protect phrases first.', 'FFFBEB')

h2('Stemming vs Lemmatization')
table(
    ['', 'Stemming', 'Lemmatization'],
    [
        ['Method',   'Chop suffixes by rules',          'Dictionary lookup for root (lemma)'],
        ['Result',   'May NOT be a real word',           'Always a valid dictionary word'],
        ['Speed',    'Faster',                           'Slower (needs POS context)'],
        ['Example',  '"computational" → "comput"',       '"am/are/is" → "be"'],
        ['Algorithm','Porter Stemmer (5 phases)',        'WordNet Lemmatizer'],
    ],
    [3, 6, 6.2]
)

h2('Porter\'s Stemmer — 5 Phases')
table(
    ['Phase', 'Rules / Examples'],
    [
        ['1', 's → ∅ (cats→cat), sses→ss (classes→class), ies→i (companies→compani)'],
        ['2', 'ational→ate (relational→relate), tional→tion (conditional→condition)'],
        ['3', 'icate→ic (triplicate→triplic), alize→al (formalize→formal)'],
        ['4', '(m>1)ement→∅ (replacement→replac), ment→∅, ent→∅, ion→∅ (if preceded by s/t)'],
        ['5', 'Remove trailing e (probate→probat), double consonant cleanup'],
    ],
    [1.5, 13.7]
)

h2('Levenshtein (Edit) Distance')
bullet('Minimum single-character edits (insert, delete, substitute) to transform string s → t')
code('Recurrence:\n  if s[i]==t[j]:  dp[i][j] = dp[i-1][j-1]          (match, no cost)\n  else:           dp[i][j] = 1 + min(\n                      dp[i-1][j],    # delete from s\n                      dp[i][j-1],    # insert into s\n                      dp[i-1][j-1]   # substitute\n                  )\nExample: "kitten" → "sitting" = 3 edits (k→s, e→i, insert g)')

h2('Byte Pair Encoding (BPE) — Subword Tokenization')
for i, s in enumerate([
    'Split all words into individual characters',
    'Count all adjacent symbol pairs in corpus',
    'Merge the most frequent pair into a new symbol; add to vocabulary',
    'Repeat until desired vocabulary size (or no more frequent pairs)',
    'Token Segmenter uses vocab to encode new sentences; Token Merger decodes back',
], 1):
    bullet(f'{i}. {s}')
body('Handles rare/OOV words gracefully. Used in GPT, BERT.')

h2('Feature Representations')
table(
    ['Method', 'Description', 'Limitation'],
    [
        ['One-Hot Encoding', 'Word → binary vector of vocab size; only its position=1', 'Sparse; no semantic similarity'],
        ['Bag of Words',     'Count occurrences of each word; stop words removed',      'Word ORDER is lost; sparse'],
        ['TF-IDF',           'TF × log(N/DF) — weights by rarity across docs',          'Still no word order'],
    ],
    [3.5, 7, 4.7]
)

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('L6 · LLMs & Word Embeddings (Word2Vec)')

h2('Skip-gram vs CBOW')
table(
    ['', 'Skip-gram', 'CBOW'],
    [
        ['Input',       'Center word',                      'Context words (averaged)'],
        ['Output',      'Predict surrounding context words','Predict center word'],
        ['Better for',  'Rare words',                       'Frequent words'],
        ['Speed',       'Slower to train',                  'Faster to train'],
        ['Embeddings',  'Input vectors v_c preferred',      'Context vectors V_o used as embeddings'],
    ],
    [3, 6, 6.2]
)

h2('Skip-gram: Objective Function')
code('Maximize:  Σ_t  Σ_{-m≤j≤m, j≠0}  log P(o | c)\n\nP(o | c) = exp(u_o^T · v_c)  /  Σ_w exp(u_w^T · v_c)\n\n  v_c  = input embedding of center word c (from matrix V)\n  u_o  = output embedding of context word o (from matrix U)\n  Denominator = softmax over entire vocabulary (expensive for large vocab)')

h2('Skip-gram Assumptions')
bullet('Window independence: each context word predicted independently given center word')
bullet('Position independence: word order within window does not matter')

h2('CBOW: Loss Function')
code('Input:  x = (1/2m) Σ v_w  for w in context window of size m\n\nP(c | context) = exp(u_c^T · x)  /  Σ_w exp(u_w^T · x)\n\nLoss: minimize  NLL = -log P(c | context)\n\nNote: context vectors V_o are the final word embeddings in CBOW')

h2('Skip-gram with Negative Sampling (SGNS)')
code('y = 1  for real (center, context) pairs\ny = 0  for k randomly sampled noise pairs\n\nLoss = -[ log σ(u_o^T v_c)  +  Σ_k log σ(-u_k^T v_c) ]\n\nσ(x) = 1 / (1 + e^(-x))    (sigmoid)\n\nWhy: converts expensive softmax (50k-class) into cheap binary classifiers')

h2('Word2Vec → Transformers (conceptual)')
bullet('Word2Vec: static embeddings — one vector per word regardless of context')
bullet('BERT/GPT: contextual embeddings — same word has different vector per sentence')
bullet('Attention: model looks at all positions simultaneously (no fixed window)')

# ─────────────────────────────────────────────────────────────────────────
h1('L7 · Link Analysis — PageRank')

h2('Core Idea')
body('A page is important if important pages link to it. PageRank distributes "rank" along edges until convergence.')

h2('Stochastic Adjacency Matrix M')
code('M[j][i] = 1 / out_degree(i)   if edge i → j exists\nM[j][i] = 0                   otherwise\n\nColumns sum to 1 (column-stochastic).\nPageRank vector r satisfies:  r = M · r  (eigenvector with eigenvalue 1)')

h2('Problems & Fixes')
table(
    ['Problem', 'Cause', 'Fix'],
    [
        ['Dead Ends',     'Node with no outgoing edges — absorbs rank',          'Treat as linking to all N pages uniformly (teleport)'],
        ['Spider Traps',  'Group linking only to each other — traps all rank',   'Random teleport with probability (1−β)'],
    ],
    [2.8, 7, 5.4]
)

h2('Google Matrix')
code('A = β · M  +  (1−β) · [1/N]_{N×N}\nr = A · r\n\nβ ∈ [0.8, 0.9]  — damping factor\n(1−β)           — teleport probability\n\nInterpretation: prob β → follow a link; prob (1−β) → jump to random page')

h2('Power Iteration (Algorithm)')
for i, s in enumerate([
    'Initialise: r = [1/N, 1/N, …, 1/N]',
    'Multiply: r_new = A · r',
    'Repeat until ||r_new − r||₁ < ε (converges ~50 iterations on web graph)',
], 1):
    bullet(f'{i}. {s}')

h2('Efficient Sparse Formula (Tutorial 7)')
code('Avoids dense N×N matrix:\n  r^(t+1) = β · M · r^t  +  (1−β)/N\n\nPySpark implementation:\n  contribs = adj_list.join(ranks).flatMap(\n      lambda (url, (links, rank)): [(link, rank/len(links)) for link in links]\n  )\n  ranks = contribs.reduceByKey(add).mapValues(\n      lambda r: beta*r + (1-beta)/N\n  )')

h2('Worked Example (3-node graph)')
code('Nodes: A, B, C\nEdges: A→B, A→C, B→C, C→A\n\n      A    B    C\nM = [ 0    0    1  ]   (who points TO A)\n    [1/2   0    0  ]   (who points TO B)\n    [1/2   1    0  ]   (who points TO C)\n\nStart: r = [1/3, 1/3, 1/3]^T\nIter 1: M·r = [1/3, 1/6, 1/2]^T  → apply Google Matrix with β=0.85\n...(iterate until convergence)')

callout('★ Exam question type:', 'Given a small graph, build M by hand, run 1–2 power iterations, identify dead ends / spider traps.', 'DBEAFE')

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('L8 · Graph Analytics')

h2('Graph Basics')
table(
    ['Term', 'Definition', 'Formula'],
    [
        ['Degree d(v)',       'Number of edges incident to v',                  '—'],
        ['Average Degree',    'Mean degree across all nodes',                   '2|E| / N'],
        ['Graph Density',     'Fraction of possible edges that exist',          '2|E| / (N(N−1))'],
        ['Distance d(u,v)',   'Edges on shortest path between u and v',         'BFS'],
        ['Diameter',          'Maximum shortest-path distance in graph',        'max over all pairs d(u,v)'],
        ['Avg Path Length',   'Average distance between all node pairs',        'mean of all d(u,v)'],
    ],
    [3.5, 6.5, 5.2]
)

h2('Clustering Coefficient')
code('C(v) = 2·m_v / (d_v · (d_v − 1))\n\nm_v  = edges between v\'s neighbors\nd_v  = degree of v\nRange [0,1]:  1 = all neighbors connected; 0 = none')

h2('Centrality Measures')
table(
    ['Measure', 'Formula', 'Limitation'],
    [
        ['Closeness',    'C_clos(v) = (N−1) / Σ_x d(v,x)',              'Undefined for disconnected graphs'],
        ['Harmonic',     'C_harm(v) = Σ_{x≠v} 1/d(v,x)',               'Handles disconnected (unreachable → 0)'],
        ['Betweenness',  'BC(v) = Σ_{s≠t} σ_st(v) / σ_st',            'O(VE) to compute; expensive'],
        ['Eigenvector',  'x_v = (1/λ) Σ_{u∈N(v)} x_u',               'Ill-defined for disconnected graphs'],
    ],
    [3, 6.5, 5.7]
)
body('σ_st = total shortest paths from s to t; σ_st(v) = those passing through v')

h2('Betweenness — Worked Example')
body('Key insight: high betweenness = "bridge" node. Removing it fragments the network.')
code('Linear chain: A–B–C–D–E with shortcut B–D\nBC(B) sums contributions from all (s,t) pairs where s≠B≠t:\n  (A,C): only path A→B→C; σ(B)=1/1 = 1.0\n  (A,D): shortest A→B→D; σ(B)=1/1 = 1.0\n  (A,E): only path A→B→D→E; σ(B)=1/1 = 1.0\n  (C,E): C→D→E; does not pass B; σ(B)=0\n  Add all pairs → BC(B)')

h2('Graph Connectivity')
bullet('Connected graph: path exists between every pair of nodes')
bullet('Giant component: largest connected subgraph (contains most nodes in social/web graphs)')
bullet('BFS (Breadth-First Search) used to find connected components and shortest paths')
code('BFS from s:\n  1. Mark s visited, enqueue\n  2. While queue not empty:\n       u = dequeue\n       for each neighbour v of u not yet visited:\n           mark visited; distance[v] = distance[u]+1; enqueue v')

h2('Degree Distribution & Network Types')
table(
    ['Network type', 'Degree distribution', 'Properties', 'Examples'],
    [
        ['Random',      'Bell curve (Poisson)',   'Uniform connectivity',                  'Erdős–Rényi model'],
        ['Small-World', 'Bell curve',             'Short paths + high clustering coefficient','Social networks'],
        ['Scale-Free',  'Power law P(k)~k^(−γ)', 'Few hubs with very high degree; heavy tail','WWW, citations'],
    ],
    [3, 4, 5, 3.2]
)

# ─────────────────────────────────────────────────────────────────────────
h1('L9 · Big Data Storage & NoSQL')

h2('ACID Properties')
table(
    ['Property', 'Meaning'],
    [
        ['Atomicity',    'All operations succeed or none (all-or-nothing)'],
        ['Consistency',  'DB moves between valid states; all rules enforced'],
        ['Isolation',    'Concurrent transactions execute as if sequential'],
        ['Durability',   'Committed transactions survive system failure'],
    ],
    [3.5, 11.7]
)

h2('CAP Theorem')
body('In a distributed system you can guarantee AT MOST 2 of 3:')
table(
    ['Letter', 'Meaning'],
    [
        ['C — Consistency',          'Every read returns most recent write (or error)'],
        ['A — Availability',         'Every request gets a non-error response (may be stale)'],
        ['P — Partition Tolerance',  'System operates despite dropped/delayed messages between nodes'],
    ],
    [4, 11.2]
)
table(
    ['Choose', 'Give Up', 'Typical System'],
    [
        ['C + P', 'Availability (during partition)',  'MySQL, PostgreSQL, HBase, Zookeeper → RDBMS'],
        ['A + P', 'Consistency (may return stale)',   'Cassandra, DynamoDB, CouchDB → NoSQL'],
        ['C + A', 'Partition tolerance (impossible)', 'Single-machine RDBMS only'],
    ],
    [2, 5, 8.2]
)
callout('Key rule:', 'Network partitions WILL happen. Real distributed systems choose C vs A. CA = theoretical only.', 'FEF2F2')

h2('Strong vs Eventual Consistency')
table(
    ['', 'Strong Consistency', 'Eventual Consistency'],
    [
        ['Guarantee', 'Read after write always returns new value; all nodes in sync', 'Converges over time; reads may be temporarily stale'],
        ['Latency',   'Higher; may block writes',                                     'Lower; always writable'],
        ['Used by',   'RDBMS (CP systems)',                                           'NoSQL (AP systems)'],
    ],
    [3, 6, 6.2]
)

h2('BASE Model (NoSQL alternative to ACID)')
table(
    ['Letter', 'Stands for', 'Meaning'],
    [
        ['B', 'Basically Available', 'System always acknowledges requests (may return stale data)'],
        ['S', 'Soft State',          'State can change over time even without new input (propagation)'],
        ['E', 'Eventually Consistent','Reaches consistency once all propagation completes'],
    ],
    [1.5, 3.5, 10.2]
)

h2('NoSQL Data Models')
table(
    ['Type', 'Structure', 'Examples', 'Use case'],
    [
        ['Key-Value',    '{key: value}',          'Redis, DynamoDB',    'Sessions, caching'],
        ['Document',     'JSON/BSON documents',   'MongoDB, CouchDB',   'Content, catalogs'],
        ['Column-Family','Rows + column families', 'Cassandra, HBase',  'Time-series, analytics'],
        ['Graph',        'Nodes + edges',          'Neo4j',             'Social networks, recommendations'],
    ],
    [3, 4, 4, 4.2]
)

h2('Partitioning vs Replication Trade-offs')
table(
    ['Strategy', 'Improves', 'Hurts'],
    [
        ['Partitioning (sharding)', 'Write performance',                     'Reads that join across partitions (expensive)'],
        ['Replication',             'Fault tolerance + read performance',    'Write performance (must update all replicas)'],
    ],
    [4, 5, 6.2]
)

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('L10 · Recommendation Systems')

h2('Two Main Approaches')
table(
    ['', 'Content-Based Filtering', 'Collaborative Filtering (CF)'],
    [
        ['Basis',        'Item features (genre, tags, director)',   'User behaviour (ratings matrix only)'],
        ['Data needed',  'Item metadata',                           'Other users\' ratings'],
        ['Cold start',   'Bad for new users; OK for new items',     'Bad for BOTH new users and new items'],
        ['Problem',      'Limited novelty (filter bubble)',         'Sparsity — most users rate very few items'],
    ],
    [3.5, 6, 5.7]
)

h2('Collaborative Filtering — User-Based vs Item-Based')
table(
    ['', 'User-Based CF', 'Item-Based CF'],
    [
        ['Idea',        'Find similar users; recommend what they liked',     'Find similar items to those user rated'],
        ['Similarity',  'Between users (row vectors)',                       'Between items (column vectors)'],
        ['Stability',   'User prefs change → less stable',                  'Item characteristics stable → more stable'],
        ['Scale',       'Costly as users grow',                             'Pre-compute item-item matrix (Amazon\'s approach)'],
    ],
    [3, 6, 6.2]
)

h2('Similarity Metrics')
code('Cosine Similarity:\n  sim(u,v) = (u·v) / (||u|| · ||v||)\n  Range [-1,1]; 1=identical direction, 0=orthogonal, -1=opposite\n\nPearson Correlation (mean-centred):\n  sim(u,v) = Σ(r_ui − r̄_u)(r_vi − r̄_v) / (σ_u · σ_v)\n  Adjusts for harsh vs generous raters')

h2('Matrix Factorization (ALS)')
code('Decompose ratings matrix R ≈ U · V^T\n  U = (users × k)  latent user matrix\n  V = (items × k)  latent item matrix\n  k = number of latent factors (50–200)\n\nPrediction: r̂_ui = u_i^T · v_j\n\nObjective: minimize Σ(r_ui − u_i^T v_j)² + λ(||U||²+||V||²)\n  optimised with ALS (Alternating Least Squares) or SGD')

h2('ALS Algorithm Steps')
for i, s in enumerate([
    'Initialise U and V with random values',
    'Fix V, solve for U (least squares on each user row)',
    'Fix U, solve for V (least squares on each item column)',
    'Repeat steps 2–3 until loss converges',
], 1):
    bullet(f'{i}. {s}')

h2('ALS in PySpark (Tutorial 9)')
code('from pyspark.ml.recommendation import ALS\nfrom pyspark.ml.evaluation import RegressionEvaluator\n\n(training, test) = data.randomSplit([0.8, 0.2], seed=1234)\nals = ALS(maxIter=5, regParam=0.01,\n          userCol="userId", itemCol="movieId", ratingCol="rating")\nmodel = als.fit(training)\npredictions = model.transform(test)\nrmse = RegressionEvaluator(metricName="rmse", labelCol="rating",\n    predictionCol="prediction").evaluate(predictions)\nprint("RMSE:", rmse)')

h2('Evaluation Metrics')
table(
    ['Metric', 'Formula', 'Measures'],
    [
        ['RMSE',         '√(Σ(r̂−r)²/n)',              'Prediction accuracy (lower=better)'],
        ['MAE',          'Σ|r̂−r|/n',                   'Mean absolute error'],
        ['Precision@K',  'Relevant in top-K / K',        'What fraction of recommendations are good?'],
        ['Recall@K',     'Relevant in top-K / total rel','Did we find all the good items?'],
    ],
    [3, 4, 8.2]
)

h2('Challenges')
table(
    ['Challenge', 'Description', 'Fix'],
    [
        ['Cold Start',     'New user/item has no ratings',           'Ask for initial prefs; use item content'],
        ['Sparsity',       'Ratings matrix >99% empty',              'Matrix factorization (ALS)'],
        ['Scalability',    'Millions of users × millions of items',  'Approximate nearest neighbours; distributed ALS'],
        ['Filter Bubble',  'Only recommends what\'s similar',        'Inject serendipitous recommendations'],
    ],
    [3, 5.5, 6.7]
)

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('Tutorial Code Reference (T01–T04)')

h2('T01 — Pandas Essentials')
code('# Read TSV\ndf = pd.read_csv("data.tsv", delimiter="\\t")\n\n# Filter + sort\ndf[(df["gender"]=="F") & (df["year"]>1990)].sort_values("year", ascending=False)\n\n# Merge\nmerged = pd.merge(left=df, right=ratings,\n                  left_on=["userID","movieID"], right_on=["userID","movieID"])\n\n# Groupby mean\nmerged.groupby("name")[["rating"]].mean().sort_index()\n\n# Missing values\ndf.fillna("-")                 # replace NaN\ndf.dropna(axis=0)              # drop any-NaN rows\ndf.dropna(subset=["col"])      # drop where specific col is NaN\n\n# df["col"]   → Series (1D)\n# df[["col"]] → DataFrame (2D)')

h2('T02 — Dask')
code('import dask.array as da\narr = da.random.normal(20, 0.1, size=(20000,20000), chunks=(10000,10000))\narr.mean(axis=0).compute()\n\n# Dask DataFrame\nddf[~ddf["Cancelled"]].groupby("Origin").Origin.count().compute()\nddf.groupby("DayOfWeek").DepDelay.mean().idxmax().compute()\n\n# map_partitions (apply func to each pandas partition)\nmeta = pd.Series(name="Distance", dtype="float64")\nddf.Distance.map_partitions(lambda df: df*1.60934, meta=meta)')

h2('T03 — Spark RDD (Word Count, DNA, Palindrome)')
code('# Word count\ntextRDD.flatMap(lambda x: x.split())\\\n       .map(lambda x: (x.lower(),1))\\\n       .reduceByKey(add)\\\n       .sortBy(lambda x: x[1], ascending=False)\\\n       .collect()\n\n# DNA k-mer counting (k=5)\ndef generatePattern(line, k):\n    return [(line[i:i+k],1) for i in range(len(line)-k+1)]\ndnaRDD.flatMap(lambda l: generatePattern(l,5)).reduceByKey(add)\\\n      .sortBy(lambda x: x[1], ascending=False)\n\n# Palindrome filter\nseqRDD.filter(lambda x: x[1]>1)\\\n      .filter(lambda x: x[0]==x[0][::-1])\\\n      .collect()')

h2('T04 — Spark SQL / DataFrame')
code('from pyspark.sql import Row\nfrom pyspark.sql.functions import col, when\n\n# RDD → DataFrame\nrdd.map(lambda x: Row(sequence=x[0], count=x[1])).toDF()\n\n# Read CSV\ndf = ss.read.csv("file.txt", header=True, inferSchema=True)\n\n# Computed columns\ndf = df.withColumn("avg_time", (col("time")+col("timef"))/2)\ndf = df.withColumn("level",\n    when(col("score")<200,"Easy")\n    .when(col("score")<350,"Moderate")\n    .otherwise("Difficult"))\n\n# Aggregate + sort\ndf.groupby("name").avg("speed").sort("avg(speed)", ascending=False).show(5)\n\n# Union (same schema)\ncombined = df1.union(df2)\n\n# TF (term frequency per document)\ntf = tokenized.flatMapValues(lambda x: x).countByValue()\n# DF (document frequency — how many docs contain each term)\ndoc_freq = tokenized.flatMapValues(lambda x: x).distinct()\\\n                    .map(lambda x:(x[1],x[0])).countByKey()')

# ─────────────────────────────────────────────────────────────────────────
pg()
h1('★ Quick Reference — Formulas, Comparisons & Last-Minute Priority')

h2('Must-Know Formulas')
table(
    ['Topic', 'Formula'],
    [
        ['Average graph degree',         '2|E| / N'],
        ['Graph density',                '2|E| / (N(N−1))'],
        ['Clustering coefficient',       'C(v) = 2m_v / (d_v(d_v−1))'],
        ['Closeness centrality',         '(N−1) / Σ d(v,x)'],
        ['Harmonic centrality',          'Σ_{x≠v} 1/d(v,x)'],
        ['Betweenness centrality',       'Σ_{s≠t} σ_st(v) / σ_st'],
        ['PageRank (Google Matrix)',      'r = [βM + (1−β)(1/N)J] · r'],
        ['PageRank (sparse efficient)',   'r^(t+1) = β·M·r^t + (1−β)/N'],
        ['Skip-gram probability',        'exp(u_o^T v_c) / Σ_w exp(u_w^T v_c)'],
        ['SGNS loss',                    '−[log σ(u_o^T v_c) + Σ_k log σ(−u_k^T v_c)]'],
        ['Levenshtein recurrence',       'dp[i][j] = 1 + min(dp[i−1][j], dp[i][j−1], dp[i−1][j−1])'],
        ['Matrix factorization',         'R ≈ U·V^T;  r̂_ui = u_i^T · v_j'],
        ['Cosine similarity',            '(u·v) / (||u||·||v||)'],
    ],
    [5.5, 9.7]
)

h2('Key Comparisons')
table(
    ['A', 'vs', 'B', 'Key difference'],
    [
        ['Stemming',          'vs', 'Lemmatization',        'Stem may not be real word; lemma always is'],
        ['Skip-gram',         'vs', 'CBOW',                 'Skip: center→context; CBOW: context→center'],
        ['Narrow transform',  'vs', 'Wide transform',       'Wide requires network shuffle'],
        ['Transformation',    'vs', 'Action (Spark)',       'Transformation is lazy; action triggers execution'],
        ['ACID',              'vs', 'BASE',                 'ACID = strict; BASE = eventual consistency'],
        ['CP system',         'vs', 'AP system',            'CP sacrifices availability; AP sacrifices consistency'],
        ['Content-based',     'vs', 'Collaborative filter', 'Content: item features; CF: user behaviour'],
        ['Strong consistency','vs', 'Eventual consistency', 'Strong: always up-to-date; Eventual: converges over time'],
        ['RDD',               'vs', 'DataFrame',            'DF optimised by Catalyst; RDD is lower-level'],
        ['Data Lake',         'vs', 'Data Warehouse',       'Lake: raw schema-on-read; Warehouse: structured schema-on-write'],
        ['map()',             'vs', 'flatMap()',             'flatMap flattens one level of nested lists'],
        ['User-based CF',     'vs', 'Item-based CF',        'User prefs change; item characteristics are stable'],
    ],
    [3.8, 0.8, 3.8, 6.8]
)

h2('CAP Theorem Cheat Sheet')
table(
    ['Choose', 'Give Up', 'Typical System'],
    [
        ['C + A', 'P',  'Single-machine RDBMS (theoretical)'],
        ['C + P', 'A',  'MySQL, PostgreSQL, HBase, Zookeeper'],
        ['A + P', 'C',  'Cassandra, DynamoDB, CouchDB'],
    ],
    [2.5, 2.5, 10.2]
)

h2('Last-Minute Revision Priority')
for i, s in enumerate([
    '6 V\'s with examples (especially Veracity and Value)',
    'PageRank: Google Matrix formula, power iteration, dead ends vs spider traps',
    'CAP theorem — which systems are CP vs AP and why',
    'Centrality formulas: closeness, harmonic, betweenness (with example)',
    'Spark: all RDD ops, transformations vs actions, narrow vs wide',
    'Skip-gram vs CBOW (input/output, what embeddings are used)',
    'SGNS — why negative sampling, sigmoid function',
    'Levenshtein distance — DP table recurrence',
    'Collaborative vs content-based filtering + ALS steps',
    'ACID vs BASE; strong vs eventual consistency',
    'BPE tokenization steps',
    'Porter\'s stemmer 5 phases with example rules',
    'MapReduce 5 steps + word count example',
    'HDFS: 3-way replication, write-once, fixed-size blocks',
    'Inverted index — flatMap + groupByKey pattern',
], 1):
    bullet(f'{i:2d}. {s}')

# ── Save ──────────────────────────────────────────────────────────────────
out = r'C:\Users\User\Downloads\4205\DSAI4205_Exam_Review.docx'
doc.save(out)
print(f'Saved to: {out}')
