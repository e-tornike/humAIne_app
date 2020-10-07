mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
mkdir -p ~/models/
wget ./models/cc.en.25.bin.gz https://www.dropbox.com/s/06zx30696rdllg2/cc.en.25.bin.gz?dl=0