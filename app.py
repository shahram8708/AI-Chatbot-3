from flask import Flask, render_template, request
import re
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

patterns_responses = [
    (r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]),
    (r"how are you|how are things", ["I am doing good, how about you?", "Doing well! How about you?"]),
    (r"(.*) your name?", ["I'm Chatbot, nice to meet you!"]),
    (r"what can you do", ["I can assist you with a variety of tasks like answering questions, providing information, or even just chatting if you'd like."]),
    (r"where are you located", ["I exist in the digital realm, accessible wherever you need me!"]),
    (r"who created you", ["I was created by a team of developers at Ram."]),
    (r"how does your technology work", ["I utilize natural language processing and machine learning algorithms to understand and respond to your queries."]),
    (r"can you help me with (.*)", ["Sure, I'll do my best. What do you need assistance with?"]),
    (r"do you have a personality", ["I try to be friendly and helpful, but ultimately, I'm just a program running some code!"]),
    (r"are you human", ["No, I'm a chatbot designed to assist you with your inquiries."]),
    (r"do you sleep", ["No, I'm available 24/7 to help you whenever you need assistance."]),
    (r"how old are you", ["I was created on 2024, so you could say I'm as old as my development."]),
    (r"what languages do you speak", ["I'm proficient in multiple languages. Feel free to communicate with me in any language you're comfortable with."]),
    (r"tell me a joke", ["Sure, here's one: Why don't scientists trust atoms? Because they make up everything!"]),
    (r"what's the weather like today", ["Where are you located? I can provide you with the current weather forecast."]),
    (r"what's the meaning of life", ["That's a big question! Philosophers have debated it for centuries. Some say it's about finding happiness, others say it's about personal growth and fulfillment."]),
    (r"recommend a (.*)", ["Certainly! What genre or type of cuisine are you interested in?"]),
    (r"what's the capital of (.*)", ["The capital of \\1 is..."]),
    (r"help me with my homework", ["I can certainly try! What subject are you working on?"]),
]

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

def scrape_google_search_results(question):
    content = google_search(question)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        first_result = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
        if first_result:
            return first_result.get_text()
    return None

def respond(user_input):
    for pattern, responses in patterns_responses:
        match = re.match(pattern, user_input.lower())
        if match:
            response = random.choice(responses)
            return response.format(*match.groups())
    search_results = scrape_google_search_results(user_input)
    if search_results:
        return search_results
    else:
        return "Sorry, I couldn't find any relevant information."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"].strip()
    response = respond(user_input)
    response = re.sub(r'\b\d{1,2}\s*(?:st|nd|rd|th)?(?:\s*(?:of)?\s*\w+)?(?:,\s*\d{4})?\b', '', response)
    return response

if __name__ == "__main__":
    app.run(debug=True)
