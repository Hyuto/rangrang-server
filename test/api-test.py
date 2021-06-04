"""
Testing script to post file to endpoint django.

Usage:
    python api-test.py -e URL -f PATH

Example:
    python api-test.py http://35.222.141.247/od-api/video/ -f test/test.mp4

Raises:
    KeyError: Args Error.

RangRang 2021 - server
"""
import argparse, requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Testing untuk POST file ke endpoint dari backend")
    parser.add_argument("-e",
                        "--endpoint",
                        help="URL ke endpoint dari backedn",
                        type=str)
    parser.add_argument("-f",
                        "--files",
                        help="Path ke file yang akan dipost.",
                        type=str)
    
    args = parser.parse_args()
    if args.endpoint and args.files:
        with open(args.files, 'rb') as finput:
            response = requests.post(args.endpoint, files={'file': finput})

        print(f'{response.status_code} - {response.elapsed.total_seconds()}s')
        print(response.json())
    else:
        raise KeyError('Args Error!')