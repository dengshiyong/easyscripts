在控制台使用 cd 命令时，用拼音自动补全中文路径

实验目录如下：

biff@lenovo:/domain/WorkSpace$ ls
SVN培训  全球眼  浙江建行  浙江农信

使用: (输完后按 TAB 键自动补全)
> cd S     press tab             进入[SVN培训] <br>
<blockquote>cd q     press tab             进入[全球眼]<br>
cd z     press tab             自动补全[浙江]<br>
cd zj     press tab        提示[浙江建行 浙江农信]备选br><br>
cd 浙江j press tab             进入[浙江建行]<br>
cd zjj   press tab             进入[浙江建行]<br>
cd zj1   press tab             进入[浙江建行]<br>
cd zj2   press tab             进入[浙江农信] <br></blockquote>

下载软件包，解压，参考 install.sh 进行安装。