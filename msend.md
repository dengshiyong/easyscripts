# Introduction #

msend,

在命令行上通过gmail服务发送邮件的脚本。支持主题，附件等。<br>
注意：需要libgmail支持。<br>
<br>
<br>
<blockquote>Usage:<br>
<blockquote>msend -t user@domain.com -s title<br>
msend -t user@domain.com {-s title | -f file | -z file}</blockquote></blockquote>

<blockquote>Full command:<br>
<blockquote>msend --to=user@domain.com --subject=title [--msg=body] [--files="file1;dir2"] [--zip="file1;dir2"]</blockquote></blockquote>

<blockquote>Example: ( Edit ~/.msend for default sender account )<br>
<blockquote>msend -t user@domain.com -s "just a test"<br>
msend -t user@domain.com -s "send all pic" -f ./mypics/<br>
msend -t user@domain.com -s "send files as zip" -z ./mytext/<br>
msend -t user@domain.com -s "send both" -f mytext -z mytext</blockquote></blockquote>



<h1>Details</h1>

Add your content here.  Format your content with:<br>
<ul><li>Text in <b>bold</b> or <i>italic</i>
</li><li>Headings, paragraphs, and lists<br>
</li><li>Automatic links to other wiki pages