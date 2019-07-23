import io
import sys
import difflib

class CodeDiff():
    def __init__(self, fromfile, tofile, fromtxt=None, totxt=None, name=None):
        self.filename = name
        self.fromfile = fromfile
        if fromtxt == None:
            try:
                with io.open(fromfile,encoding='utf-8') as f:
                    self.fromlines = f.readlines()
            except Exception as e:
                print("Problem reading file %s" % fromfile)
                print(e)
                sys.exit(1)
        else:
            self.fromlines = [n + "\n" for n in fromtxt.split("\n")]
        self.leftcode = "".join(self.fromlines)

        self.tofile = tofile
        if totxt == None:
            try:
                with io.open(tofile,encoding='utf-8') as f:
                    self.tolines = f.readlines()
            except Exception as e:
                print("Problem reading file %s" % tofile)
                print(e)
                sys.exit(1)
        else:
            self.tolines = [n + "\n" for n in totxt.split("\n")]
        self.rightcode = "".join(self.tolines)

    def getDiffDetails(self, fromdesc='', todesc='', context=False, numlines=5, tabSize=1):
        # change tabs to spaces before it gets more difficult after we insert
        # markkup
        def expand_tabs(line):
            # hide real spaces
            line = line.replace(' ', '\0')
            # expand tabs into spaces
            line = line.expandtabs(tabSize)
            # replace spaces from expanded tabs back into tab characters
            # (we'll replace them with markup after we do differencing)
            line = line.replace(' ', '\t')
            return line.replace('\0', ' ').rstrip('\n')

        self.fromlines = [expand_tabs(line) for line in self.fromlines]
        self.tolines = [expand_tabs(line) for line in self.tolines]

        # create diffs iterator which generates side by side from/to data
        if context:
            context_lines = numlines
        else:
            context_lines = None

        diffs = difflib._mdiff(self.fromlines, self.tolines, context_lines,
                               linejunk=None, charjunk=difflib.IS_CHARACTER_JUNK)
        return list(diffs)
        
    def getOneHtml(self,left=True):
        DiffDetails = self.getDiffDetails()
        for ele in DiffDetails:
            #print(ele)
            if left:
                my   = ele[0]
                other  = ele[1]
            else:
                my   = ele[1]
                other  = ele[0]
            isDiff = ele[2]
            if isDiff:
                if isinstance(my[0],int) and isinstance(other[0],int):
                    classname = "codeChange"
                elif isinstance(my[0],int):
                    classname = "codeAdd"
                else:
                    classname = "codeDelete"
                code = my[1]
                for s in ['\x01','\x00+','\x00-','\x00^','\x00']:
                    code = code.replace(s,'')
                yield "<tr><td class=\"lineNumber\">%02s</td><td class=\"%s\">%s</td></tr>"%(my[0],classname,code)
            else:
                yield "<tr><td class=\"lineNumber\">%02s</td><td>%s\n</td></tr>"%(my[0],my[1])
    
    def getOneDiff(self,left=True):
        DiffDetails = self.getDiffDetails()
        for ele in DiffDetails:
            #print(ele)
            if left:
                my   = ele[0]
                other  = ele[1]
            else:
                my   = ele[1]
                other  = ele[0]
            isDiff = ele[2]
            if isDiff:
                if isinstance(my[0],int) and isinstance(other[0],int):
                    classname = "codeChange"
                elif isinstance(my[0],int):
                    classname = "codeAdd"
                else:
                    classname = "codeDelete"
                code = my[1]
                for s in ['\x01','\x00+','\x00-','\x00^','\x00']:
                    code = code.replace(s,'')
                yield {'lineNumber':my[0],'classname':classname,'code':code}
            else:
                yield {'lineNumber':my[0],'classname':'','code':my[1]}
    
    def getHtml(self,path='index.html'):
        html='''<!doctype html>
                    <html>
                    <head>
                        <title>Test highlight js</title>
                        <meta charset=utf8>
                        <link href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/default.min.css" rel="stylesheet" />
                        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
                        <style type="text/css">
                        .codeAdd{
                            background-color:lightgreen;
                        }
                        .codeChange{
                            background-color:#FFE5B5;
                        }
                        .codeDelete{
                            background-color:pink;
                        }
                        .codeArea{
                            height:100%;
                        }
                        .lineNumber>span{
                            color:gray;
                            !important
                        }
                        </style>
                    </head>
                    <body>
                        <table width="100%">
                            <tr>
                                <td><pre><code class="python"><table class="codeArea" width="100%">'''
        for ele in self.getOneHtml():
            html+=ele
        html+='''               </table class="codeArea">
                                </code></pre></td>
                                <td><pre><code class="python"><table width="100%">'''
        for ele in self.getOneHtml(left=False):
            html+=ele
        html+='''               </table>
                                </code></pre></td>
                            </tr>
                        </table>
                    <!-- init highlight.js -->
                    <script>hljs.initHighlightingOnLoad();</script>
                    </body>
                    </html>'''
        with open(path,mode='w',encoding='utf8') as f:
            f.write(html)

def main(file1, file2):
    codeDiff = CodeDiff(file1, file2, name=file2)
    for idx,ele in enumerate(codeDiff.getDiffDetails()):
        print(idx,ele)

if __name__ == "__main__":
    file1 = "2.py"
    file2 = "3.py"
    codeDiff = CodeDiff(file1, file2)
    for idx,ele in enumerate(codeDiff.getOneHtml()):
        print(idx,ele)
    for idx,ele in enumerate(codeDiff.getOneHtml(False)):
        print(idx,ele)
    codeDiff.getHtml('test.html')