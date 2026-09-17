def normalize_data(n_cases, n_people, scale):
    norm_cases = []
    for idx, n in enumerate(n_cases):
        # divide new cases by population to get the ratio, multiply by scale
        norm_cases.append(scale * (n / n_people[idx]))
    return norm_cases

regions  = ['Seoul', 'Gyeongi', 'Busan', 'Gyeongnam', 'Incheon', 'Gyeongbuk', 'Daegu', 'Chungnam', 'Jeonnam', 'Jeonbuk', 'Chungbuk', 'Gangwon', 'Daejeon', 'Gwangju', 'Ulsan', 'Jeju', 'Sejong']
n_people = [9550227,  13530519, 3359527,     3322373,   2938429,     2630254, 2393626,    2118183,   1838353,   1792476,    1597179,   1536270,   1454679,   1441970, 1124459, 675883,   365309] # 2021-08
n_covid  = [    644,       529,      38,          29,       148,          28,      41,         62,        23,        27,         27,        33,        16,        40,      20,      5,        4] # 2021-09-21

sum_people = sum(n_people)
sum_covid  = sum(n_covid)
norm_covid = normalize_data(n_covid, n_people, 1000000) # The new cases per 1 million people

def write_line(f, content):
    f.write(content + "\n")

with open("covid19_statistics.md", "w", encoding="utf-8") as f:
    # Print population by region
    write_line(f, '### Korean Population by Region')
    write_line(f, '* Total population: %d' % sum_people)
    write_line(f, "") # Print an empty line
    write_line(f, '| Region | Population | Ratio (%) |')
    write_line(f, '| ------ | ---------- | --------- |')
    for idx, pop in enumerate(n_people):
        ratio = 100 / sum_people * pop
        write_line(f, '| %s | %d | %.1f |' % (regions[idx], pop, ratio))
    write_line(f, "")

    write_line(f, '### Korean VOCID-19 New Cases by Region')
    write_line(f, '* Total new cases: %d' % sum_covid)
    write_line(f, "")
    write_line(f, '| Region | New Cases | Ratio (%) | New Cases / 1M |')
    write_line(f, '| ------ | ---------- | --------- | --------- |')
    for idx, covid_pop in enumerate(n_covid):
        ratio = 100 / sum_covid * covid_pop
        write_line(f, '| %s | %d | %.1f | %.1f |' % (regions[idx], covid_pop, ratio, norm_covid[idx]))
    write_line(f, "")