#!/usr/bin/env python3
import subprocess, re, urllib, html2text
args = "netcat workshop.dciets.com 8111".split(" ")
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def find_all(s, match):
    indices = []
    start = 0

    if len(match) == 0:
        return indices

    while True:
        index = s.find(match)
        if index != -1:
            indices.append(index + start)
            start += index + len(match)
            s = s[start:]
        else:
            break

    return indices

while True:
    line = proc.stdout.readline().decode("ascii").strip()
    if line != '':
        print(line)

        match = re.match("What is the birth year of ([a-zA-z '.\\-]+) ?", line)

        if match is not None:
            name = match.group(1).strip()
            print(name)

            try:
                html = str(urllib.request.urlopen("http://en.wikipedia.org/wiki/" + name.replace(" ", "_")).read())
            except:
                print("The wikipedia entry for %s could not be found" % name)
                continue

            text = html2text.html2text(html).lower()
            years = [year[1:5] for year in re.findall(r"\D\d{4}\D", text) if int(year[1:5]) < 2000]
            years = list(set(years))
            years.sort()

            born_position = text.find("born")

            if born_position != -1:
                proximity_text = "born"
                closest_difference = None
                closest_year = None

                print(born_position)

                for year in years:
                    indices = find_all(text, str(year))
                    print(year, indices)
                    for index in indices:
                        difference = index - born_position

                        if difference > 0 and (closest_difference is None or difference < closest_difference):
                            closest_difference = difference
                            closest_year = year

                if closest_year is not None:
                    result = "%s was born in %s" % (name, closest_year)
                else:
                    result = "%s's birth year could not be found" % name

                #proc.communicate(result.encode("ascii"))

        elif line != "Wrong" and line != "Timeout":
            pass
        else:
            pass
    else:
        break
