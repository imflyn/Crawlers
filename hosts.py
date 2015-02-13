import urllib.request, shutil, platform, time
import codecs

url = 'http://freedom.txthinking.com/hosts'

platform = platform.uname()[0]
if platform == 'Windows':
    file = r'c:\windows\system32\drivers\etc\hosts'
elif platform == 'Linux':
    file = r'/etc/hosts'
data = urllib.request.urlopen(url, None, 10).read()
data = str(data).replace('<br />', '').replace('&nbsp;', '').replace('<span>', '')
if data is not None:
    # back hosts
    shutil.copyfile(file, '%s.bak-%s' % (file, time.strftime('%Y%m%d%H%M%S')))
    # write hosts
    fp = codecs.open(file, 'w', encoding='utf-8')
    fp.write(data)
    fp.close()
    print
    'ok'
else:
    print
    'url not found'