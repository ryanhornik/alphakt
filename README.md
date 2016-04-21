#Alpha Karma Train

    install python3
    virtualenv -p python3 venv

Add the lines

    export REDDIT_SECRET=XXX
    export REDDIT_CLIENT_ID=XXX
    export ACCESS_TOKEN=XXX
    export REFRESH_TOKEN=XXX


to the end of venv/bin/activate

Add the lines

    unset REDDIT_SECRET
    unset REDDIT_CLIENT_ID

to the bottom of the deactivate function in venv/bin/activate

Start the virtual environment with

    source venv/bin/activate
    
Ensure your dependencies are up to date

    pip install -r requirements.txt
    

run as

    ./candidate_identification.py
