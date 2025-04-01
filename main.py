import argparse
import socket
import ssl
import json
from urllib.parse import urljoin
import os

cache_file = 'cache.json'

def load_cache():
  if os.path.exists(cache_file):
    try:
      with open(cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)
    except json.JSONDecodeError:
      print("Cache file is corrupted. Starting with an empty cache.")
      return {}
  return {}

def save_cache(cache_data):
  with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(cache_data, f, indent=2)

cache = load_cache()

def fetch_url(url):
  cache_url = url
  if cache_url in cache:
    print(f"Cache hit for {cache_url}")
    return cache[cache_url]
  
  try:
    if not url.startswith(('http://', 'https://')):
      url = 'http://' + url

    protocol = 'http'
    if url.startswith('https://'):
      protocol = 'https'

    host = url.split('/')[2]
    path = '/' + '/'.join(url.split('/')[3:])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Wrapping the socket with SSL if HTTPS
    if protocol == 'https':
      context = ssl.create_default_context()
      s = context.wrap_socket(s, server_hostname=host)
      port = 443
    else:
      port = 80
            
    s.connect((host, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: application/json, text/html\r\nConnection: close\r\n\r\n"
    s.sendall(request.encode())

    response = b""
    while True:
      data = s.recv(4096)
      if not data:
        break
      response += data

    s.close()

    response = response.decode('utf-8', errors='ignore')
    headers, body = response.split('\r\n\r\n', 1)
    
    # Redirect handling
    if 'HTTP/1.1 301' in headers or 'HTTP/1.1 302' in headers:
      location_start = headers.find('Location:') + len('Location:')
      location_end = headers.find('\r\n', location_start)
      redirect_url = headers[location_start:location_end].strip()
    
      if not redirect_url.startswith(('http://', 'https://')):
        base_url = f"{protocol}://{host}"
        redirect_url = urljoin(base_url, redirect_url)

      return fetch_url(redirect_url)

    if 'Transfer-Encoding: chunked' in headers:
      body = handle_chunked_body(body)

    cache[cache_url] = body
    save_cache(cache)
    print(f"Cache updated for {url}")

    return body
  except Exception as e:
    return f"Error: {str(e)}"

def handle_chunked_body(body):
  cleaned_body = ""
  while body:
    chunk_size_end = body.find('\r\n')
    if chunk_size_end == -1:
      break

    # Getting the chunk size (hexadecimal)
    chunk_size_hex = body[:chunk_size_end]
    chunk_size = int(chunk_size_hex, 16)

    if chunk_size == 0:
      break

    chunk_start = chunk_size_end + 2
    chunk_end = chunk_start + chunk_size
    chunk_data = body[chunk_start:chunk_end]
    cleaned_body += chunk_data
    body = body[chunk_end + 2:]

  return cleaned_body

def search_web(query):
  cache_query = query
  if cache_query in cache:
    print(f"Cache hit for {cache_query}")
    return cache[cache_query]
  
  search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
  response = fetch_url(search_url)

  try:
    data = json.loads(response)
    related_topics = data.get("RelatedTopics", [])
    top_results = []
    for topic in related_topics[:10]:
      if "Text" in topic and "FirstURL" in topic:
        top_results.append(f"{topic['Text']} - {topic['FirstURL']}")

    if not top_results:
      return "No results found."

    return "\n".join(top_results)
  except json.JSONDecodeError:
    return "Failed to parse search results."

def main():
  parser = argparse.ArgumentParser(description="CLI tool for PWeb lab 5")
  parser.add_argument('-u', '--url', help='Make an HTTP request to the specified URL and print the response')
  parser.add_argument('-s', '--search', help='Make an HTTP request to search the term using Google and print top 10 results')
  
  args = parser.parse_args()
  
  if args.url:
    response = fetch_url(args.url)
    print(response)
  elif args.search:
    response = search_web(args.search)
    print(response)
  else:
    parser.print_help()

if __name__ == "__main__":
  main()