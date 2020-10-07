mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
mkdir -p ~/models/
gdown https://drive.google.com/uc?id=1GG1xCzZpoys-cRMyKCtwDaqyY2WQaCCl ~/models/
