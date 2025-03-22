import argparse

def main():
  parser = argparse.ArgumentParser(description="CLI tool for PWeb lab 5")
  parser.add_argument('-u', '--url', help='Make an HTTP request to the specified URL and print the response')
  parser.add_argument('-s', '--search', help='Make an HTTP request to search the term using Google and print top 10 results')
  
  args = parser.parse_args()
  if args.url:
    print(f'Making an HTTP request to {args.url}')
  elif args.search:
    print(f'Searching for {args.search} using Google')
  else:
    parser.print_help()

if __name__ == "__main__":
  main()