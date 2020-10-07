mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
mkdir -p ~/models/
aria2c -x16 https://drive.google.com/uc?id=1GG1xCzZpoys-cRMyKCtwDaqyY2WQaCCl -d ~/models
gunzip ~/models/cc.en.25.bin.gz ~/models/