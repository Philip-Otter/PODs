# This script will generate an html preview file of a specified open-dir.
# Use at your own risk.
# 2xdropout 2024
import argparse
import requests
import re
from bs4 import BeautifulSoup

class OutputFile:
    def __init__(self, connectionObject, fileName = "./webPreview.html"):
        self.fileStart = "<!DOCTYPE html>\n<html><head><title>Open-Dir webPreview</title></head>\n<body style='background-color:black;color:red;text-align:center'>"
        self.fileEnd = "\n</body></html>"
        self.fileName = fileName
        self.links = ""
        self.Connection = connectionObject
    

    def CreatePreview(self, linkItem):
        linkItemURL = str(self.Connection.URL)+linkItem.strip()
        style = "width:65vw;height:65vh;background-color:white;color:black;display:block;margin:auto;"
        htmlString = "\n<div><p>"+linkItem+"</p><iframe style='"+style+"'src='"+ linkItemURL +"'></iframe><div>"

        return htmlString


    def WriteFile(self):
        if(len(self.links) == 0):
            print(f"NO MATCHING LINKS FOUND AT THE GIVEN SITE:      {self.Connection.URL}")
            exit()

        with open(self.fileName,'w') as file:
            print("\n")
            file.write(self.fileStart)
            for item in self.links:
                print("\nGenerating line for link:  ", item.text)

                try:
                    previewLine = self.CreatePreview(item.text)
                except Exception as e:
                    print(f"FAILED TO GENERATE PREVIEW LINE:  {item.text}")
                    print(e)
                try:
                    file.write(previewLine)
                except Exception as e:
                    print("FAILED TO WRITE PREVIEW LINE TO FILE")
                    print(e)
                
                print("\n")

            file.write(self.fileEnd)
        file.close()
    
class Connection:
    def __init__(self, host):
        self.URL = host
        self.soup = ""
        self.filter = ""
    

    def SearchContent(self):
        if(self.filter != ""):
            filterRegex = re.compile(str(self.filter))
            return self.soup.find_all('a', {"href":filterRegex})
        else:
            return self.soup.find_all('a')


    def GetContent(self):
        returnedContent = requests.get(self.URL,verify=False)
        self.soup=BeautifulSoup(returnedContent.text, "html.parser")

        return self.SearchContent()
    


def main():
    parser = argparse.ArgumentParser(description='PODs, an open-dir preview tool')

    parser.add_argument('-H', '--host', help='Set the open-dir host location')
    parser.add_argument('-o', '--outputFile', help='Set the output file for the preview HTML page')
    parser.add_argument('-m', '--matchType', help='Only return matched file types based on the provided extension')

    args = parser.parse_args()

    if(args.host == None):
        print("Host value required for PODs to run!")
        exit()
    else:
        con = Connection(args.host)
    if(args.outputFile != None):
        outFile = OutputFile(con, args.outputFile)
    else:
        outFile = OutputFile(con)
    
    if(args.matchType != None):
        con.filter = "\."+str(args.matchType)
    
    outFile.links = con.GetContent()
    print(outFile.links)
    outFile.WriteFile()


main()
