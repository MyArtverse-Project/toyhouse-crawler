import asyncio
from requests import Session
from bs4 import BeautifulSoup


def get_requests(url: str) -> BeautifulSoup:
    _req = Session().get(url)

    return BeautifulSoup(_req.text, "html.parser")


def get_character_data(url: str):
    soup = get_requests(url)
    name = soup.find("h1", class_="display-4").get_text()
    try:
        description = soup.find(
            "div", class_="profile-content-content").find("p").get_text()
    except:
        description = "Description not provided"

    gallery_soup = get_requests(f"{url}/gallery")
    artworks = gallery_soup.find_all("div", class_="gallery-thumb")
    artworks = [{"href": f'{artwork.find("img").get("src")}'}
                for artwork in artworks]
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

    characters = []

    soup = get_requests(f"{base_url}/{username}/characters")
    folder_links = soup.find_all("a", class_="characters-folder")
    character_links = soup.find_all("a", class_="character-thumb")

    folders = [{"href": folder.get("href"), "name": folder.find(
        "div", class_="characters-folder-name").get_text()} for folder in folder_links]
    characters = [characters.get("href") for characters in character_links]

    # TODO: Go through each folder and get the characters
    print(f"Found {len(folders)} folders!")
    print(f"Getting Folder Data (Will take {len(folders) * 5} seconds))")

    for data in folders:
        link = data['href']
        folder_soup = get_requests(link)
        folder_character_links = folder_soup.find_all(
            "div", class_="character-thumb")
        folder_characters = [
            {"href": f'{base_url}{characters.find("a").get("href")}', "folder": data['name']} for characters in folder_character_links]

        characters.extend(folder_characters)

    print(f"Found {len(characters)} characters.")
    print(f"Getting Character Data (Will take {len(characters) * 5} seconds))")

    final_characters = []

    # TODO Go through each character and get the data via get_character_data
    for character in characters:
        print(character)
        final_characters.append(get_character_data(character['href']))
    return final_characters
