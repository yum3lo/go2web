# Lab 5 - Websockets

## Overview

This project implements a command-line tool called `go2web` that performs HTTP requests and searches using DuckDuckGo. The program follows the requirements below:

## Features Implemented

1. CLI commands:
    ```
    go2web -u <URL>         # makes an HTTP request to the specified URL and prints the response
    go2web -s <search-term> # searches the term using DuckDuckGo and prints top 10 results
    go2web -h               # shows help
    ```
2. Human-readable output
3. Special Conditions:
   - No built-in or third-party libraries for HTTP requests were used.
   - The program is implemented in Python and uses raw sockets for HTTP/HTTPS communication.
   - Handles `301` and `302` redirects.
   - Implements an in-memory cache to store responses.
   - Supports both JSON and HTML content types via the `Accept` header.

## Results

Below is a GIF demonstrating the program in action:
![ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/6eb30eb8-cda2-4b47-a2fd-8a336cbf527a)

## How to run
1. Clone the repository.
2. Run the program using:
   ```
   python main.py -u <URL>
   python main.py -s <search-term>
   ```
