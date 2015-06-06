# Reptile
要求：
编写一个页面抓取程序，抓取给定网站的页面。保存网站的url列表
并将抓到的每个页面单独存成文件。

说明：
使用gevent或者多线程能够设定参数，如深度、最大页面数等，记录
必要的日志
页面存成文件后，给定原来的url能够迅速找到对应的文件


使用说明：
目前只支持命令行操作
命令行参数说明：
reptile.py { -u http://url [ -t timeout ] [ -n maxnum ] [ -d maxdepth ] | -l } |  [ -p storysite ] 

Options:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout=TIMEOUT
                        Specify connection time limit
  -u URL, --url=URL     Specify the target URL
  -n MAXNUM, --number=MAXNUM
                        Specify the max numbers of target pages
  -d DEPTH, --depth=DEPTH
                        Specify the max depth of target pages
  -p PATH, --path=PATH  Specify the pathsite to store pages
  -l, --list            list every url mapping to which file.

-t: 如不指定默认超时时间为10秒
-n: 如不指定默认抓取页面最大个数为100个
-d：如不指定默认抓取页面最大深度为2

-d 和 -n 同时指定是抓取只要满足最大页面数或者最大个数就停止抓取

-l：显示url与抓取文件的对应关系 指定-u参数时，显示指定的url对应的文件，不指定为显示所有的

-p: 指定抓页面存放目录，未实现改功能，目前存放目录为~/reptile

文件映射说明：
~/reptile/objs
存放抓取的页面信息，文件保存采用将url 使用sha1计算40 hash值，前两位作为目录，后38位为文件名

~/reptile/objs/index
记录抓取的url与文件对应关系格式为
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx http://url

~/reptile/log/errorlog
记录抓取过程中，连接超时或者页面错误，的url


