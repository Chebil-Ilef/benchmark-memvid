
# Ingestion & Retrieval Benchmark: Memvid (vs FAISS classic RAG)

## Dataset Collections

| Collection                | # PDFs | Avg Pages | Total Size |
| ------------------------- | ------ | --------- | ---------- |
| **Short (Radar)**         | 5      | \~10      | 5.4 MB     |
| **Long (BEAM Reports)**   | 21     | 200–300+  | 366.2 MB   |
| **Certificates (Energy)** | 7      | \~5       | 2.4 MB     |

---

## Summary Table of Results

| Category            | Memvid Time | Memvid Size | FAISS Time | FAISS Size |
| ------------------- | ----------- | ----------- | ---------- | ---------- |
| Short (Radar)       | 45.8 sec    | 9.59 MB     | 5.11 sec   | 0.57 MB    |
| Long (BEAM Reports) | \~2.75 hrs  | 192.8 MB    | 868.8 sec  | 41.24 MB   |
| Energy Certificates | 38.6 sec    | 3.70 MB     | 4.00 sec   | 0.45 MB    |

---


## Full Details:  Ingestion Benchmark

### **Short Collection (Radar PDFs)**

#### Memvid

* Chunks per PDF:

  * radar1: 70
  * radar2: 117
  * radar3: 16
  * radar4: 41
  * radar5: 47
* Total Chunks: 291
* Ingestion Time: `4.45 sec`
* Video Build Time: `41.35 sec`
* Output Size: `4.79 MB`

**Total Time:** `45.80 sec`
**Total Disk Usage:** `9.59 MB`

#### FAISS

* Chunks per PDF:

  * radar1: 67
  * radar2: 112
  * radar3: 15
  * radar4: 40
  * radar5: 45
* Total Chunks: `279`
* Ingestion Time: `4.56 sec`
* Embedding + Indexing: `0.55 sec`
* Output Size: `0.57 MB`

**Total Time:** `5.11 sec`
**Total Disk Usage:** `0.57 MB`

---

### **Long Collection (BEAM Reports)**

#### Memvid

* Total Chunks: `~21,000`
* Ingestion Time: `686.70 sec`
* Video Build Time: **`2:03:00` (hh\:mm\:ss)**
* Output Size Estimate: `~192.8 MB`

#### FAISS

* Ingestion Time: `835.88 sec`
* Embedding + Indexing: `32.93 sec`
* Output Size: `41.24 MB`
* Chunks per PDF: \~700–1000 per file

**Total Time:** `868.81 sec`
**Disk Usage:** `41.24 MB`

---

### **Energy Certificates**

#### Memvid

* Total Chunks: `225`
* Ingestion Time: `3.40 sec`
* Video Build Time: `35.15 sec`
* Output Size: `3.70 MB`

**Total Time:** `38.55 sec`
**Disk Usage:** `3.7 MB

#### FAISS

* Ingestion Time: `3.32 sec`
* Embedding + Indexing: `0.68 sec`
* Output Size: `0.45 MB`
* Total Chunks: `213`

**Total Time:** `4.00 sec`
**Disk Usage:** `0.45 MB`

---

## Full Details : Retrieval Performance

### Short Collection

#### Memvid

* Total Queries: `21`
* Avg Query Time: `71.29 ms`
* Time Range: `55.23 – 221.47 ms`
* **Limitations:**

  * No similarity scores returned
  * Chunks often cut off mid-word
  * No support for reranking or threshold filtering

BUT from inspection : the quality of chunks are very poor , they are cut off at words letters

=> IMPLEMENTED MY MANUAL SCORES EVALUATION, here is a sample


[query] 'How does the EU's risk assessment approach for crypto services differ from Germany’s national FATF compliance measures?' 
[similarity ranking (preview chunk ...)]
  1. Score: 0.653 | e (EU) 2015/849 (4th Anti-Money Laundering Directive, Dataset 849)and now also the ...
  2. Score: 0.622 | d considered in the enterprise-wide risk assessment, policies, and procedures in accordance...
  3. Score: 0.611 | nd the information requirements set out in Regulation (EU) 2023/1113 for previous ...
  4. Score: 0.586 | to Guideline 15: Sector-specific guideline for investment firms IX. Amendments to Guideline...
  5. Score: 0.553 | , new technologies or distribution channels are used, or the business relationship was ...

notice how at the start of each chunk it's cutoff

[query] 'What new entities are being established by the Financial Crime Prevention Act in German' (repetitions: 3)
[similarity ranking (preview chunk ...)] 
  1. Score: 0.541 | dations of the Financial Action Task Force (FATF). Overall, the Act aims to strengthen the...
  2. Score: 0.541 | Financial Crime Prevention Act Abbreviation (standard) FKBG Abbreviation FKBG Implementation...
  3. Score: 0.540 | ng Supervision (ZfG) and - the establishment of a competence center for training and ...
  4. Score: 0.535 | ; - creation of a central office for money laundering supervision (ZfG) and https://normen...
  5. Score: 0.534 | ndment to the Banking Act (KWG) (Article 16) VIII. Amendment to the Money Laundering Act...

low similarities 

### Energy Certificates

#### Memvid

* Total Queries: `21`
* Avg Query Time: `71.72 ms`
* Time Range: `46.89 – 260.67 ms`

Example Query:

[query] 'How does the calculated energy demand differ from the recorded energy consumption in the building?' 
[similarity ranking (preview chunk ...)] 
  1. Score: 0.421 | ion*) 70% chauffage gaz naturel 12 285 (12285 é.f.) entre 690€ et 950€ eau chaude 20% gaz ...
  2. Score: 0.413 | es (oder: "Registriernummer wurde beantragt am ...") Energiebedarf CO -Emissionen 3 kg/m²...
  3. Score: 0.412 | es (oder: "Registriernummer wurde beantragt am ...") Energiebedarf CO -Emissionen 3 2 kg/...
  4. Score: 0.409 | 0 3 (oder: „Registriernummer wurde beantragt am...“) Endenergieverbrauch Endenergieverbrau...
  5. Score: 0.399 | Primärenergiebedarf erneuerbar 5.307 kWh/a PEBern.,SK 24,4 kWh/m²a Kohlendioxidemissionen ...

[query] 'What are the HT' values for the building envelope and how do they compare to the EnEV limits?' 
[similarity ranking (preview chunk ...)] 
  1. Score: 0.374 | es (oder: "Registriernummer wurde beantragt am ...") Energieverbrauch A+ A B C D E F G H 0...
  2. Score: 0.372 | ive possible (réalisation du pack avant le pack ). Faites-vous accompagner par un professi...
  3. Score: 0.366 | issen Verschärfter Anforderungswert führen können. Insbesondere wegen standardisierter Ran...
  4. Score: 0.360 | . der Energieeinsparverordnung (EnEV) vom ¹ 18.11.2013 Registriernummer ² SH-2022-00400842...
  5. Score: 0.356 | . der Energieeinsparverordnung (EnEV) vom ¹ 18.11.2013 Registriernummer ² 3 Erfasster Ener...



