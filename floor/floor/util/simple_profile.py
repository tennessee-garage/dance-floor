import time
import os
import logging


class profile(object):
    """Utility decorator that implements a simple profiler.
    """

    __INSTANCE = None
    PROFILE_ENABLED = 'PROFILE' in os.environ and os.environ['PROFILE']

    def __new__(cls, print_seconds=None):
        if profile.__INSTANCE is None:
            profile.__INSTANCE = object.__new__(cls)
            profile.__INSTANCE.data = []

        if print_seconds:
            profile.__INSTANCE.print_seconds = print_seconds
            print("Profiling enabled: output every {} seconds".format(print_seconds))

        return profile.__INSTANCE

    @classmethod
    def instance(cls):
        return cls.__INSTANCE

    def init_timer(self, name):
        timer = {
            'name': name,
            'calls': 0,
            'cumulative': 0,
            'print_seconds': self.print_seconds,
            'last_print': time.time()
        }
        self.data.append(timer)
        return timer

    def print_profiling_data(self):
        self.data.sort(key=lambda v: v['cumulative'], reverse=True)

        # Total time spent will be the wrapper, which should have the highest time
        total_time = self.data[0]['cumulative']

        print("---------------------------")
        print(" {: >5s} | {: >8s} | {: >8s} | {: >6s} | {}"
              .format('calls', 'percall', 'cumul', 'pct', 'func'))
        for timer in self.data:
            self.print_profile_line(timer, total_time)
            self.reset_timer(timer)

    @classmethod
    def print_profile_line(cls, data, total):
        name = data['name']
        calls = data['calls']
        cumulative = data['cumulative']
        per_call = float(data['cumulative']) / data['calls']
        pct = 100 * (cumulative / float(total))

        # Print times in microseconds
        print(" {: >5d} | {: >8.3f} | {: >8.3f} | {: >6.2f} | {}"
              .format(calls, per_call*1000, cumulative*1000, pct, name))

    @classmethod
    def reset_timer(cls, timer):
        timer['calls'] = 0
        timer['cumulative'] = 0
        if timer['last_print']:
            timer['last_print'] = time.time()

    def __call__(self, fn, *args, **kwargs):
        # Return the original function if profiling is not enabled
        if not self.PROFILE_ENABLED:
            return fn

        function_name = fn.__name__
        timer = self.init_timer(function_name)

        def new_fn(*args, **kwargs):
            timer['calls'] += 1
            start_time = time.time()

            ret_val = fn(*args, **kwargs)

            total = time.time() - start_time
            timer['cumulative'] += total

            if timer['print_seconds']:
                if (time.time() - timer['last_print']) > timer['print_seconds']:
                    profile.instance().print_profiling_data()

            return ret_val

        return new_fn
