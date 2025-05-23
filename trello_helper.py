import argparse
import requests
import json
import webbrowser

#this is the helper file for the trello_main.py file
#this file contains the functions to get the token, boards, lists and labels
#the functions are used in the trello_main.py file

#Alper Kutay OZBEK
#20250222

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
        if "invalid app token" in response.text:
            print("Invalid token. Please check your API key and token.")
            get_token(api_key)
        return None

def get_lists(api_key, token, board_id):#this is the function to get the lists
    """Retrieve all lists from a given board"""
    url = f"{BASE_URL}/boards/{board_id}/lists?key={api_key}&token={token}"
    response = requests.get(url)
    if response.status_code == 200: 
        return response.json()
    else:
        print("Error fetching lists:", response.text)
        if "invalid id" in response.text:
            print_boards_ids(api_key, token)
        return None

def get_labels(api_key, token, board_id):#this is the function to get the labels
    """Retrieve all labels from a given board"""
    url = f"{BASE_URL}/boards/{board_id}/labels?key={api_key}&token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching labels:", response.text)
        if "invalid id" in response.text:
            print_boards_ids(api_key, token)
        return None

def print_boards_ids(api_key, token):
    boards = get_boards(api_key, token)
    if boards:
        print("Available Boards:")
        for board in boards:
            print(f"ID: {board['id']} - Name: {board['name']}")

def print_lists_ids(api_key, token, board_id):
    lists = get_lists(api_key, token, board_id)
    if lists:
        print("Available Lists in Board:")
        for lst in lists:
            print(f"ID: {lst['id']} - Name: {lst['name']}")

def print_labels_ids(api_key, token, board_id):
    labels = get_labels(api_key, token, board_id)
    if labels:
        print("Available Labels in Board:")
        for label in labels:
            name = label['name'] or '[No name]'
            color = label['color'] or '[No color]'
            print(f"ID: {label['id']} - Name: {name} - Color: {color}")

def main():
    parser = argparse.ArgumentParser(description='Find Trello Board ID, List ID, Labels and Token')
    parser.add_argument('--api-key', required=True, help='Your Trello API key')
    parser.add_argument('--get-token', action='store_true', help='Fetch Trello API token')
    parser.add_argument('--get-board-ids', action='store_true', help='Retrieve Board ID')
    parser.add_argument('--get-list-ids', type=str, help='Retrieve List ID for a given Board ID')
    parser.add_argument('--get-label-ids', type=str, help='Retrieve Label IDs for a given Board ID')
    parser.add_argument('--token', type=str, help='Your Trello API token (required for board, list and label retrieval)')
    args = parser.parse_args()
    
    if args.get_token:
        get_token(args.api_key)#I have written this function because user has to authorize the app by visiting the url
        return
    
    if not args.token:
        print("Error: --token argument is required unless fetching a new token.")
        return

    if args.get_board_ids:
        print_boards_ids(args.api_key, args.token)

    if args.get_list_ids:
        print_lists_ids(args.api_key, args.token, args.get_list_ids)

    if args.get_label_ids:
        print_labels_ids(args.api_key, args.token, args.get_label_ids)

if __name__ == "__main__":
    main()