# Teknikat e Painformuara të Kërkimit (Uninformed Search Techniques)

## Përmbajtja

- [1. Social Golfers Problem](#1-social-golfers-problem)
- [2. Modelimi](#2-modelimi)
- [3. Reprezentimi](#3-reprezentimi)
- [4. Funksioni objektiv](#4-funksioni-objektiv)
  - [Kufiri i sipërm i javëve](#kufiri-i-sipërm-i-javëve)
  - [Shembull 1. Rast i mundur](#shembull-1-rast-i-mundur)
  - [Shembull 2. Rast i pamundur](#shembull-2-rast-i-pamundur)
- [5. Landscape (hapësira e kërkimit)](#5-landscape-hapësira-e-kërkimit)
- [6. DFS me backtracking](#6-dfs-me-backtracking)
- [7. Rezultatet](#7-rezultatet)
- [8. Ekzekutimi](#8-ekzekutimi)

---

## 1. Social Golfers Problem

**Përshkrimi**
32 lojtarë golfi luajnë golf një herë në javë dhe gjithmonë në grupe me nga 4. Për sa javë mund të luajnë në mënyrë që dy lojtarë të mos luajnë së bashku më shumë se një herë në të njëjtin grup?

A është e mundur të planifikohen `n = g × p` lojtarë golfi në `g` grupe me `p` lojtarë për `w` javë, në mënyrë që dy lojtarë të mos luajnë në të njëjtin grup më shumë se një herë?

**Shembull**

|        | Group 1 | Group 2   | Group 3   | Group 4    | Group 5    | Group 6     | Group 7     | Group 8     |
|--------|---------|-----------|-----------|------------|------------|-------------|-------------|-------------|
| Week 1 | 0,1,2,3 | 4,5,22,23 | 6,7,20,21 | 8,25,26,27 | 9,10,11,24 | 12,13,15,30 | 14,28,29,31 | 16,17,18,19 |

**Kërkesat e detyrës:**

1. Modeloni problemin.
2. Tregoni reprezentimin e problemit (variablat, domeni etj.).
3. Formuloni funksionin objektiv.
4. Kalkuloni landscape-in.
5. Implementoni Depth First Search (DFS) me backtracking.

---

## 2. Modelimi

Problemi modelohet si problem me kufizime (Constraint Satisfaction Problem). Çdo javë është një ndarje e `n = 32` lojtarëve në `g = 8` grupe me nga `p = 4` lojtarë. Kërkojmë numrin maksimal të javëve `w` për të cilin ekziston një orar që i plotëson kufizimet.

Le të jetë:

- `w`: numri i javëve
- `g`: numri i grupeve në javë
- `p`: numri i lojtarëve në grup
- `n = g · p`: numri total i lojtarëve

## 3. Reprezentimi

| Elementi | Përshkrimi |
|---|---|
| Variablat | `x[w][g][s]`: lojtari që zë vendin `s` në grupin `g` të javës `w` |
| Numri i variablave | `w · g · p = 32w` |
| Domeni | `{0, 1, ..., 31}` |

**Kufizimet:**

1. Brenda një jave çdo lojtar del saktësisht një herë.
2. Çdo grup ka saktësisht 4 lojtarë.
3. Dy lojtarë takohen në të njëjtin grup me se shumti një herë gjatë gjithë javëve.


## 4. Funksioni objektiv

Qëllimi kryesor:

```
maksimizo w   ashtu që ekziston orar pa konflikte
```

Për një `w` të fiksuar, cilësia e një orari matet me numrin e takimeve të përsëritura:

```
f = Σ max(0, takime(i, j) − 1)   për të gjitha çiftet (i, j), i < j
```

Orari është zgjidhje kur `f = 0`.

## 5. Landscape (hapësira e kërkimit)

Numri i mënyrave për të ndarë `n` lojtarë në grupe me madhësi `p`, kur grupet konsiderohen të renditura:

```
C(32,4) · C(28,4) · C(24,4) · ... · C(4,4)
= 35960 · 20475 · 10626 · 4845 · 1820 · 495 · 70 · 1
= 32! / (4!)^8 ≈ 2.4 × 10^24
```

Renditja e grupeve brenda javës nuk ka rëndësi, prandaj pjesëtojmë me `8!`:

```
32! / ((4!)^8 · 8!) ≈ 5.9 × 10^19   ndarje të ndryshme për një javë
```

Për `w` javë, me javën e parë të fiksuar:

```
|S| ≈ (5.9 × 10^19)^(w − 1)
```

| w | Madhësia e hapësirës |
|---|---|
| 2 | ≈ 5.9 × 10^19 |
| 5 | ≈ 1.2 × 10^79 |
| 7 | ≈ 4.2 × 10^118 |
| 10 | ≈ 8.7 × 10^177 |

Me reprezentimin e papërpunuar (pa thyer simetrinë), çdo javë ka `32! ≈ 2.6 × 10^35` mundësi, pra `(2.6 × 10^35)^w`.


## 6. DFS me backtracking

Implementimi është në `social_golfers.py`, kurse validimi dhe funksioni objektiv në `solution_validator.py`.

Algoritmi:

1. Mbush variablat me radhë: java, pastaj grupi, pastaj vendi në grup.
2. Për vendin e radhës provo kandidatët:
   - lojtari nuk duhet të jetë përdorur këtë javë;
   - lojtari nuk duhet të jetë takuar më parë me asnjë nga lojtarët e grupit aktual;
   - kandidati duhet t'i respektojë rregullat e thyerjes së simetrisë.
3. Nëse kandidati është i vlefshëm, vendose, shëno takimet dhe vazhdo më thellë.
4. Nëse asnjë kandidat nuk funksionon, kthehu mbrapa (backtrack): hiq lojtarin e fundit dhe takimet e tij.
5. Kur janë mbushur të gjitha javët, zgjidhja është gjetur.

Programi provon `w = 1, 2, 3, ...` me radhë dhe ndalon te `w`-ja e parë për të cilën nuk gjen zgjidhje brenda limitit të kohës. Çdo orar i gjetur kontrollohet me validatorin (`f = 0`).

**Dy mënyra kërkimi:**

- **DFS sistematik** (parazgjedhja): kandidatët provohen në rritje. Kërkimi është i plotë: nëse e shteron pemën, kjo provon që `w` është e pamundur.
- **DFS me rinisje të rastësishme** (`--random`): kandidatët renditen rastësisht dhe kërkimi rinis sa herë kalon një numër nyjesh (`--restart-nodes`). Kjo e shmang ngecjen në një degë të keqe në fillim të pemës dhe zakonisht arrin më shumë javë brenda të njëjtës kohë. Mbetet DFS me backtracking, por me limitin e kohës nuk mund të provojë që një `w` është e pamundur.

## 7. Rezultatet

Për çdo `w` programi shtyp nëse u gjet orar, vlerën e `f`, numrin e nyjeve të vizituara, kohën dhe, në mënyrën `--random`, numrin e rinisjeve. Në fund shtyp orarin me më shumë javë që gjeti.

Ekzekutimi me 8 × 4 lojtarë dhe limit prej 60 sekondash për çdo `w`:

| w | DFS sistematik | DFS me rinisje (`--seed 1`) |
|---|---|---|
| 1 | 0.00s, 42 nyje | 0.00s, 42 nyje |
| 2 | 0.00s, 83 nyje | 0.00s, 98 nyje |
| 3 | 0.00s, 124 nyje | 0.00s, 154 nyje |
| 4 | 0.00s, 165 nyje | 0.00s, 490 nyje |
| 5 | 0.00s, 206 nyje | 0.00s, 1 317 nyje |
| 6 | nuk u gjet brenda 60s | 0.05s, 15 338 nyje |
| 7 | | 0.15s, 49 733 nyje |
| 8 | | nuk u gjet brenda 60s (18.5 milion nyje, 370 rinisje) |

Të gjitha oraret e gjetura u kontrolluan me validatorin: `f = 0`.

Për javët ku kërkimi ngeci, ekzekutimi u përsërit me limit 10 herë më të madh, 600 sekonda (`--from` e nis kërkimin direkt nga ajo javë):

| Mënyra | w | Rezultati me 600s |
|---|---|---|
| DFS sistematik | 6 | nuk u gjet |
| DFS me rinisje (`--seed 1`) | 8 | nuk u gjet (168 milion nyje, 3 363 rinisje) |

Orari me 7 javë i gjetur nga DFS me rinisje:

```
Java  1: 0,1,2,3 | 4,5,6,7 | 8,9,10,11 | 12,13,14,15 | 16,17,18,19 | 20,21,22,23 | 24,25,26,27 | 28,29,30,31
Java  2: 0,18,23,30 | 1,14,22,31 | 2,20,25,28 | 3,21,27,29 | 4,9,13,16 | 5,11,19,26 | 6,10,15,17 | 7,8,12,24
Java  3: 0,15,20,29 | 1,19,27,30 | 2,14,23,24 | 3,10,25,31 | 4,12,22,28 | 5,9,17,21 | 6,8,16,26 | 7,11,13,18
Java  4: 0,14,16,25 | 1,8,21,28 | 2,17,27,31 | 3,19,20,24 | 4,11,15,23 | 5,10,13,29 | 6,9,12,18 | 7,22,26,30
Java  5: 0,4,10,27 | 1,13,17,25 | 2,7,9,29 | 3,18,26,28 | 5,8,15,22 | 6,14,20,30 | 11,16,21,24 | 12,19,23,31
Java  6: 0,6,24,31 | 1,11,12,20 | 2,10,18,22 | 3,5,16,30 | 4,17,26,29 | 7,15,21,25 | 8,13,23,27 | 9,14,19,28
Java  7: 0,13,19,22 | 1,9,15,24 | 2,4,8,30 | 3,11,14,17 | 5,18,20,31 | 6,23,25,29 | 7,16,27,28 | 10,12,21,26
```

**Interpretimi:**

- DFS sistematik i gjen 5 javët pa asnjë backtracking (rreth 41 nyje për javë). Renditja në rritje ndërton një orar shumë të rregullt, që i "bllokon" lojtarët: në javën e 6-të DFS-ja ngec në një degë të keqe afër rrënjës dhe nuk del prej saj brenda 60 sekondave.
- DFS me rinisje arrin 7 javë për 0.15 sekonda, pa asnjë rinisje. Renditja e rastësishme nuk e ndërton atë strukturë bllokuese, dhe rinisjet e shmangin ngecjen në një degë të keqe.
- Më shumë kohë nuk ndihmoi. DFS sistematik nuk e gjeti javën e 6-të as për 10 minuta, sepse mbetet në të njëjtën degë të keqe. DFS me rinisje nuk e gjeti javën e 8-të as me 168 milion nyje. Kjo përputhet me landscape-in: hapësira rritet me rreth `10^19` herë për çdo javë, kurse kufiri teorik prej 10 javësh kërkon metoda më të avancuara (thyerje më e fortë e simetrisë, heuristika ose kërkim lokal).

Rezultati varet nga limiti i kohës, kurse në mënyrën `--random` edhe nga `--seed`.

## 8. Ekzekutimi

Me Python (3.8 ose më i ri, pa librari shtesë):

```bash
python social_golfers.py
python social_golfers.py --random --time 60 --seed 1
python social_golfers.py -g 8 -p 4 -t 120
```
