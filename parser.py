import xml.etree.ElementTree as ET
import urllib.request
import time
import sys
import re

if len(sys.argv) > 2:
    raise Exception("Correct usage: python redditparser.py subreddit")

else:
    try:
        link = sys.argv[1]
        print(link)
    except:
        link = input("Enter the name of a subreddit to parse (e.g. AskReddit): \n")

data = """"""

print("Searching...")
time.sleep(3)
#xml_data = open("rss.xml", "r")
xml_data = urllib.request.urlopen("https://www.reddit.com/r/" + link.lower() + "/.rss")
for line in xml_data:
    data += line.decode().strip()

m = re.search("<feed xmlns=\"http[s]*:\/\/\w+\W+\w+\W+\w+\/\w*\/\w*\">", data)
if m != None:
    data = data.replace(data[m.span()[0]:m.span()[1]], "<feed>")

tree = ET.fromstring(data)

entries = tree.findall('entry')
#entry = tree.find('entry')
post_check = [1]
post_counter = 0
replace_list = ["<p>", "</p>", "<tr>", "</tr>", "<td>",
"</td>", "<table>", "</table>", "<!-- SC_OFF -->",
"<div class=\"md\">", "</a>", "<strong>", "</strong>",
"<br/>", "<h1>", "</h1>", "<ul>", "</ul>"]

for entry in entries:
    print("Title:", entry.find('title').text)
    print("User:", entry.find('author')[0].text)
    print("Last updated:", entry.find('updated').text)
    original_link = entry.find('link').attrib['href']
    print("Original link:", original_link)

    content = entry.find('content').text

    for item in replace_list:
        content = content.replace(item, "")

    #x = re.search('<link href=("https://www.reddit.com(\/r\/)+.*)+>', content)
    for link in re.finditer('<a\s+(?:[^>]*?\s+)?href=([\"\'])(.*?)\\1>', content):
        if re.search('<a\s+(?:[^>]*?\s+)?href=([\"\'])https://www.reddit.com\/r\/\w+\/comments\/(.*?)>', link.group(0)) != None and link.group(0)[9:len(link.group(0)) - 2] != original_link:
            content = content.replace(link.group(0), link.group(0)[9:len(link.group(0))-2] + " ")
        else:
            content = content.replace(link.group(0), '')
        #x = re.search('<a href=("https://www.reddit.com(\/r\/)+.*)+>', content)
        #content = content.replace(link.group(0), "")
        for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
            for src in re.finditer('src=([\"\'])(.*?)\\1', img.group(0)):
                content = content.replace(img.group(0), src.group(0)[5:len(src.group(0))-1])

    content = content.replace("&amp;", "&")
    content = content.replace("&#39;", "'")
    content = content.replace("&quot;", "\"")
    content = content.replace("<li>", "* ")
    content = content.replace("</li>", "\n")

    split_content = content.partition('</div>')[0]

    if "&#32" in split_content:
        print("Post:", split_content.partition('&#32')[0].strip())
    else:
        print("Post:", split_content.strip())
    print('\n')
    input('')
