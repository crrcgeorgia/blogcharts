import os

targets = [
    "cad-democracy",
    "church-scandal",
    "covid-democracy",
    "open-economy",
    "rally-flag",
    "approve-business",
]

for t in targets:
    for lang in ["en", "ka", "ru"]:
        try:
            charts = [i for i in os.listdir(f"{t}/{lang}") if ".html" in i]
        except:
            continue
        if len(charts) > 0:
            for c in charts:
                with open("lazee_output.txt", "a") as f:
                    ghubpath = (
                        f"https://crrcgeorgia.github.io/blogcharts/{t}/{lang}/{c}\n"
                    )
                    f.write(ghubpath)
