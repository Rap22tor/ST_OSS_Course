def read_data(filename):
    f = open(filename)
    data = []
    for line in f.readlines():
        try:
            values = [int(word) for word in line.split(',')]
            data.append(values)
        except ValueError as ex:
            # We expect this error for the header
            print(f'A line is ignored. (message: {ex})’)')
    return data

def calc_weighted_average(data_2d, weight):
    average = []
    for data in data_2d:
        average.append((weight[0] * data[0]) + (weight[1] * data[1]))
    return average

def analyze_data(data_1d):
    mean = sum(data_1d) / len(data_1d)

    squared_diffs = []
    for data in data_1d:
        squared_diffs.append(pow(mean - data, 2))

    var = sum(squared_diffs) / len(data_1d)
    data_1d.sort()
    median = data_1d[len(data_1d)//2]
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')