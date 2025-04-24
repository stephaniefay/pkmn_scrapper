@echo off
setlocal EnableDelayedExpansion
REM activate Python venv
CALL python -m scrapy crawl index_spider
CALL python -m scrapy crawl edition_spider
cd %~dp0
for %%f in ("%CD%\extracted\*.csv") do (
    if "%%~xf"==".csv" (
        set "filepath=%%~ff"
        set "filepath=!filepath:\=/!"
        REM echo Path gerado: !filepath!
        CALL python -m scrapy crawl download_images -a file_name="!filepath!"
        REM pause
    )
)

CALL python -m scrapy crawl download_images -a file_name=C:\Users\<your_user_and_path>\pkmn_scrapper\pkmn_scrapper\extracted\index\editions.csv
