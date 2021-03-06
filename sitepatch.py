import os
import re
import glob
import argparse

types = ('*.html', '*.htm') 

class NotionSitePatch:
  def __init__(self, args):
    self.gtagline = f'''<!-- Global site tag (gtag.js) - Google Analytics -->
      <script async src="https://www.googletagmanager.com/gtag/js?id={args.gtag}"></script>
      <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag("js", new Date());
      gtag("config", "{args.gtag}");
      </script>\n'''
    self.favline = f'''<link rel="icon" type="image/png" href="{args.favpath}"/>\n'''
    self.sitedir = args.sitedir

  def getSiteName(self):
    with open(os.path.join(self.sitedir,'index.html'),'r') as f:
      _indexfile = f.read()
    _sitetitle = re.compile('<title>(.*?)</title>').search(_indexfile)
    return _sitetitle.group(1)

  def applyPatch(self):
    paths = []
    for fType in types:
      for filename in glob.iglob(os.path.join(self.sitedir,'**/' + fType), recursive=True):
          paths.append(filename)
    _sitename = self.getSiteName()
    for path in paths:
        with open(path,'r') as f:
            lines = f.readlines()
        with open(path, 'w') as w:
            for i in range(0,len(lines)):
                if f"{_sitename} 2019" in lines[i]:
                    lines[i] = lines[i].replace(f"<div>&copy; {_sitename} 2019</div>", f"<div>&copy; {_sitename} 2021</div>")
                if ".html" in lines[i]:
                    lines[i] = lines[i].replace(".html", "")
                if ("href=" in lines[i]) and ("Navbar__Btn" not in lines[i+1]) and ('index.html' not in path):
                    lines[i] = lines[i].replace('href=', 'target="_blank" href=')
                w.write(lines[i])
                if "<head>" in lines[i]:
                    if "<!-- Global site tag (gtag.js) - Google Analytics -->" not in lines[i+1]:
                        w.write(self.gtagline)
                if "<title>" in lines[i]:
                    if self.favline not in lines[i+1]:
                        w.write(self.favline)

if __name__ == "__main__":
  parser = argparse.ArgumentParser("NotionSitePatchWork")
  parser.add_argument("--gtag", default="G-5F9Y9HC95G", help="Google analytics tag.", type=str)
  parser.add_argument("--favpath", default="./favicon.png", help="Site favicon path.", type=str)
  parser.add_argument("--sitedir", default="./public", help="Public directory path generated by Notablog", type=str)
  args = parser.parse_args()
  notionpatch = NotionSitePatch(args)
  notionpatch.applyPatch()