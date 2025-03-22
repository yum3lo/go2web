import argparse
import socket
import ssl

def fetch_url(url):
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
      # Forcing TLSv1.2 or higher for the specific SSL/TLS version DuckDuckGo API requires
      context.minimum_version = ssl.TLSVersion.TLSv1_2
      context.maximum_version = ssl.TLSVersion.TLSv1_3
      s = context.wrap_socket(s, server_hostname=host)
      port = 443
    else:
      port = 80
            
    s.connect((host, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    s.sendall(request.encode())

    response = b""
    while True:
      data = s.recv(4096)
      if not data:
        break
      response += data

    s.close()

    return response.decode('utf-8', errors='ignore')
  except Exception as e:
    return f"Error: {str(e)}"

def search_web(query):
  search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
  response = fetch_url(search_url)
  return response

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