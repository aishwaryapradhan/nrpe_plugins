#!/usr/bin/python

import sys
import argparse
import signal


def check_variable(my_var, k):
    if my_var.strip() == '':
        if k == 1:
            return sys.maxsize
        else:
            return -sys.maxsize
    else:
        try:
            return int(my_var)
        except:
            print("UNKNOWN - Issue with configuration")
            sys.exit(3)



# sys.maxint
def main():
    timeout_seconds = 10
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--warning", required=True, help="Set the warning threshold e.g.: -w 'min:max'")
    ap.add_argument("-c", "--critical", required=True, help="Set the critical threshold e.g.: -c 'min:max'")
    ap.add_argument("-p", "--process", required=True, help="Give the process name e.g.: -p 'psAgent'")
    args = vars(ap.parse_args())

    process_name = args["process"]
    try:
        w_min, w_max = args["warning"].split(":")
        c_min, c_max = args["critical"].split(":")
    except:
        print("UNKNOWN - Issue with configuration")
        sys.exit(3)


    w_min = check_variable(w_min,-1)
    w_max = check_variable(w_max,1)
    c_min = check_variable(c_min,-1)
    c_max = check_variable(c_max, 1)

    # Add alarm exception
    try:
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.alarm(timeout_seconds)

        # process_count = int(os.popen("ps -eaf | grep '{}' | grep -v grep | wc -l".format(process_name)).readline().strip()) - 1
        process_count = 10
    except AlarmException as a:
        print("CRITICAL - command is taking more than 10 seconds to execute.")
        sys.exit(2)


    # Checking if critical threshold are getting breached or not
    if process_count < c_min or process_count > c_max:
        print("CRITICAL - Only {} process found with name: '{}'".format(process_count, process_name))
        sys.exit(2)


    # Checking if warning threshold are getting breached or not
    if process_count < w_min or process_count > w_max:
        print("WARNING - Only {} process found with name: '{}'".format(process_count, process_name))
        sys.exit(1)


    # Else everything is good.
    print("OK - Found {} process found with {} name".format(process_count, process_name))


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


if __name__ == '__main__':
    main()
