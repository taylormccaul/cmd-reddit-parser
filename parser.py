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
data2 = """"""

#print("Searching...")
#time.sleep(3)
html_file = open("rss.html", "w")
xml_data = open("rss.xml", "r")
headings = ["<!DOCTYPE html>\n", "<html>\n", "<head>\n", "<title>RSS FEED</title>\n", "<style>\n", "</style>\n", "</head>\n", "<body>\n"]

for item in headings:
    data2 +=(item)

#xml_data = urllib.request.urlopen("https://www.reddit.com/r/" + link.lower() + "/.rss")
for line in xml_data:
    data += line.strip()#line.decode().strip()
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
"<div class=\"md\">", "<br/>", "<ul>", "</ul>", "</a>"]

for entry in entries:
    data2 += "<div class=\"entry\">\n"
    #title = "<div class=\"title\">" + entry.find('title').text + "</div>\n"
    title = entry.find('title').text
    author = "<div class=\"author\">" + entry.find('author')[0].text + "</div>\n"
    original_link = "<a href=\"" + entry.find('link').attrib['href'] + "\">"
    #data2 += "<a href=\"" + original_link + "\">\n"

    content = entry.find('content').text

    for item in replace_list:
        content = content.replace(item, "")

    for link in re.finditer('<a\s+(?:[^>]*?\s+)?href=([\"\'])(.*?)\\1>', content):
        if re.search('<a\s+(?:[^>]*?\s+)?href=([\"\'])https://www.reddit.com\/r\/\w+\/comments\/(.*?)>', link.group(0)) != None and link.group(0)[9:len(link.group(0)) - 2] != original_link:
            content = content.replace(link.group(0), "<a href=\"" + link.group(0)[9:len(link.group(0))-2] + "\">" + title + "</a>\n")#" ")
            #print(content.replace(link.group(0), "<a href=\"" + link.group(0)[9:len(link.group(0))-2] + "\">" + title + "</a>\n"))
        else:
            content = content.replace(link.group(0), '')
        for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
            for src in re.finditer('src=([\"\'])(.*?)\\1', img.group(0)):
                content = content.replace(img.group(0), "<img src=\"" + src.group(0)[5:len(src.group(0))-1] + "\">\n")

    content = content.replace("&amp;", "&")
    content = content.replace("&#39;", "'")
    content = content.replace("&quot;", "\"")
    split_content = content.partition('</div>')[0]

    if "&#32" in split_content:
        data2 += author
        data2 += "<div class=\"updated\">" + entry.find('updated').text + "</div>\n"
        data2 += split_content.partition('&#32')[0].strip()
    elif original_link + title + "</a>\n" not in split_content and "&#32" not in split_content:
        data2 += author
        #data2 += original_link + title + "</a>\n"
        data2 += "<div class=\"updated\">" + entry.find('updated').text + "</div>\n"
        data += split_content.strip()
    else:
        data2 += author
        #print(original_link)
        data2 += original_link + title + "</a>\n"
        data2 += "<div class=\"updated\">" + entry.find('updated').text + "</div>\n"
        data += split_content.strip()
    data2 += ("</div>\n")
data2 += "</body>\n"
data2 += "</html>"
html_file.write(data2)
html_file.close()
xml_data.close()


"""
### KEEP FOR ORIGINAL XML PARSER ###
replace_list = ["<p>", "</p>", "<tr>", "</tr>", "<td>",
"</td>", "<table>", "</table>", "<!-- SC_OFF -->",
"<div class=\"md\">", "</a>", "<strong>", "</strong>",
"<br/>", "<h1>", "</h1>", "<ul>", "</ul>"]
"""

"""KEEEEEEPPPPPPPPPfor entry in entries:
    data2 += "<div class=\"entry\">"
    data2 += "<div class=\"title\">" + entry.find('title').text + "</div>"
    data2 += "<div class=\"author\">" + entry.find('author')[0].text + "</div>"
    data2 += "<div class=\"updated\">" + entry.find('updated').text + "</div>"
    original_link = entry.find('link').attrib['href']
    data2 += "<a href=\"" + original_link + "\">"
    data2 += "<table>"
    data += "<tr>"
    #print("Title:", entry.find('title').text)
    #print("User:", entry.find('author')[0].text)
    #print("Last updated:", entry.find('updated').text)
    #original_link = entry.find('link').attrib['href']
    #print("Original link:", original_link)

    content = entry.find('content').text
    #print("<div class=\"content\">")
    for item in replace_list:
        content = content.replace(item, "")

    for link in re.finditer('<a\s+(?:[^>]*?\s+)?href=([\"\'])(.*?)\\1>', content):
        if re.search('<a\s+(?:[^>]*?\s+)?href=([\"\'])https://www.reddit.com\/r\/\w+\/comments\/(.*?)>', link.group(0)) != None and link.group(0)[9:len(link.group(0)) - 2] != original_link:
            content = content.replace(link.group(0), "<a href=\"" + link.group(0)[9:len(link.group(0))-2] + "\">\n")#" ")
        else:
            content = content.replace(link.group(0), '')
        for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
            for src in re.finditer('src=([\"\'])(.*?)\\1', img.group(0)):
                content = content.replace(img.group(0), "<img src=\"" + src.group(0)[5:len(src.group(0))-1] + "\">\n")

    content = content.replace("&amp;", "&")
    content = content.replace("&#39;", "'")
    content = content.replace("&quot;", "\"")
    #KEEPcontent = content.replace("<li>", "* ")
    #KEEPcontent = content.replace("</li>", "\n")

    split_content = content.partition('</div>')[0]

    if "&#32" in split_content:
        #KEEPprint("Post:", split_content.partition('&#32')[0].strip())
        data2 += split_content.partition('&#32')[0].strip()
        print(data2)
        #KEEPprint(split_content.partition('&#32')[0].strip())
    else:
        #print("Post:", split_content.strip())
        data += (split_content.strip())
    data2 += ("</div>")
    #data2 += ("</div>")
    #KEEPprint('\n')
    #KEEPinput('')
#print(data2)"""
