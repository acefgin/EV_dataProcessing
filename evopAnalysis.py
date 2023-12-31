import numpy as np
import os, glob, csv, sys

def smooth(x,window_len=10,window='hanning'):

	if x.ndim != 1:
		raise ValueError("smooth only accepts 1 dimension arrays.")

	if x.size < window_len:
		raise ValueError("Input vector needs to be bigger than window size.")

	if window_len<3:
		return x

	if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
		raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

	s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
	#print(len(s))
	if window == 'flat': #moving average
		w = np.ones(window_len,'d')
	else:
		w = eval('np.'+window+'(window_len)')

	y = np.convolve(w/w.sum(),s,mode='valid')
	return np.round(y, decimals = 3)

def evopAnalysis(signal):
    signalDiff = np.round(np.diff(signal), 2)
    step_idx = [0]
    for n, diff in enumerate(signalDiff):
        if diff > 20:
            step_idx.append(n + 1)
    step_idx.append(len(signal) - 1)
    signalStages = []
    for i in range(len(step_idx)):
        if i != len(step_idx) - 1:
            signalStages.append(np.round(np.average(signal[step_idx[i]:step_idx[i+1]]), 2))
    return signalStages
    
def csvAnalyzer(filename):

    print(os.path.splitext(os.path.basename(filename))[0])

    x = []
    signalList = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []

    with open(filename,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        idx = 0
        headerDist = {}

        for row in plots:
            if idx == 0:
                for n, header in enumerate(row):
                    headerDist[header] = n
            if idx == 8:
                sampleId = row[0]
                x = row[7:]
                x = [float(i)/1000/60 - 5 for i in x]
            if idx == 11:
                y1 = row[7:]
                y1 = np.array([float(i) for i in y1])
                if len(y1) >= 9: signalList.append(y1)
            if idx == 12:
                y2 = row[7:]
                y2 = np.array([float(i) for i in y2])
                if len(y2) >= 9: signalList.append(y2)
            if idx == 13:
                y3 = row[7:]
                y3 = np.array([float(i) for i in y3])
                if len(y3) >= 9: signalList.append(y3)
            if idx == 14:
                y4 = row[7:]
                y4 = np.array([float(i) for i in y4])
                if len(y4) >= 9: signalList.append(y4)
            if idx == 15:
                y5 = row[7:]
                y5 = np.array([float(i) for i in y5])
                if len(y5) >= 9: signalList.append(y5)
            idx += 1
    rltList = []
    if len(signalList) != 0:

        for i in range(5):
            rltList.append(evopAnalysis(signalList[i]))
    return sampleId, rltList

if __name__=='__main__':
    csvfoler = sys.argv[1]
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    print('Analysis optical EV test CSVs...')
    
    header = ["SampleID", "IlluminationLv", "PD1", "PD2", "PD3", "PD4", "PD5"]
    with open('report.csv','w', newline = '') as reportCsv:
        writer = csv.writer(reportCsv)
        writer.writerow(header)
        for filename in filenames:
            sampleId, chStages = csvAnalyzer(filename)
            for lv in range(5):
                data2write = [sampleId]
                data2write.append(lv + 1)
                for ch in range(5):
                    data2write.append(chStages[ch][lv])
                writer.writerow(data2write)
    input('Press <Enter> to exit')

