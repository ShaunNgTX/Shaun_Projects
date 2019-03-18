
# Web_test.py for lab1

from bottle import route, run, template, get, post, request, error, Response
from collections import Counter
from operator import itemgetter
import redis
#adding something here

backup = ""
text1 = ""
hi = redis.Redis()
i = 0 #i is how many urls inside
url_id="" #for the URL storage

Response(headers={"X-Frame-Options": "sameorigin"})

@route('/')

def search():


    html = """
    <html>
    <head>
    <title>Welcome to my Search Page!</title>
    <style type="text/css">
    body
    {background-color:lightblue;} 
    h1
    {
    text-align:center;
    }
    h2
    {
    text-align:center;
    height:300px;
    }
    p
    {
    width:100%;
    height: 10px;
    text-align:center;
    font-size:170%;
    }
    v
    {
    width:100%;
    height: 300px;
    text-align:center;
    font-size:120%;
    vertical-align:middle;
    }
    v2
    {
    width:100%
    } 

    </style>
    </head>
    
    <h1>Welcome to my Search Page</h1>
    <h2> By: Victor & Shaun</h2>
    <P>Enter keywords to search: </P>
    <v><form action="/s" method="get" style="text-align:center;" autocomplete="off">
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form></v>

    <v2><i>If unsatisfactory, please click <a href="http://www.google.com">here</a> !</i></v2>
   
    </body>
    </html>

"""
    global text
    text = request.query.keywords
    return html

#get a search bar with search button

@route('/s', method = "GET")

def output():


    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
"""
    
    global text
    text = request.query.keywords
    global backup
    backup += text + " "

    if text != "":

        global text1
        global url_id
        textstr = str(text)
        text = textstr.lower().split() #get all lower case and split individually
        text1 = textstr.lower().split(' ', 1)[0]

        check = "" #duplicate word checker for the original text
        checker = "" #duplicate word checker for the history
        sorter = "" #for the sorting of the history
        
        history = backup
        firstword_id = "nothing"

        for words_id in text:
            if hi.get(words_id) is None: 
                pass
            elif hi.get(words_id) is not None: 
                firstword_id = hi.get(words_id)
                word_id = firstword_id.replace("word_id_", "")
                smember_id = 'inv_index_word_' + word_id  
                url_id = hi.smembers(smember_id)  
                checkme = 0
                break
        if firstword_id == "nothing":
            html += """
                <table align="center" id='ErrorMessage'>
                <caption style="text-align:center;">
                <b><i><font size ="12">Oops.. No Results Found</b></i></font></caption>
                <tr>

                <th align="center;" >
                <b><font size = "10"><i>Please set a new search parameter</b></font></i></th>
                </body>
                </style>
                </html>
            """
            return html


        global i
        i = 0
        
        html += """
        <html>
        <head>
        <style>
        .box{
            display: none;
            width: 100%;
        }

        a:hover + .box,.box.hover{
            display:block;
            position: relative;
            z-index: 100;
        }
        td {
            padding:50px;
        }
        </style>
        </head>
        </html>

        <table align="center" id='URLS'>
        <caption style="text-align:center;">
        <b>Search Results</b></caption>

        """

        for numbers in url_id:
            i += 1

        for numbers in url_id:
            html += """
            <tr>
                <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
                <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
                </div></td>
            </tr>

            """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
            checkme += 1
            if checkme >= 5:
                break
        html += """

        </table>
        """

        html += """
            <html>
            <head>
            <style>
            .center {
                text-align:center;
            }

            .pagination {
                display: inline-block;
                position: fixed;
                bottom: 15px;
                width: 50%;
            }

            .pagination a {
                color: black;
                float: left;
                padding: 8px 16px;
                text-decoration: none;
                transition: background-color .3s;
            }

            .pagination a.active {
                background-color: #4C55AF;
                color: white;
                border: 1px solid #4C55AF;
                pointer-events: none;
            }

            .pagination a:hover:not(.active) {background-color: #ddd;}

            .disabled {
                pointer-events: none;
            }
            </style>
            </head>
            <body>
            """

        if i<= 5:
            html += """
                <div class="center">
                  <div class="pagination">
                    <a href="/%s/&page=1" class="disabled">&laquo;</a>
                    <a href="/%s/&page=1" class="active" class="disabled">1</a>
                    <a href="/%s/&page=1" class="active" class="disabled">&raquo;</a>
                  </div>
                </div>

                </body>
                </html>
            """ %(text1,text1,text1)

        elif i > 5 and i <= 10:
            html += """
                <div class="center">
                  <div class="pagination">
                    <a href="/%s/&page=1" class="disabled">&laquo;</a>
                    <a href="/%s/&page=1" class="active" class="disabled">1</a>
                    <a href="/%s/&page=2">2</a>
                    <a href="/%s/&page=2">&raquo;</a>
                  </div>
                </div>

                </body>
                </html>
            """ %(text1,text1,text1,text1)


        elif i > 10 and i <= 15:
            html += """
                <div class="center">
                  <div class="pagination">
                    <a href="/%s/&page=1" class="disabled">&laquo;</a>
                    <a href="/%s/&page=1" class="active" class="disabled">1</a>
                    <a href="/%s/&page=2">2</a>
                    <a href="/%s/&page=3">3</a>
                    <a href="/%s/&page=3">&raquo;</a>
                  </div>
                </div>

                </body>
                </html>
            """ %(text1,text1,text1,text1,text1)

        elif i > 15 and i <= 20:
            html += """
                <div class="center">
                  <div class="pagination">
                    <a href="/%s/&page=1" class="disabled">&laquo;</a>
                    <a href="/%s/&page=1" class="active" class="disabled">1</a>
                    <a href="/%s/&page=2">2</a>
                    <a href="/%s/&page=3">3</a>
                    <a href="/%s/&page=4">4</a>
                    <a href="/%s/&page=4">&raquo;</a>
                  </div>
                </div>

                </body>
                </html>
            """ %(text1,text1,text1,text1,text1,text1)

        elif i > 20 and i <= 25:
            html += """
                <div class="center">
                  <div class="pagination">
                    <a href="/%s/&page=1" class="disabled">&laquo;</a>
                    <a href="/%s/&page=1" class="active" class="disabled">1</a>
                    <a href="/%s/&page=2">2</a>
                    <a href="/%s/&page=3">3</a>
                    <a href="/%s/&page=4">4</a>
                    <a href="/%s/&page=5">5</a>
                    <a href="/%s/&page=5">&raquo;</a>
                  </div>
                </div>

                </body>
                </html>
            """ %(text1,text1,text1,text1,text1,text1,text1)

    return (html)

@route('/<keywords>/&page=1', method = "GET")

def page1(keywords):

    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website page:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
""" 

    text = request.query.keywords
    global backup
    global i
    global url_id
    backup += text + " "

    global text1
    textstr = str(text)
    text = textstr.lower().split() #get all lower case and split individually

    check = "" #duplicate word checker for the original text
    checker = "" #duplicate word checker for the history
    sorter = "" #for the sorting of the history
    
    history = backup
    
    for words in text:
        if words not in check:
            html += """
            <tr> 
                <td>%s</td>
                <td>%s</td>
            </tr>
            """ % (words, str(text.count(words)))
            check += words
    html += "</table>"  #close results table
   
    html += """
    <html>
    <head>
    <style>
    .box{
        display: none;
        width: 100%;
    }
    a:hover + .box,.box.hover{
        display:block;
        position: relative;
        z-index: 100;
    }
    td {
        padding:50px;
    }
    </style>
    </head>
    </html>

    <table align="center" id='URLS'>
    <caption style="text-align:center;">
    <b>Search Results</b></caption>
    """

    checkme = 0
    for numbers in url_id:
        html += """
        <tr>
            <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
            <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
            </div></td>

        </tr>
        """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
        checkme += 1
        if checkme >= 5:
            break
    html += """
        </table>
        """
    
    html += """
        <html>
        <head>
        <style>
        .center {
            text-align:center;
        }

        .pagination {
            display: inline-block;
            position: fixed;
            bottom: 15px;
            width: 50%;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4C55AF;
            color: white;
            border: 1px solid #4C55AF;
            pointer-events: none;
        }

        .pagination a:hover:not(.active) {background-color: #ddd;}

        .disabled {
            pointer-events: none;
        }
        </style>
        </head>
        <body>
        """

    if i<= 5:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1" class="disabled">&laquo;</a>
                <a href="/%s/&page=1" class="active" class="disabled">1</a>
                <a href="/%s/&page=1" class="active" class="disabled">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1)

    elif i > 5 and i <= 10:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1" class="disabled">&laquo;</a>
                <a href="/%s/&page=1" class="active" class="disabled">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=2">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1)


    elif i > 10 and i <= 15:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1" class="disabled">&laquo;</a>
                <a href="/%s/&page=1" class="active" class="disabled">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=3">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1)

    elif i > 15 and i <= 20:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1" class="disabled">&laquo;</a>
                <a href="/%s/&page=1" class="active" class="disabled">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=4">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1)

    elif i > 20 and i <= 25:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1" class="disabled">&laquo;</a>
                <a href="/%s/&page=1" class="active" class="disabled">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=5">5</a>
                <a href="/%s/&page=5">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1,text1)

    return (html)

@route('/<keywords>/&page=2', method = "GET")

def page2(keywords):

    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website page:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
"""

    text = request.query.keywords
    global backup
    global i
    backup += text + " "
    global text1
    textstr = str(text)
    text = textstr.lower().split() #get all lower case and split individually

    check = "" #duplicate word checker for the original text
    checker = "" #duplicate word checker for the history
    sorter = "" #for the sorting of the history
    
    history = backup
    
    
    html += """
    <html>
    <head>
    <style>
    .box{
        display: none;
        width: 100%;
    }
    a:hover + .box,.box.hover{
        display:block;
        position: relative;
        z-index: 100;
    }
    td {
        padding:50px;
    }
    </style>
    </head>
    </html>

    <table align="center" id='URLS'>
    <caption style="text-align:center;">
    <b>Search Results</b></caption>
    """


    checkCount = 1
    checkme = 0
    for numbers in url_id:
        if checkCount<= 5:
            checkCount += 1
        elif checkCount > 5 and checkCount <=10:
            html += """
            <tr>
                <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
                <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
                </div></td>

            </tr>
            """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
            checkme += 1
            if checkme >= 5:
                break
    html += """

    </table>
    """
    
    html += """
        <html>
        <head>
        <style>
        .center {
            text-align:center;
        }

        .pagination {
            display: inline-block;
            position: fixed;
            bottom: 15px;
            width: 50%;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4C55AF;
            color: white;
            border: 1px solid #4C55AF;
            pointer-events: none;
        }

        .pagination a:hover:not(.active) {background-color: #ddd;}

        .disabled {
            pointer-events: none;
        }
        </style>
        </head>
        <body>
        """

    if i<= 5:
        html += ""

    elif i > 5 and i <= 10:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1"1</a>
                <a href="/%s/&page=2" class="active" class="disabled">>2</a>
                <a href="/%s/&page=2" class="disabled">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1)


    elif i > 10 and i <= 15:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2" class="active" class="disabled">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=3">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1)

    elif i > 15 and i <= 20:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2" class="active" class="disabled">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=4">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1)

    elif i > 20 and i <= 25:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2" class="active" class="disabled">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=5">5</a>
                <a href="/%s/&page=5">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1,text1)


    return (html)

@route('/<keywords>/&page=3', method = "GET")

def page3(keywords):

    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website page:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
"""

    text = request.query.keywords
    global backup
    global i
    backup += text + " "
    global text1
    textstr = str(text)
    text = textstr.lower().split() #get all lower case and split individually

    check = "" #duplicate word checker for the original text
    checker = "" #duplicate word checker for the history
    sorter = "" #for the sorting of the history
    
    history = backup
    

    html += """
    <html>
    <head>
    <style>
    .box{
        display: none;
        width: 100%;
    }
    a:hover + .box,.box.hover{
        display:block;
        position: relative;
        z-index: 100;
    }
    td {
        padding:50px;
    }
    </style>
    </head>
    </html>

    <table align="center" id='URLS'>
    <caption style="text-align:center;">
    <b>Search Results</b></caption>
    """


    checkCount = 1
    checkme = 0
    for numbers in url_id:
        if checkCount<= 10:
            checkCount += 1
        elif checkCount > 10 and checkCount <=15:
            html += """
            <tr>
                <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
                <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
                </div></td>

            </tr>
            """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
            checkme += 1
            if checkme >= 5:
                break
    html += """

    </table>
    """

    html += """
        <html>
        <head>
        <style>
        .center {
            text-align:center;
        }

        .pagination {
            display: inline-block;
            position: fixed;
            bottom: 15px;
            width: 50%;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4C55AF;
            color: white;
            border: 1px solid #4C55AF;
            pointer-events: none;
        }

        .pagination a:hover:not(.active) {background-color: #ddd;}

        .disabled {
            pointer-events: none;
        }

        </style>
        </head>
        <body>
        """

    if i<= 5:
        html += ""

    elif i > 5 and i <= 10:
        html += ""

    elif i > 10 and i <= 15:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3" class="active" class="disabled">3</a>
                <a href="/%s/&page=3" class="disabled">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1)

    elif i > 15 and i <= 20:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3" class="active" class="disabled">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=4">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1)

    elif i > 20 and i <= 25:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3" class="active" class="disabled">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=5">5</a>
                <a href="/%s/&page=5">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1,text1)

    return (html)

@route('/<keywords>/&page=4', method = "GET")

def page4(keywords):

    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website page:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
"""

    text = request.query.keywords
    global backup
    global i
    backup += text + " "
    global text1
    textstr = str(text)
    text = textstr.lower().split() #get all lower case and split individually

    check = "" #duplicate word checker for the original text
    checker = "" #duplicate word checker for the history
    sorter = "" #for the sorting of the history
    
    history = backup
    

    html += """
    <html>
    <head>
    <style>
    .box{
        display: none;
        width: 100%;
    }
    a:hover + .box,.box.hover{
        display:block;
        position: relative;
        z-index: 100;
    }
    td {
        padding:50px;
    }
    </style>
    </head>
    </html>

    <table align="center" id='URLS'>
    <caption style="text-align:center;">
    <b>Search Results</b></caption>
    """


    checkCount = 1
    checkme = 0
    for numbers in url_id:
        if checkCount<= 15:
            checkCount += 1
        elif checkCount > 15 and checkCount <=20:
            html += """
            <tr>
                <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
                <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
                </div></td>

            </tr>
            """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
            checkme += 1
            if checkme >= 5:
                break
    html += """

    </table>
    """
    
    html += """
        <html>
        <head>
        <style>
        .center {
            text-align:center;
        }

        .pagination {
            display: inline-block;
            position: fixed;
            bottom: 15px;
            width: 50%;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4C55AF;
            color: white;
            border: 1px solid #4C55AF;
            pointer-events: none;
        }

        .pagination a:hover:not(.active) {background-color: #ddd;}

        .disabled {
            pointer-events: none;
        }

        </style>
        </head>
        <body>
        """

    if i<= 5:
        html += ""

    elif i > 5 and i <= 10:
        html += ""

    elif i > 10 and i <= 15:
        html += ""

    elif i > 15 and i <= 20:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4" class="active" class="disabled">4</a>
                <a href="/%s/&page=4" class="active" class="disabled">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1)

    elif i > 20 and i <= 25:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4" class="active" class="disabled">4</a>
                <a href="/%s/&page=5">5</a>
                <a href="/%s/&page=5">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1,text1)

    return (html)

@route('/<keywords>/&page=5', method = "GET")

def page5(keywords):

    html = """
    <style>
    body
    {background-color:lightblue;} 
    </style>
    <form action="/s" method="get" style="text-align:center;" autocomplete="off">
    Enter keywords to search the Website page:
    <input name="keywords" type="text" />
    <input type="submit" spellcheck="true" value="Search" /></form>
"""

    text = request.query.keywords
    global backup
    global i
    backup += text + " "
    global text1
    textstr = str(text)
    text = textstr.lower().split() #get all lower case and split individually

    check = "" #duplicate word checker for the original text
    checker = "" #duplicate word checker for the history
    sorter = "" #for the sorting of the history
    
    history = backup
    

    html += """
    <html>
    <head>
    <style>
    .box{
        display: none;
        width: 100%;
    }
    a:hover + .box,.box.hover{
        display:block;
        position: relative;
        z-index: 100;
    }
    td {
        padding:50px;
    }
    </style>
    </head>
    </html>

    <table align="center" id='URLS'>
    <caption style="text-align:center;">
    <b>Search Results</b></caption>
    """


    checkCount = 1
    checkme = 0
    for numbers in url_id:
        if checkCount<= 20:
            checkCount += 1
        elif checkCount > 20 and checkCount <=25:
            html += """
            <tr>
                <td align="center"><a href="%s"><b><p style="font-size:30px">%s</p></b></a><div class="box">
                <iframe src="%s" width = "750px" height = "450px" scrolling="yes"></iframe>
                </div></td>

            </tr>
            """ %(hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers),hi.get('doc_id_'+numbers))
            checkme += 1
            if checkme >= 5:
                break
    html += """

    </table>
    """
    
    html += """
        <html>
        <head>
        <style>
        .center {
            text-align:center;
        }

        .pagination {
            display: inline-block;
            position: fixed;
            bottom: 15px;
            width: 50%;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4C55AF;
            color: white;
            border: 1px solid #4C55AF;
            pointer-events: none;
        }

        .pagination a:hover:not(.active) {background-color: #ddd;}

        .disabled {
            pointer-events: none;
        }

        </style>
        </head>
        <body>
        """

    if i<= 5:
        html += ""

    elif i > 5 and i <= 10:
        html += ""

    elif i > 10 and i <= 15:
        html += ""

    elif i > 15 and i <= 20:
        html += ""

    elif i > 20 and i <= 25:
        html += """
            <div class="center">
              <div class="pagination">
                <a href="/%s/&page=1">&laquo;</a>
                <a href="/%s/&page=1">1</a>
                <a href="/%s/&page=2">2</a>
                <a href="/%s/&page=3">3</a>
                <a href="/%s/&page=4">4</a>
                <a href="/%s/&page=5" class="active" class="disabled">5</a>
                <a href="/%s/&page=5" class="disabled">&raquo;</a>
              </div>
            </div>

            </body>
            </html>
        """ %(text1,text1,text1,text1,text1,text1,text1)

    return (html)
        
run(host='localhost', port=8080, debug=True)

