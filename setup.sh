mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml
wget -O w2b_bitlevel2_size400_vocab400K.tar.gz https://www.dropbox.com/s/aj05qcqjucu5c7j/w2b_bitlevel2_size400_vocab400K.tar.gz?dl=0
tar -xf w2b_bitlevel2_size400_vocab400K.tar.gz