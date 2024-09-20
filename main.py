import speech_recognition as sr
import wikipediaapi
import requests
from bs4 import BeautifulSoup

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:500]  # Return first 500 characters of the summary
    else:
        return "No Wikipedia page found."

def scrape_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    if snippets:
        return snippets[0].text
    else:
        return "No relevant Google data found."

def main():
    query = recognize_speech()

    if "wikipedia" in query:
        query = query.replace("wikipedia", "")
        response = search_wikipedia(query.strip())
        print(f"Wikipedia says: {response}")
    elif "google" in query:
        query = query.replace("google", "")
        response = scrape_google(query.strip())
        print(f"Google result: {response}")
    else:
        print("Please ask for either Wikipedia or Google search.")

if __name__ == "__main__":
    main()
