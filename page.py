from frontpy.frontpy import *

#This block is used to create one theme for all pages
backgroundColor = "#dddddd"
brandColor = "red" 
brandText = Text()
brandText.color = brandColor
pageParams = tuple(["utf-8",{"background":backgroundColor}])
menu = InlineMenu({"background":"black"},{"Home":"/", "Objectives":"/objectives","User guide":"/userGuide","Tester guide":"/testerGuide","Developer guide":"/developerGuide"},"white",BrandText("Front-py",brandColor))
foot = Text("&copy DimonLuk")
foot.position = "center"
foot.color = "white"
footer = Footer(foot)
footer.backgroundColor = "black"

@serve("/")
def index(request):
    if request.method == "GET":
        articles = RowArticles("Three facts about %s 0.0.1(pre-alpha)" % brandText("Front-py"),horizontalLine=True,headersLevel=2,horizontalDistance="50px")
        articles.addArticle("The first fact","This framework is attemp to combine the best ideas from Django, Flask, Angular and other frameworks but %s complicated application architecture" % brandText("without creating"))
        articles.addArticle("The second fact","You have to use only %s 3.x to write %s front and back-end" % (brandText("python"),brandText("both")))
        articles.addArticle("The third fact","Just compare:%s" % ContainerRow(Image("test.png","Code",50),Image("test.png","Code",50)))
    
        page = Page("Home",*pageParams)
        page.addElement(menu.addLinks({"Additional Link":"/nothing"},brandColor),articles,footer)
        return page









@serve("/objectives")
def objectives(request):
    articles = Article(headersLevel=2)
    
    frontEnd = articles("Front-end",NumberedList({},"A lot of tests","Custom Forms","Reorgonaising folders"))
    backEnd = articles("Back-end",NumberedList({},"Task","Simple","Test"))
    experience = articles("User experience",NumberedList({"background":"red"},"SimpleTask"))
    
    articleSection = ColumnArticles("%s pre-alpha objectives" % brandText("Front-py"),"",1,"center","50px",True,frontEnd,backEnd,experience)

    page = Page("Objectives",*pageParams)
    page.addElement(menu,articleSection,footer)
    return page

@serve("/userGuide")
def userGuide(request):
    page = Page("User Guide",*pageParams)
    page.addElement(menu,footer)
    return page
@serve("/testerGuide")
def testerGuide(request):
    page = Page("Tester Guide",*pageParams)
    page.addElement(menu,footer)
    return page

@serve("/developerGuide")
def testerGuide(request):
    page = Page("Developer Guide",*pageParams)
    page.addElement(menu,footer)
    return page

@serve("/<any>")
def anypage(request):
    page = Page("%s" % request.path[1:],*pageParams)
    page.addElement(menu,Text("ANY"),footer)
    return page

runApp()
