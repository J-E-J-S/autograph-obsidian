# AutoGraph-Obsidian: Automated Knowledge Graph Construction.   

## Prerequisites:  
* [Python](https://www.python.org/downloads/) >= 3.6  
* [Node.js](https://nodejs.org/en/) >= 14.0  
* [Obsidian.md](https://obsidian.md/)

## Quickstart:
```
pip install autograph-obsidian
```

## Usage:  
```
Usage: autograph [OPTIONS] QUERY

  Arguments:

  QUERY The main search string.

Options:
  -l, --limit INTEGER  Number of papers to mine. Default = 500
  -v, --version        Show version number and exit.
  --help               Show this message and exit.
```
e.g.
```
autograph 'Genetic Code Expansion' -l 100
```
## Case Study  
Generating the graph with autograph.  

![](/assets/autograph.gif)

Viewing the graph with Obsidian.md


![](/assets/case_study.gif)
