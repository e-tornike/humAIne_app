mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
mkdir -p ~/models/
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz /models/