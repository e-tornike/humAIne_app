mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
wget -O cc.en.10.bin https://www.dropbox.com/s/yfnef36kp5d14l1/cc.en.10.bin?dl=0