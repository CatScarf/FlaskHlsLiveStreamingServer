import time

ms = lambda timestamp : int(timestamp * 1000)

class Timer:

    def __init__(self):
        self.avg_time = None
        self.time_list = []
    
    def start(self):
        self.time_list = [time.time()]

    def reset(self):
        self.time_list = [time.time()]

    def timing(self):
        self.time_list += [time.time()]

    def __str__(self):
        if len(self.time_list) <= 1:
            return 'No enough timing, call timing at least once'
        total_time = self.time_list[-1] - self.time_list[0]
        if self.avg_time is None:
            avg_time = total_time
        else:
            avg_time = 0.9 * avg_time + 0.1 * total_time
        s = f'{ms(total_time)}ms(avg:{ms(avg_time)}ms)('
        for i in range(1, len(self.time_list)):
            timing_segment = self.time_list[i] - self.time_list[i-1]
            if i > 1:
                s += ' '
            s += f'{ms(timing_segment)}ms'
        s += ')'
        return s
