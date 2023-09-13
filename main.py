import asyncio
import requests
import bs4
# from kutils.python.kurosoup import KuroSoup

def get_character_data(url):
  req = requests.get(url)
  soup = bs4.BeautifulSoup(req.text, "html.parser")
  name = soup.find("h1", class_="display-4").get_text()
  try:
    description = soup.find("div", class_="profile-content-content").find("p").get_text()
  except:
    description = "No description."
  gallery_req = requests.get(f"{url}/gallery")
  gallery_soup = bs4.BeautifulSoup(gallery_req.text, "html.parser")
  artworks = gallery_soup.findAll("div", class_="gallery-thumb")
  artworks = [{ "href": f'{artwork.find("img").get("src")}'} for artwork in artworks]
  print(artworks)
  results = {
    "name": name,
    "description": description,
    "artworks": artworks
  }
  return results


def get_toyhouse_data(username):
  base_url = "https://toyhou.se"
  print(f"Username: {username}")
  print(f"Host: {base_url}")
  print("Getting folders...")
  req = requests.get(f"{base_url}/{username}/characters")
  soup = bs4.BeautifulSoup(req.text, "html.parser")
  characters = []
  folder_links = soup.findAll("a", class_="characters-folder")
  character_links = soup.findAll("a", class_="character-thumb")
  folders = [{ "href": folder.get("href"), "name": folder.find("div", class_="characters-folder-name").get_text()} for folder in folder_links]  
  characters = [characters.get("href") for characters in character_links]  
  # TODO: Go through each folder and get the characters
  print(f"Found {len(folders)} folders.")
  print(f"Getting Folder Data (Will take {len(folders) * 5} seconds))")
  for data in folders:
    link = data['href']
    folder_req = requests.get(link)
    folder_soup = bs4.BeautifulSoup(folder_req.text, "html.parser")
    folder_character_links = folder_soup.findAll("div", class_="character-thumb")
    folder_characters = [{ "href": f'{base_url}{characters.find("a").get("href")}', "folder": data['name']} for characters in folder_character_links]
    characters.extend(folder_characters)
  print(f"Found {len(characters)} characters.")
  print(f"Getting Character Data (Will take {len(characters) * 5} seconds))")
  final_characters = []
  # TODO Go through each character and get the data via get_character_data
  for character in characters:
    print(character)
    final_characters.append(get_character_data(character['href']))
  return final_characters
  
  

if __name__ == "__main__":
  main()