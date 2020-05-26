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

#time.sleep(5)

#print("Searching...")
xml_data = open("rss.xml", "r")
#xml_data = urllib.request.urlopen("https://www.reddit.com/r/" + link.lower() + "/.rss")
for line in xml_data:
    data += line.strip()#line.decode().strip()

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
"<br/>"]

for entry in entries:
    print("Title:", entry.find('title').text)
    print("User:", entry.find('author')[0].text)
    print("Last updated:", entry.find('updated').text)

    content = entry.find('content').text

    for item in replace_list:
        content = content.replace(item, "")

    for link in re.finditer('<a\s+(?:[^>]*?\s+)?href=([\"\'])(.*?)\\1>', content):
        content = content.replace(link.group(0), "")

    for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
        for src in re.finditer('src=([\"\'])(.*?)\\1', img.group(0)):
            content = content.replace(img.group(0), src.group(0)[5:len(src.group(0))-1])
    split_content = content.partition('</div>')[0]

    if "&#32" in split_content:
        print(split_content.partition('&#32')[0].strip())
    else:
        print(split_content.strip())

    for m in re.finditer(r'<span><a href=\"https://\w*.\w*.\w*/\w*.*/*\w*></span>', content):
        for n in re.finditer(r'https://[www]*[i]*.\w+.\w+.\w+/\w+/*\w*/*\w*', m.group(0)):
            if re.search("https://www.reddit.com.\w+/\w+/*\w*/*\w*", n.group(0)) == None and re.search("https://[(i)(media3)(imgur)(giphy)]+[www]{0}.\w+.\w+.\w+/\w+/*\w*/*\w*", m.group(0)) == None: #(re.search("https://i.\w+.\w+.\w+/\w+/*\w*/*\w*", n.group(0)) != None):
                print('External link: %s' % (n.group(0)))
            elif re.search("https://[(i)(media3)(imgur)(giphy)]+[www]{0}.\w+.\w+.\w+/\w+/*\w*/*\w*", m.group(0)) != None and re.search("https://www.reddit.com.\w+/\w+/*\w*/*\w*", n.group(0)) == None:
                print('Image: %s' % (n.group(0)))
            else:
                post = n.group(0)
                if post_check[post_counter] == post:
                    print("")
                else:
                    print('Post: %s' % (n.group(0)))
                    post_check.append(post)
                    post_counter += 1
    print('\n')
    input('')
