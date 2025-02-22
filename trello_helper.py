import argparse
import requests
import json
import webbrowser

# Trello API credentials
BASE_URL = "https://api.trello.com/1"

def get_token(api_key):#this is the function to get the token
    """Retrieve authentication token from Trello"""
    auth_url = f"{BASE_URL}/authorize?key={api_key}&name=TrelloCLI&expiration=never&response_type=token&scope=read,write"
    print("Please authorize the app by visiting this URL:")
    print(auth_url)
    webbrowser.open(auth_url)

def get_boards(api_key, token):#this is the function to get the boards
    """Retrieve all boards for the user"""
    url = f"{BASE_URL}/members/me/boards?key={api_key}&token={token}"
    response = requests.get(url)
    if response.status_code == 200:#this is the status code for successful request
        return response.json()
    else:
        print("Error fetching boards:", response.text)
        return None

def get_lists(api_key, token, board_id):#this is the function to get the lists
    """Retrieve all lists from a given board"""
    url = f"{BASE_URL}/boards/{board_id}/lists?key={api_key}&token={token}"
    response = requests.get(url)
    if response.status_code == 200:#this is the status code for successful request
        return response.json()
    else:
        print("Error fetching lists:", response.text)
        return None

def main():
    parser = argparse.ArgumentParser(description='Find Trello Board ID, List ID, and Token')
    parser.add_argument('--api-key', required=True, help='Your Trello API key')
    parser.add_argument('--get-token', action='store_true', help='Fetch Trello API token')
    parser.add_argument('--board', action='store_true', help='Retrieve Board ID')
    parser.add_argument('--list', type=str, help='Retrieve List ID for a given Board ID')
    parser.add_argument('--token', type=str, help='Your Trello API token (required for board and list retrieval)')
    args = parser.parse_args()
    
    if args.get_token:
        get_token(args.api_key)#I have written this function because user has to authorize the app by visiting the url
        return
    
    if not args.token:
        print("Error: --token argument is required unless fetching a new token.")
        return
    
    if args.board:
        boards = get_boards(args.api_key, args.token)
        if boards:
            print("Available Boards:")
            for board in boards:
                print(f"ID: {board['id']} - Name: {board['name']}")
    
    if args.list:
        lists = get_lists(args.api_key, args.token, args.list)
        if lists:
            print("Available Lists in Board:")
            for lst in lists:
                print(f"ID: {lst['id']} - Name: {lst['name']}")

if __name__ == "__main__":
    main()