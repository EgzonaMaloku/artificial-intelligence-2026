# Teknikat e Painformuara të Kërkimit (Uninformed Search Techniques)

## Përmbajtja

- [1. Sudoku Solver](#1-sudoku-solver)
- [2. Modelimi](#2-modelimi)
- [3. Reprezentimi](#3-reprezentimi)
- [4. Funksioni objektiv](#4-funksioni-objektiv)
- [5. Landscape (hapësira e kërkimit)](#5-landscape-hapësira-e-kërkimit)
- [6. BFS me backtracking](#6-bfs-me-backtracking)
- [7. Nivelet Easy, Medium, Hard](#7-nivelet-easy-medium-hard)
- [8. Rezultatet](#8-rezultatet)
- [9. Ekzekutimi](#9-ekzekutimi)

---

## 1. Sudoku Solver

**Përshkrimi**
Të shkruhet programi i cili e zgjidh një Sudoku. Programi duhet t'i parashohë tri nivele të Sudoku: Easy, Medium, Hard.

Sudoku ka 81 qeliza në një rrjetë 9 × 9, të ndara në 9 rreshta, 9 kolona dhe 9 blloqe 3 × 3. Disa qeliza janë të dhëna. Qelizat bosh duhet të plotësohen me numrat 1 deri 9, ashtu që në çdo rresht, kolonë dhe bllok çdo numër të paraqitet vetëm një herë.

**Kërkesat e detyrës:**

1. Modeloni problemin.
2. Tregoni reprezentimin e problemit (variablat, domeni etj.).
3. Formuloni funksionin objektiv.
4. Kalkuloni landscape-in.
5. Implementoni Breadth First Search (BFS) me backtracking.

---

## 2. Modelimi

Sudoku modelohet si problem me kufizime (Constraint Satisfaction Problem):

- çdo qelizë bosh është një variabël;
- çdo variabël merr një vlerë nga 1 deri 9;
- kufizimet kërkojnë që vlerat në çdo rresht, kolonë dhe bllok të jenë të ndryshme (kufizim *all-different*).

Për kërkimin, problemi shndërrohet në problem kërkimi në hapësirën e gjendjeve: nisemi nga rrjeta e dhënë dhe në çdo hap plotësojmë edhe një qelizë, derisa rrjeta të jetë e plotë dhe e vlefshme.

## 3. Reprezentimi

| Elementi | Përshkrimi |
|---|---|
| Variablat | `X[r][c]`: vlera në rreshtin `r` dhe kolonën `c`, për çdo qelizë bosh (`k` variabla, `k` = numri i qelizave bosh) |
| Domeni | `{1, 2, ..., 9}`; për qelizat e dhëna domeni është vlera e dhënë |
| Kufizimet | 27 njësi (9 rreshta, 9 kolona, 9 blloqe) ku të gjitha vlerat janë të ndryshme; çdo qelizë ka 20 "fqinjë" me të cilët nuk mund të ketë vlerë të njëjtë |
| Gjendja fillestare | sudoku i dhënë |
| Gjendja finale | të gjitha 81 qelizat janë plotësuar dhe asnjë kufizim nuk shkelet |
| Kostoja e hapit | 1 (çdo hap plotëson një qelizë) |

## 4. Funksioni objektiv

Për një rrjetë të plotë, numri i shkeljeve të kufizimeve:

```
f = Σ (mbi 27 njësitë) Σ (v = 1..9) max(0, numri(v në njësi) − 1)
```

Rrjeta është zgjidhje kur është e plotë dhe `f = 0`. Qëllimi është:

```
gjej rrjetën e plotë me  f = 0  që i ruan numrat e dhënë
```

Në kërkim, `f` mbahet gjithmonë 0, sepse një vlerë vendoset vetëm nëse nuk krijon përsëritje. Prandaj testi i qëllimit reduktohet në "a ka mbetur ndonjë qelizë bosh". Validatori (`sudoku_validator.py`) e llogarit `f` për çdo zgjidhje të gjetur si kontroll i pavarur.

## 5. Landscape (hapësira e kërkimit)

Për një sudoku me `k` qeliza bosh, pa asnjë kufizim, çdo qelizë ka 9 mundësi:

```
|S| = 9^k
```
Programi i llogarit të dyja vlerat për çdo sudoku:

| Niveli | Numra të dhënë | Qeliza bosh `k` | `9^k` | Me kandidatët fillestarë |
|---|---|---|---|---|
| Easy | 30 | 51 | 9^51 
| Medium | 26 | 55 | 9^55 
| Hard | 21 | 60 | 9^60 

## 6. BFS me backtracking

Implementimi është në `sudoku_solver.py`, kurse validimi dhe funksioni objektiv në `sudoku_validator.py`.

**BFS** i zgjeron gjendjet nivel pas niveli me një radhë (FIFO):

1. Fut gjendjen fillestare në radhë.
2. Merr gjendjen e parë nga radha.
3. Zgjidh një qelizë bosh dhe llogarit kandidatët e saj.
4. Për çdo kandidat krijo një gjendje fëmijë dhe fute në fund të radhës. Nëse fëmija nuk ka më qeliza bosh, ai është zgjidhje.
5. Përsërit nga hapi 2 derisa të gjendet zgjidhja ose radha të zbrazet.

Në nivelin `d` të pemës janë të gjitha gjendjet me `d` qeliza të plotësuara, kështu që BFS i provon paralelisht të gjitha rrugët e mundshme.

**Backtracking-u** është krasitja e degëve të pavlefshme:

- Një fëmijë krijohet vetëm nëse vlera nuk përsëritet në rresht, kolonë ose bllok. Gjendjet e pavlefshme nuk hyjnë kurrë në radhë.
- Nëse qeliza e zgjedhur nuk ka asnjë kandidat, gjendja është rrugë pa dalje dhe hidhet. Kërkimi "kthehet mbrapa" duke vazhduar me gjendjet e tjera në radhë.

Pa këtë krasitje, BFS do të duhej të mbante në radhë deri në `9^d` gjendje në nivelin `d`, gjë që është e pamundur për memorien.

**Renditja e qelizave** (`--order`):

- `fixed`: qeliza e parë bosh, rresht pas rreshti. Plotësisht e painformuar.
- `mrv` (parazgjedhja): qeliza bosh me më pak kandidatë (*Minimum Remaining Values*). Qelizat me një kandidat të vetëm plotësohen pa degëzim, dhe një qelizë me zero kandidatë zbulohet menjëherë, kështu që rrugët pa dalje priten shumë më herët.

**Unikaliteti:** me `--all` BFS vazhdon derisa radha të zbrazet dhe numëron të gjitha zgjidhjet. Kështu verifikohet që secili nga tri sudoku-t ka saktësisht një zgjidhje.

## 8. Rezultatet

Ekzekutimi me `--all`, që e shteron gjithë pemën dhe numëron zgjidhjet. Meqë të gjitha zgjidhjet janë në thellësinë e fundit, BFS e gjen zgjidhjen vetëm pasi i ka zgjeruar pothuajse të gjitha nivelet, prandaj numrat pa `--all` janë gati të njëjtë.

**Renditja `fixed` (rresht pas rreshti, e painformuar):**

| Niveli | Koha | Nyje të zgjeruara | Rrugë pa dalje | Frontier maksimal | Zgjidhje |
|---|---|---|---|---|---|
| Easy | 0.06s | 4 631 | 1 371 | 738 | 1 |
| Medium | 0.43s | 33 498 | 10 239 | 5 821 | 1 |
| Hard | 25.10s | 2 068 780 | 705 261 | 356 812 | 1 |

**Renditja `mrv` (qeliza me më pak kandidatë):**

| Niveli | Koha | Nyje të zgjeruara | Rrugë pa dalje | Frontier maksimal | Zgjidhje |
|---|---|---|---|---|---|
| Easy | 0.00s | 51 | 0 | 1 | 1 |
| Medium | 0.00s | 156 | 4 | 4 | 1 |
| Hard | 0.52s | 24 880 | 1 799 | 1 003 | 1 |

Të gjitha zgjidhjet u kontrolluan me validatorin: `f = 0` dhe numrat e dhënë të paprekur.

Zgjidhja e sudoku-t Hard:

```
8 1 2 | 7 5 3 | 6 4 9
9 4 3 | 6 8 2 | 1 7 5
6 7 5 | 4 9 1 | 2 8 3
------+-------+------
1 5 4 | 2 3 7 | 8 9 6
3 6 9 | 8 4 5 | 7 2 1
2 8 7 | 1 6 9 | 5 3 4
------+-------+------
5 2 1 | 9 7 4 | 3 6 8
4 3 8 | 5 2 6 | 9 1 7
7 9 6 | 3 1 8 | 4 5 2
```

**Interpretimi:**

- Nivelet dallohen qartë te renditja `fixed`: nga Easy te Hard numri i nyjeve rritet rreth 450 herë, kurse koha nga 0.06s në 25s.
- Problemi kryesor i BFS-së është memoria. Te Hard radha arriti 356 812 gjendje njëherësh, sepse BFS i mban të gjitha rrugët e hapura të një niveli para se të kalojë në nivelin tjetër.
- Backtracking-u e bën BFS-në të zbatueshme. Nga `10^37` kombinime të kandidatëve fillestarë, BFS zgjeroi vetëm rreth `2 × 10^6` gjendje, sepse çdo degë me përsëritje pritet menjëherë.
- MRV e zvogëlon punën rreth 80 deri në 100 herë. Te Easy nuk ka asnjë degëzim: çdo hap ka një qelizë me një kandidat të vetëm, kështu që BFS ecën drejt e te zgjidhja në 51 hapa.

## 9. Ekzekutimi

Me Python (3.8 ose më i ri, pa librari shtesë):

```bash
python sudoku_solver.py
python sudoku_solver.py --level hard --order fixed
python sudoku_solver.py --all
python sudoku_solver.py --puzzle "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
```

Me Docker:

```bash
docker build -t sudoku_solver .
docker run --rm sudoku_solver --level all --all
```
