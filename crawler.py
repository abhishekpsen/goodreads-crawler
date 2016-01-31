import requests
from bs4 import BeautifulSoup
from collections import deque
import networkx as nx
import NetworkxD3

def goodreads_spider_bfs(max_pages_crawled = 1200):
	seed_url = 'https://www.goodreads.com/book/show/164323.The_Google_Story'
	q = deque()
	q.append(seed_url)
	pages_crawled = {seed_url}
	f = open('Small_BookGraph_BFS.txt','w')
	print 'Beginning the crawl with %s'%(get_book_name(seed_url))
	f.write('Beginning the crawl with %s\n'%(get_book_name(seed_url)))
	num_pages_crawled = 1
	G = nx.Graph()	#Graph for visualization

	while q and num_pages_crawled <= max_pages_crawled:
		u = q.popleft()
		u_book_name = get_book_name(u)
		similar_books = get_similar_books(u)
		if not similar_books:
			continue
		for v in similar_books[:3]:
			if v not in pages_crawled:
				pages_crawled.add(v)
				q.append(v)
				v_book_name = get_book_name(v)
				print '%s -> %s'%(u_book_name,v_book_name)
				f.write('%s -> %s\n'%(u_book_name,v_book_name))
				G.add_edge(u_book_name,v_book_name)
				num_pages_crawled += 1
	f.close()
	NetworkxD3.simpleNetworkx(G)


def goodreads_spider_dfs(max_pages_crawled = 15):
	seed_url = 'https://www.goodreads.com/book/show/13912.A_Beautiful_Mind'
	seed_url = 'https://www.goodreads.com/book/show/11084145-steve-jobs'
	s = []
	s.append(seed_url)
	pages_crawled = {seed_url}
	print 'Beginning the crawl with %s'%(get_book_name(seed_url))
	num_pages_crawled = 1
	G = nx.Graph()	#Graph for visualization
	while s and num_pages_crawled <= max_pages_crawled:
		u = s.pop()
		u_book_name = get_book_name(u)
		for v in get_similar_books(u)[:3]:
			if v not in pages_crawled:
				pages_crawled.add(v)
				s.append(v)
				#num_pages_crawled += 1
				v_book_name = get_book_name(v)
				print '%s -> %s'%(u_book_name,v_book_name)
				G.add_edge(u_book_name,v_book_name)
				num_pages_crawled += 1
	NetworkxD3.simpleNetworkx(G)

def get_similar_books(url):
	try:
		page_source = requests.get(url).text
	except:
		return None
	soup = BeautifulSoup(page_source)
	bookCarousel = soup.find('div', class_='bookCarousel').ul
	similar_books = []
	for li in bookCarousel.findAll('li'):
		similar_books.append(li.a.get('href'))
	return similar_books


def get_book_name(url):
	try:
		page_source = requests.get(url).text
		soup = BeautifulSoup(page_source)
		book_name = str(soup.h1.text.strip().split("\n",1)[0])
	except:
		book_name = 'Book name is not ascii encoded'
	return book_name


if __name__ == '__main__':
	print 'Crawler starts'
	goodreads_spider_bfs(20)
