import xml.etree.ElementTree as ET
import urllib.request
import time
import sys
import re

#Check that user entered the proper number of arguments
#If the user entered more than two arguments, raise an exception error, reminding them of proper usage
if len(sys.argv) > 2:
    raise Exception("Correct usage: python redditparser.py subreddit")
else:
#If the arguments are equal to two, set the value of the 'link' variable to the second argument
    try:
        link = sys.argv[1]
        #print(link)
#If the user entered only one argument, open an input dialog prompting the user to enter the missing argument
    except:
        link = input("Enter the name of a subreddit to parse (e.g. AskReddit): \n")

#Declare an empty multiline string called 'data' to hold the raw XML data
data = """"""

print("Searching...")
#time.sleep(3)

#Open a file called 'rss.html' to store the parsed XML in HTML format
html_file = open("rss.html", "w+")
xml_data = open("rss.xml", "r")

#List of headings used in formatted HTML
headings = ["<!DOCTYPE html>\n", "<html>\n", "<head>\n", "<title>RSS FEED</title>\n", "<style>\n", "</style>\n", "</head>\n", "<body>\n"]

#Loop over the list of headings, adding each one to the html_file file
for item in headings:
    html_file.write(item)

#xml_data = urllib.request.urlopen("https://www.reddit.com/r/" + link.lower() + "/.rss")
for line in xml_data:
    """UPDATE BEFORE CALLING XML"""
    data += line.strip()
    #time.sleep(2)

m = re.search("<feed xmlns=\"http[s]*:\/\/\w+\W+\w+\W+\w+\/\w*\/\w*\">", data)
if m != None:
    data = data.replace(data[m.span()[0]:m.span()[1]], "<feed>")

tree = ET.fromstring(data)

entries = tree.findall('entry')
post_check = [1]
post_counter = 0

replace_list = ["<tr>", "</tr>", "<td>",
"</td>", "<table>", "</table>", "<!-- SC_OFF -->",
"<div class=\"md\">", "<br/>", "<ul>", "</ul>"]

for entry in entries:
    content = entry.find('content').text
    if "<img src=" in content:
        html_file.write("<div class=\"img-entry\">\n")
    else:
        html_file.write("<div class=\"text-entry\">\n")
    title = "<div class=\"title\">" + entry.find('title').text + "</div>\n"
    author = "<div class=\"author\">" + entry.find('author')[0].text + "</div>\n"
    original_link = "<a href=\"" + entry.find('link').attrib['href'] + "\">"
    user_link = "<a href=\"" + entry.find('author')[1].text + "\">\n"


    for item in replace_list:
        content = content.replace(item, "")

    html_file.write(original_link + title + "</a>\n")
    html_file.write(user_link + author + "</a>\n")

    for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
        #img_link = img.group(0)[9:len(img.group(0))-1].split(" ")[0]
        html_file.write(original_link + img.group(0) + "</a>\n")


    content = content.replace("&amp;", "&")
    content = content.replace("&#39;", "'")
    content = content.replace("&quot;", "\"")
    split_content = content.partition('</div>')[0]

    if "&#32" in split_content:
        html_file.write("<div class=\"updated\">" + entry.find('updated').text + "</div>\n")
        extra_link_index = split_content.index(split_content.partition('&#32')[0].strip()[0:len(original_link)])

        if split_content[extra_link_index:len(original_link) + extra_link_index] in split_content:
            split_content.replace(split_content[extra_link_index:len(split_content) - 1], "")
    elif original_link + title + "</a>\n" not in split_content and "&#32" not in split_content:
        html_file.write("<div class=\"updated\">" + entry.find('updated').text + "</div>\n")
        """### ADD DIV TO SEPARATE CONTENT ###"""
        html_file.write(split_content.strip())

    html_file.write("</div>\n")
    html_file.write("\n")

html_file.write("</body>\n")
html_file.write("</html>")
html_file.close()

xml_data.close()
