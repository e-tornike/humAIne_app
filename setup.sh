mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
wget -O cc.en.25.bin https://www.dropbox.com/s/d7b4f6gn3zae1ie/cc.en.25.bin?dl=0