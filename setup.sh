mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
wget -O cc.en.10.bin https://www.dropbox.com/s/m7t27m73qqcl2my/w2v.100k.txt?dl=0
