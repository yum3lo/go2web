import argparse
import socket

def fetch_url(url):
  try:
    if not url.startswith('http://'):
      url = 'http://' + url

    host = url.split('/')[2]
    path = '/' + '/'.join(url.split('/')[3:])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

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

def main():
  parser = argparse.ArgumentParser(description="CLI tool for PWeb lab 5")
  parser.add_argument('-u', '--url', help='Make an HTTP request to the specified URL and print the response')
  parser.add_argument('-s', '--search', help='Make an HTTP request to search the term using Google and print top 10 results')
  
  args = parser.parse_args()
  if args.url:
    response = fetch_url(args.url)
    print(response)
  elif args.search:
    print(f'Searching for {args.search} using Google')
  else:
    parser.print_help()

if __name__ == "__main__":
  main()