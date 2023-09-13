import requests
import bs4
# from kutils.python.kurosoup import KuroSoup

def get_character_data(url):
  # TODO: Get Name
  # TODO: Get Description
  # TODO: Get Artworks via /gallery
  # TODO: (For Frontend) Prompt which artwork to use as the character's image and ref sheet
  pass


def main():
  
  victim= "reshireve"
  base_url = "https://toyhou.se/"
  req = requests.get(f"{base_url}{victim}/characters")
  soup = bs4.BeautifulSoup(req.text, "html.parser")
  characters = []
  folder_links = soup.findAll("a", class_="characters-folder")
  character_links = soup.findAll("a", class_="character-thumb")
  folders = [{ "href": folder.get("href"), "name": folder.find("div", class_="characters-folder-name").get_text()} for folder in folder_links]  
  characters = [characters.get("href") for characters in character_links]  
  # TODO: Go through each folder and get the characters
  for data in folders:
    link = data['href']
    folder_req = requests.get(link)
    folder_soup = bs4.BeautifulSoup(folder_req.text, "html.parser")
    folder_character_links = folder_soup.findAll("a", class_="character-thumb")
    folder_characters = [{ "href": characters.get("href"), "folder": folders["name"] } for characters in folder_character_links]

    characters.extend(folder_characters)
  print(len(characters))
  # TODO 2: Go through each character and get the character's info
  print(len(character_links))
  
  

if __name__ == "__main__":
  main()