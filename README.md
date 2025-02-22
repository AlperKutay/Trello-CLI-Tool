# Trello CLI Tool

## Overview
This **Trello CLI Tool** allows you to create Trello cards effortlessly from your terminal. With this tool, you can:
- Fetch your **Trello API token** for authentication.
- Retrieve **Board IDs**, **List IDs**, and **Label IDs** dynamically.
- Create Trello cards with **descriptions, labels, and comments**.

Built to simplify Trello workflows, this CLI ensures that you don’t have to navigate through the web interface to manage your tasks.

---

## Features
✅ Fetch **Board IDs, List IDs, and Label IDs** dynamically.\
✅ **Automatically resolve label names** to valid label IDs.\
✅ Create a **Trello card with a description, labels, and comments**.\
✅ Handle errors gracefully and provide helpful suggestions.


---

## Installation
### **Prerequisites:**
- Python 3.6+
- A **Trello API key** and **Token** (See below for how to get them).

### **Clone the Repository:**
```sh
 git clone https://github.com/AlperKutay/CanonicalAssignment.git
 cd CanonicalAssignment
```

### **Install Dependencies:**
```sh
pip install -r requirements.txt
```

---

## How to Get Your Trello API Key & Token
### **Get Trello API Key**
1. Visit [Trello API Key Page](https://trello.com/app-key).
2. Click on **Power-Up Admin Portal.**
3. Click on **Create a new app.**
4. Click on **Create.**
5. Generate a new key.
6. Copy your API Key.

### **Get Trello API Token**
1. Run this command:
   ```sh
   python trello_helper.py --api-key YOUR_API_KEY --get-token
   ```
2. This will open a **Trello authorization page**.
3. Approve the request and **copy the generated token**.

---

## How to Use the CLI Tool
### **1. Find Your Board ID**
```sh
python trello_helper.py --api-key YOUR_API_KEY --token YOUR_TRELLO_TOKEN --get-board-ids
```
Copy the **Board ID** you want to use.

### **2. Find Your List ID**
```sh
python trello_helper.py --api-key YOUR_API_KEY --token YOUR_TRELLO_TOKEN --get-list-ids YOUR_BOARD_ID
```
Copy the **List ID** where you want to create a card.

### **3. Find Your Label ID (Optional)**
```sh
python trello_helper.py --api-key YOUR_API_KEY --token YOUR_TRELLO_TOKEN --get-label-ids YOUR_BOARD_ID
```
Copy the **Label ID** if you want to add labels to the card.

### **4. Create a Trello Card**
```sh
python trello_main.py --api-key YOUR_API_KEY --token YOUR_TRELLO_TOKEN \
--board-id YOUR_BOARD_ID --list-id YOUR_LIST_ID --name "New Task" \
--description "Task details here" --labels LABEL_ID1 LABEL_ID2 --comment "This is a comment"
```

---

## Example Usage
```sh
python trello_main.py --api-key 123abc --token xyz789 \
--board-id 67b7bc7d40db64e1936d83c0 --list-id 60b4dcba3e8e1a1234567890 \
--name "Fix Bug #124" --description "Resolve critical issue in API" \
--labels Bug Urgent --comment "This is a high-priority fix."
```

---

## Notes
- **If you pass a label name instead of an ID, the script will automatically convert it to an ID.**
- If you **forget the Board ID or List ID**, just run the helper commands to retrieve them.
- This tool is designed for **productivity-focused users** who prefer working with the terminal over the web UI.

---

## Credits
Developed by **Alper Kutay Ozbek**
GitHub: [AlperKutay](https://github.com/AlperKutay)
Date: **February 22, 2025**

---

## Notes

- **If you pass a label name instead of an ID, the script will automatically convert it to an ID.**
- If you **forget the Board ID or List ID**, just run the helper commands to retrieve them.
- This tool is designed for **productivity-focused users** who prefer working with the terminal over the web UI.

---

## Comments

Firstly, I have written the `trello_helper.py` file to learn how the Trello API works.\
The most important thing to achieve this assignment was understanding which **URL** to use.\
I used the following base URL: `https://api.trello.com/1`, and all other URLs were sourced from the Trello API documentation.

After obtaining the API token, I was able to access **boards, lists, and labels**. Then, I utilized the API to create a card with **labels and comments**.

Additionally, I used **ChatGPT** to help with the usage of **argparse**, parsing **JSON data**, and writing the **README file**.
And I spent approximately 10 hours to complete this assignment.
### **Resources Used:**

- [Trello Boards API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)
- [Trello Cards API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)
- [Trello Labels API](https://developer.atlassian.com/cloud/trello/rest/api-group-labels/)

I have designed the code in a way that clearly indicates which IDs to use.\
There are many IDs involved, and I initially struggled to differentiate between them. To make things easier, I structured the code to be user-friendly and intuitive.

### Alper Kutay OZBEK
### 2025/02/22

## License
This project is licensed under the MIT License. Feel free to use and modify!



