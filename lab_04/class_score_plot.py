import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Prepare Midterm and Finals data, same for Korean and English students
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm_kr + 60/100*final_kr for (midterm_kr, final_kr) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm_en + 60/100*final_en for (midterm_en, final_en) in class_en]

    # Plot midterm/final scores as scatter plots
    plt.xlim(0, 125)
    plt.xlabel('Midterm scores')
    plt.ylim(0, 100)
    plt.ylabel('Final scores')
    # size behaves a little differently for plus markers vs points, so we need to scale the plus a bit more up
    # so they show up about similarly
    plt.scatter(midterm_en, final_en, s=20, c='blue', marker="+", linewidths=0.5, label="English")
    plt.scatter(midterm_kr, final_kr, s=10, c='red', label="Korean")
    plt.legend()
    plt.grid()
    plt.title('Midterm vs Final scores, Korean and English Students')
    plt.show()

    # Plot total scores as a histogram, overlapping
    plt.xlim(0, 100)
    plt.xlabel('Total Scores')
    plt.ylabel('Number of Students')
    plt.hist(total_kr, bins=np.arange(0, 101, 5), color='red', label="Korean")
    # Turning down the alpha value a bit makes the blue layer slightly transparent, allowing the background to show
    plt.hist(total_en, bins=np.arange(0, 101, 5), color='blue', alpha=0.5, label="English")
    plt.legend()
    plt.title('Total Scores, Korean and English Students')
    plt.show()