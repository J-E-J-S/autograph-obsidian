# AutoGraph-Obsidian: Automated Knowledge Graph Generation.   

## Introduction  
AutoGraph is a tool that enables rapid, automated knowledge graph generation. AutoGraph does this by mining scientific literature against a search query for keywords. From this data, an Obsidian vault is made where each mined keyword has its own markdown file containing: i) the name of the paper the keyword was scraped from and ii) links to other keywords from that paper. When two papers share a keyword, a link is established between those articles through that term. Over many papers, this allows a network of interactions between articles in a field to be visualized. The purpose of this tool is not only to establish graph-based summaries of topics but also to identify hidden links between divergent fields - largely inspired by the works of [Manfred Kochen](https://dblp.org/pid/31/4553.html).


## Prerequisites:  
* [Python](https://www.python.org/downloads/) >= 3.6  
* [Obsidian.md](https://obsidian.md/)

## Quickstart:
```
pip3 install autograph-obsidian
```

## Usage:  
```
Usage: autograph [OPTIONS] QUERY

  Arguments:

  QUERY The main search string.

Options:
  -l, --limit INTEGER  Number of papers to mine. Default = 500.
  -v, --version        Show version number and exit.
  --help               Show this message and exit.
```
e.g.
```
autograph 'Genetic Code Expansion' -l 100
```
## Case Study  
Generating the graph with autograph  

![](/assets/autograph.gif)

Viewing the graph with Obsidian.md


![](/assets/case_study.gif)

## Acknowledgements  
The mining of scientific literature is handled by the [pygetpapers](https://github.com/petermr/pygetpapers) package developed by [ContentMine](https://contentmine.github.io/).
