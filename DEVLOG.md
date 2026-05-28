traffic-predictor/  — root
    app/    — helps organize the project
        main.py
        models.py   — helps structure the database (Object Relational Mapper)
        database.py — creates the PostgreSQL connection
        scheduler.py    — recollects the data
        services/ — separation of concerns: grouped bcs they are doing the same thing: calling APIs
            maps.py — calls MAPS
            weather.py — calls WEATHER
            holidays.py — calls HOLIDAY
    static/
        index.html — sets the frontend
    config.yaml — sets a base structure, without hardcoding somewhere else, to be used (like a sample)
    .env    — used if there's sensitive information that shouldn't be uploaded (it never does)
    .gitignore  — tells git to ignore the files outlined inside
    requirements.txt    — all the libraries used, if called in the terminal it installs them all