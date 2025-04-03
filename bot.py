import requests
import telegram
from datetime import datetime
import time

# Your API keys (SportsMonk and others)
api_keys = [
    "10K1q8aHCHcC2zJn4SIoAPmF0L6GePM2o7bQnaRF25ftQTUAdG11BYiZTUUj",  # Example API key 1
    "ddac830e88b36908d910d3a6243febe0",  # Example API key 2
    "9446479bb0f51557d3e219ad87d0823c",  # Example API key 3
    "0d3fbebb6a0f480d882b6cbe6c94935b",  # Example API key 4
]

# Telegram bot token
TELEGRAM_TOKEN = "7468130122:AAGemkwMbVxUYGufj8ILwtfNzs3oed41Gx0"  # Your actual bot token
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Replace with your chat ID or group ID
chat_id = "@YOUR_GROUP_OR_CHANNEL_NAME"  # Replace with your actual Telegram chat ID or group ID

def fetch_bets():
    # Function to fetch the bets from the API
    for api_key in api_keys:
        url = f"https://api.sportsmonk.com/v1/odds"  # Adjust the API endpoint for fetching odds or bets
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        
        if response.status_code == 200:
            return response.json()  # Return the bet data if successful
        else:
            print(f"Error fetching data from API. Status code: {response.status_code}")
            continue
    return None

def fetch_live_score(match_name):
    # Function to fetch live scores
    for api_key in api_keys:
        url = f"https://api.sportsmonk.com/v1/matches?name={match_name}"  # Adjust this for the live score API
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        
        if response.status_code == 200:
            return response.json()  # Return the match score if successful
        else:
            print(f"Error fetching score. Status code: {response.status_code}")
            continue
    return "No score found for this match."

def send_message(message):
    # Function to send messages to the Telegram bot
    bot.send_message(chat_id=chat_id, text=message)

def main():
    # Main function that runs the bot continuously
    while True:
        user_input = input("Enter your request (type 'exit' to quit): ")

        if user_input.lower() == "exit":
            break
        
        if "check result" in user_input.lower():
            match_name = user_input.replace("check result", "").strip()
            score = fetch_live_score(match_name)
            send_message(f"Score for {match_name}: {score}")
        
        else:
            bets = fetch_bets()
            if bets:
                # Format the bet message as needed
                formatted_bets = "\n".join([f"{bet['match']} - {bet['odds']}" for bet in bets['data']])
                send_message(f"Today's bets: \n{formatted_bets}")
            else:
                send_message("No bets available at the moment.")
        
        time.sleep(10)  # Sleep for 10 seconds to avoid API rate limits

if __name__ == "__main__":
    main()
