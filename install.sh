wget  https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_118.0.5993.70-1_amd64.deb
sudo dpkg -i google-chrome-stable*
sudo apt-get install -f
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo apt-get install tree
tree chromedriver*
python -m pip install --upgrade pip
pip install -r requirements.txt
	
