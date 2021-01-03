import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = corpus[page]
    if not pages:
        return {x:1 / len(corpus) for x in corpus.keys()}

    model = {x:((1 - damping_factor) / len(corpus)) for x in corpus.keys()}
    for p in pages:
        model[p] += damping_factor / len(pages)
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    first = random.sample(corpus.keys(), 1)[0]
    model = transition_model(corpus, first, damping_factor)
    pagerank = model
    for _ in range(n - 1):
        next_page = random.choices(list(model.keys()), weights=list(model.values()))[0]
        model = transition_model(corpus,next_page,damping_factor)
        pagerank = {key: pagerank[key] + model.get(key,0) for key in pagerank}
    return {key:value/n for key,value in pagerank.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    random_p = (1 - damping_factor) / len(corpus)
    corpus = {x:(y if len(y) != 0 else set(corpus.keys())) for x,y in corpus.items()}
    pagerank = {x:(1/len(corpus)) for x in corpus}

    while True:
        conv = 0
        check = copy.deepcopy(pagerank)
        for page in corpus:
            count = 0
            for link in corpus:
                if page in corpus[link]:
                    count += check[link] / len(corpus[link])
            pagerank[page] = random_p + count * damping_factor
            if abs(check[page] - pagerank[page]) < 0.001:
                conv += 1
        if conv == len(corpus):
            break
    return check


if __name__ == "__main__":
    main()
