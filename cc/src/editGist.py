#!/usr/bin/python3

# NOTE: github_gist.key must contain a key from github that has GIST permissions.
# Posts the Gist, prints the Gist ID and URL

import os.path
import requests
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generates a gistPost based on input")

    parser.add_argument(
        "-file",
        type=str,
        default=None,
        help="Path to file that contains the upload content. Example: recipe.txt",
        dest="file",
        required=True,
    )
    parser.add_argument(
        "-name",
        type=str,
        default=None,
        help="Name of the file that's being edited on the gist",
        required=False
    )
    parser.add_argument(
        "-id",
        type=str,
        default=None,
        help="ID of the gist to edit",
        dest="gistID",
        required=True,
    )
    parser.add_argument(
        "-d",
        type=str,
        default=None,
        help="Description of the uploaded content",
        dest="description",
        required=False,
    )
    parser.add_argument("-public", action="store_true")
    parser.add_argument("-private",action="store_true")

    args = parser.parse_args()

    # Get location of the pyscript
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    # Location of the stories folder
    STORY_FOLDER = os.path.join(__location__, "./stories")
    # Get location of the keyfile
    KEYFILE_LOC = os.path.join(__location__, "github_gist.key")

    # Get API KEY from github_gist.key
    with open(KEYFILE_LOC, "r") as keyfile:
        API_KEY = keyfile.read().strip(" ").strip("\n")

    # Check if key exists
    if API_KEY == "":
        print(f"API KEY not found in {KEYFILE_LOC}\nPlease place API key in keyfile.")

    # API URL for gists
    GITHUB_URL = f"https://api.github.com/gists/{args.gistID}"


    # Build the data
    headers = {f"Authorization": f"token {API_KEY}"}
    params = {"scope": "gist"}
    with open(os.path.join(STORY_FOLDER, args.file), "r") as f:
        content = f.read()
    if args.name is not None:
        name = args.name
    else:
        name = args.file
    data = {"files": {name:{"content":content}}}

    if args.description is not None:
        data["description"] = args.description
    if args.public:
        data['public'] = True
    elif args.private:
        data['public'] = True
    

    res = requests.patch(
        GITHUB_URL, headers=headers, params=params, data=json.dumps(data)
    )
    
    print(f"{res.status_code}")

if __name__ == "__main__":
    main()
