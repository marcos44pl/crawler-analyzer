from args_parser import Args, parse
from graph import Graph
from page_rank import PageRank

if __name__ == "__main__":
    args = parse("Graph Analyzer by Marcin Knap")
    path = args[Args.ProjectName.value]
    g = Graph(path)
    g.analyze()
    page_rank = PageRank(g.dig, path)
    #page_rank.check_concur()
    page_rank.calc_page_rank(d=0.85)
    page_rank.print()
    page_rank.save()
