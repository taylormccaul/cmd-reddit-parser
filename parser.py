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
#If the user entered only one argument, open an input dialog prompting the user to enter the missing argument
    except:
        link = input("Enter the name of a subreddit to parse (e.g. AskReddit): \n")

#Declare an empty multiline string called 'data' to hold the raw XML data
data = """"""

print("Searching...")
#time.sleep(3)

#Open a file called 'rss.html' to store the parsed XML in HTML format
html_file = open("rss.html", "w+")
#Store the data in a variable called 'xml_data'
xml_data = open("rss.xml", "r")
#xml_data = urllib.request.urlopen("https://www.reddit.com/r/" + link.lower() + "/.rss")

#List of headings used in formatted HTML
headings = ["<!DOCTYPE html>\n", "<html>\n", "<head>\n", "<title>RSS Feed</title>\n", "<link href=\"./parser.css\" rel=\"stylesheet\">\n", "</head>\n", "<body>\n", "<h1>r/{}</h1>\n".format(link)]

#Loop over the list of headings, adding each one to the html_file file
for item in headings:
    html_file.write(item)

#Read each line of the data, adding the decoded bytes to the data variable
for line in xml_data:
    """UPDATE BEFORE CALLING XML"""
    data += line.strip()
    #data += line.decode().strip()

#Replace the '<feed xmlns...>' header and values with a plain '<feed>' root header
m = re.search("<feed xmlns=\"http[s]*:\/\/\w+\W+\w+\W+\w+\/\w*\/\w*\">", data)
if m != None:
    data = data.replace(data[m.span()[0]:m.span()[1]], "<feed>")

#Declare a variable called tree to be the root node for the elements parsed from XML
tree = ET.fromstring(data)

#Find all elements with the tag '<entry>' in the data
entries = tree.findall('entry')

#List of all elements in the XML to be replaced
replace_list = ["<tr>", "</tr>", "<td>", "</td>", "<table>", "</table>", "<hr>", "<!-- SC_OFF -->", "<!-- SC_ON -->", "<div class=\"md\">", "<br/>"]

#Loop over each entry
for entry in entries:
    #Variable called content that holds that value of the entry's '<content>' tag
    content = entry.find('content').text
    #If the content contains an image, nest the remaining content in an 'img-entry' div for styling
    if "<img src=" in content:
        html_file.write("<div class=\"img-entry\">\n")
    #Otherwise, nest the remaining content in a 'text-entry' div
    else:
        html_file.write("<div class=\"text-entry\">\n")

    #Add variables for the title, author, post link, and user profile link
    title = "<div class=\"title\">" + entry.find('title').text + "</div>\n"
    author = "<div class=\"author\">" + entry.find('author')[0].text + "</div>\n"
    original_link = "<a href=\"" + entry.find('link').attrib['href'] + "\">"
    user_link = "<a href=\"" + entry.find('author')[1].text + "\">\n"

    #Loop over the items in the replace_list, replacing them with an empty string
    for item in replace_list:
        content = content.replace(item, "")

    #Write a 'text-links' div to the file, nesting the original link, the title, the user profile link, the author, and the time last updated inside
    html_file.write("<div class=\"text-links\">\n")
    html_file.write(original_link + title + "</a>\n")
    html_file.write(user_link + author + "</a>\n")
    html_file.write("<div class=\"updated\">" + entry.find('updated').text + "</div>\n")
    html_file.write("</div>\n")

    #Loop over the images in the content, nest them in a link to the original post, and write to the HTML file
    #for img in re.finditer('<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\\1 alt=([\"\'])(.*?)\\1 title=([\"\'])(.*?)\\1 \/>', content):
     #   #img_link = img.group(0)[9:len(img.group(0))-1].split(" ")[0]
    #    html_file.write(original_link + img.group(0) + "</a>\n")

    #Replace HTML char codes for the &, ',  and " characters with their text equivalents
    content = content.replace("&amp;", "&")
    content = content.replace("&#39;", "'")
    content = content.replace("&quot;", "\"")
    z = re.search("https:\/\/\w+.\w+.\w+\/\w+\.*\w*\">", content)
    #if z != None:
    #    print(content[z.span()[0]:z.span()[1]])

    split_content = content.partition('</div>')[0]
    #ADDED
    #split_content = split_content.partition('</a>')[0]

    if "&#32" in content:
        split_content = content.partition('&#32')[0]
        extra_link_index = content.index(content.partition('&#32')[0].strip()[0:len(original_link)])
    if content[extra_link_index:len(original_link) + extra_link_index] in content:
        content.replace(content[extra_link_index:len(content) - 1], "")
        #html_file.write("<div class=\"content\">\n" + content.strip()[0:500] + "...\n</div>\n")
        #print(content.strip()[0:500])
        #print(split_content)
        short_p = split_content.strip().split("</p>")
        #print(short_p)
        #input('')
        #print(split_content)
        try:
            #content = content.replace(content[content.index("<span>"):len(content) - 1], "")
            #content.content.replace(content[content.index("<!-- SC_ON -->"):len(content) - 1], "</div></div>")
            html_file.write("<div class=\"content\">")
            #print(split_content)
            #input("")
            if len(split_content.partition('</div>\n')[0] > 400):
                html_file.write(split_content.partition('</div>\n')[0][0:400] + "...")
                
            """if "<p>" in short_p[0] and "<span>" not in short_p[0]:
                #print(short_p[0] + "</p>")
                html_file.write(short_p[0] + "</p>")
                #print("SHORT P 1:", short_p[0])
            if "<p>" in short_p[1] and "<span>" not in short_p[1] and short_p[0] in html_file:
                #print("SHORT P 2:", short_p[1])
                html_file.write(short_p[1] + "</p>\n")"""
            html_file.write("</div>\n")
        except:
            print("Exception")
            html_file.write(split_content.strip())
            #print(split_content.strip())
        #print(content.strip())
    elif original_link + title + "\n</a>\n" not in content and "&#32" not in content:
        """### ADD DIV TO SEPARATE CONTENT ###"""
        html_file.write("<div class=\"content\">\n" + content.strip()[0:500] + "...\n</div>\n")
        #print(content.strip()[0:500])

    html_file.write("</div>\n")
    html_file.write("\n")

html_file.write("</body>\n")
html_file.write("</html>")
html_file.close()

xml_data.close()
