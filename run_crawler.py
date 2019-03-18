from args_parser import parse, Args
from parallel_crawler import ParallelCrawler


def main():
    args = parse("WebCrawler by Marcin Knap")
    crawler = ParallelCrawler(args[Args.HomePage.value], args[Args.ProjectName.value], args[Args.SaveFlag.value])
    crawler.crawl()


if __name__ == "__main__":
    main()
