import argparse
import requests
import json
import sys
import webbrowser
from trello_helper import print_boards_ids, print_lists_ids, print_labels_ids

#Alper Kutay OZBEK
#20250222

# Trello API Base URL
BASE_URL = "https://api.trello.com/1"

class TrelloCardCLI:
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token
        self.auth_params = {
            'key': self.api_key,
            'token': self.token
        }
    
    def get_token(self):
        """Generate a Trello authentication token."""
        auth_url = f"https://trello.com/1/authorize?key={self.api_key}&name=TrelloCLI&expiration=never&response_type=token&scope=read,write"
        print("Authorize the app by visiting:")
        print(auth_url)
        webbrowser.open(auth_url)
    
    def get_boards(self):
        """Retrieve all boards for the user."""
        url = f"{BASE_URL}/members/me/boards"
        response = requests.get(url, params=self.auth_params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching boards:", response.text)
            return None
    
    def get_lists(self, board_id):
        """Retrieve all lists from a given board."""
        url = f"{BASE_URL}/boards/{board_id}/lists"
        response = requests.get(url, params=self.auth_params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching lists:", response.text)
            return None
    
    def get_labels(self, api_key, token, board_id):
        """Retrieve all labels from a given board"""
        url = f"{BASE_URL}/boards/{board_id}/labels?key={api_key}&token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching labels:", response.text)
        return None
    
    def resolve_label_ids(self, board_id, label_identifiers):
        """Convert label names or IDs to Trello label IDs."""
        all_labels = self.get_labels(self.api_key, self.token, board_id)
        if not all_labels:
            return []
        
        label_ids = []
        for identifier in label_identifiers:
            # First try to match by ID
            id_match = next((label['id'] for label in all_labels if label['id'] == identifier), None)
            if id_match:
                label_ids.append(id_match)
                continue
                
            # If no ID match, try to match by name
            name_match = next((label['id'] for label in all_labels if label['name'].lower() == identifier.lower()), None)
            if name_match:
                label_ids.append(name_match)
                continue
        
        if not label_ids:
            print("Warning: No matching label IDs found for given names/IDs.")
            print_labels_ids(self.api_key, self.token, board_id)
            print("\nIf you want to create a card, you need to provide a label ID. use --labels <label_id>")
            sys.exit(1)
        return label_ids
    
    def create_card(self, board_id, list_id, name, description=None, labels=None, comment=None):
        
        """Create a card on Trello with labels and a comment."""

        label_ids = self.resolve_label_ids(board_id, labels) if labels else []
        
        url = f"{BASE_URL}/cards"
        data = {
            **self.auth_params,
            'idList': list_id,
            'name': name,
            'idLabels': ','.join(label_ids) if label_ids else ''
        }
        
        if description:
            data['desc'] = description
        
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Error creating card: {response.text}")
            return None
        
        card = response.json()
        if comment:
            self.add_comment(card['id'], comment)
        
        return card
    
    def add_comment(self, card_id, comment):
        """Add a comment to a Trello card."""
        url = f"{BASE_URL}/cards/{card_id}/actions/comments"
        data = {
            **self.auth_params,
            'text': comment
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Error adding comment: {response.text}")

def main():
    #I used chatgpt to help me with the usage of argparse
    parser = argparse.ArgumentParser(description='Trello CLI Tool to add a card with labels and comments')
    parser.add_argument('--api-key', required=True, help='Your Trello API key')
    parser.add_argument('--token', required=True, help='Your Trello API token')
    parser.add_argument('--board-id', required=True, help='Trello Board ID')
    parser.add_argument('--list-id', required=True, help='List ID where the card will be created')
    parser.add_argument('--name', required=True, help='Card name')
    parser.add_argument('--description', help='Card description')
    parser.add_argument('--labels', nargs='+', help='Label names or IDs to add to the card')
    parser.add_argument('--comment', help='Comment to add to the card')
    
    # First parse just the API key, token, and board-id
    partial_parser = argparse.ArgumentParser(add_help=False)
    partial_parser.add_argument('--api-key')
    partial_parser.add_argument('--token')
    partial_parser.add_argument('--board-id')
    partial_parser.add_argument('--list-id')
    partial_args, _ = partial_parser.parse_known_args()

    # If we have API key and token but no board ID, show available boards
    if partial_args.api_key and partial_args.token and not partial_args.board_id:
        print("\nTo find your board ID, here are your available boards:")
        print_boards_ids(partial_args.api_key, partial_args.token)
        print("\nIf you want to create a card, you need to provide a board ID. use --board-id <board_id>")
        sys.exit(1)

    if partial_args.api_key and partial_args.token and partial_args.board_id and not partial_args.list_id:
        print("\nTo find your list ID, here are your available lists:")
        print_lists_ids(partial_args.api_key, partial_args.token, partial_args.board_id)
        print("\nIf you want to create a card, you need to provide a list ID. use --list-id <list_id>")
        sys.exit(1)

    # Parse all arguments
    args = parser.parse_args()
    trello_cli = TrelloCardCLI(args.api_key, args.token)
    card = trello_cli.create_card(
        args.board_id, args.list_id, args.name, description=args.description,
        labels=args.labels, comment=args.comment
    )
    
    if card:
        print(f"\nCard created successfully! ID: {card['id']} - URL: {card['url']}")

if __name__ == "__main__":
    main()
