
mkdir -p $HOME/bin
cp chsdir chs_completion $HOME/bin/ && \
echo '[ -f $HOME/bin/chs_completion ] && . $HOME/bin/chs_completion' >> $HOME/.bashrc

echo "Close and open new terminal."
