# This script will generate an html preview file of a specified open-dir.
# Use at your own risk.
# 2xdropout 2024
import requests
from bs4 import BeautifulSoup


def generate_html_file_end():
    bodyEnd = "</body>"
    htmlEnd = "</html>"

    return bodyEnd+htmlEnd


def generate_html_file_start():
    doctype = "<!DOCTYPE html>"
    htmlStart = "<html>"
    head = "<head><title>Open-Dir webPreview</title></head>"
    body = "<body style='background-color:black;color:red;text-align:center'>"

    return doctype+head+body


def generate_preview_line(linkItem,webURL):
    linkItemURL = webURL+linkItem.strip()
    style = "width:65vw;height:65vh;background-color:white;color:black;display:block;margin:auto;"
    htmlString = "<div><p>"+linkItem+"</p><iframe style='"+style+"'src='"+ linkItemURL +"'></iframe><div>"

    return htmlString


def main():
    fileName = "./webPreview.html"
    lineCountSuccess = 0
    lineCountFailure = 0

    webURL = input("Please paste the url of the open directory:  ")
    returnedContent = requests.get(webURL,verify=False)

    soup=BeautifulSoup(returnedContent.text, "html.parser")

    openDirLinks = soup.find_all('a')

    with open(fileName,'w') as file:
        print("\n")
        file.write(generate_html_file_start())
        for item in openDirLinks:
            print("\nGenerating line for link:  ", item.text)

            try:
                previewLine = generate_preview_line(item.text,webURL)
            except Exception as e:
                print("FAILED TO GENERATE PREVIEW LINE")
                print(e)
            try:
                file.write(previewLine)
                lineCountSuccess += 1
            except Exception as e:
                print("FAILED TO WRITE PREVIEW LINE TO FILE")
                print(e)
                lineCountFailure += 1
            
            print("\n")

        file.write(generate_html_file_end())
    file.close()

    print("Succeded In Writting:  "+lineCountSuccess+" Lines\nFailed To Write:  "+lineCountFailure+" Lines")
    print("\n\nDONE")


main()
