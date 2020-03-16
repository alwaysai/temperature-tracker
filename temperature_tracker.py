from gpiozero import CPUTemperature
import time


class TemperatureTracker:

    MAX_TEMP_RASP4 = 82.0

    def __init__(self, temp_time_list=[]):
        self.temp_time_list = temp_time_list
        self.start_timestamp = None
        self.stop_timestamp = None


    def minimum(self):
        """
        Returns the minimum temperature reading in the instance list

        Calls the minimum_from() function, using the instance list as an input parameter

        Returns
        -------
        float
            The temperature from the input list with the lowest temperature value
        """
        return self.minimum_from(self.temp_time_list)[0]


    def minimum_from(self, temp_time_list):
        """
        Returns the minimum temperature reading in the specified list

        Get the minimum temperature listed from an input list of tuples that contain
         temperature floats and time data

        Parameters
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken

        Returns
        -------
        (float, time)
            The tuple from the input list with the lowest temperature value
        """
        result = temp_time_list[0]
        for temp, time in temp_time_list:
            if temp < result[0]:
                result = (temp, time)

        return result


    def maximum(self):
        """
        Returns the maximum temperature reading in the instance list

        Calls the maximum_from() function, using the instance list as an input parameter

        Returns
        -------
        float
            The temperature from the input list with the highest temperature value
        """
        return self.maximum_from(self.temp_time_list)[0]


    def maximum_from(self, temp_time_list):
        """
        Returns the maximum temperature reading in the specified list

        Get the maximum temperature listed from an input list of tuples that contain
         temperature floats and time data

        Parameters
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken

        Returns
        -------
        (float, time)
            The tuple from the input list with the highest temperature value
        """
        result = temp_time_list[0]
        for temp, time in temp_time_list:
            if temp > result[0]:
                result = (temp, time)

        return result


    def update(self):
        """
        Updates the temperature readings

        Calculates the current temperature reading, calls the update_from() function,
        using the instance list as an input parameter, as well as the new temperature reading.
        """
        cpu = CPUTemperature()
        new_reading = (cpu.temperature, time.localtime())

        self.update_from(new_reading, self.temp_time_list)



    def update_from(self, new_reading, temp_time_list):
        """
        Takes a new temperature reading and appends this to
        the input list.

        Updates the instance list with the appended list.

        Parameters
        -------
        new_reading : (float, time)
        temp_time_list : [(float, time)]
        """
        temp_time_list.append(new_reading)

        # update the instance list with the new set of readings
        self.temp_time_list = temp_time_list



    def now(self):
        """
        Calculates and returns the current temperature and timestamp

        Returns
        -------
        new_reading : (float, time)
            The current temperature and time
        """
        cpu = CPUTemperature()
        new_reading = (cpu.temperature, time.localtime())
        return new_reading



    def average(self):
        """
        Returns the average temperature reading in the instance list

        Calls the average_from() function, using the instance list as an input parameter

        Returns
        -------
        float
            The temperature from the input list with the average temperature value
        """
        return self.average_from(self.temp_time_list)



    def average_from(self, temp_time_list):
        """
        Returns the average temperature reading in the specified list

        Calculates the average temperature from an input list of tuples that contain
         temperature floats and time data

        Parameters
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken

        Returns
        -------
        float
            The average temperature reading from the input list
        """
        total_temp = 0.0
        count = 0

        for temp, time in temp_time_list:
            total_temp += temp
            count += 1

        return total_temp / count



    def count(self):
        """
        Returns the number of temperature readings in the specified list

        Calls count_from() with the instance list as input

        Returns
        -------
        int
            The number of temperature readings from the input list
        """

        return self.count_from(self.temp_time_list)



    def count_from(self, temp_time_list):
        """
        Returns the number of temperature readings in the specified list

        Parameters
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken

        Returns
        -------
        int
            The number of temperature readings from the input list
        """

        count = len(temp_time_list)
        return count


    def temperatures(self):
        """
        Returns the temperature readings for the instance

        Returns
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken
        """
        return self.temp_time_list



    def start(self):
        """
        Marks the start time of the temperature tracker

        Sets the instance time of start_timestamp to current time
        """
        self.start_timestamp = time.localtime()


    def get_start(self):
        """
        Returns the start time of the temperature tracker

        Returns
        -------
        time
            The time the tracker started
        """
        return self.start_timestamp


    def stop(self):
        """
        Marks the stop time of the temperature tracker

        Sets the instance time of stop_timestamp to current time
        """
        self.stop_timestamp = time.localtime()


    def get_stop(self):
        """
        Returns the stop time of the temperature tracker

        Returns
        -------
        time
            The time the tracker stopped
        """
        return self.stop_timestamp


    def summary_from(self, temp_time_list):
        """
        Prints out a summary of the temperature readings in easy to read format.

        Includes average temperature, the number of readings, each reading in
        human-readable format, and the the maximum, minimum, and average temperatures.

        Parameters
        -------
        temp_list : [(float, time)]
            A list of (temperature, time) tuples that each specify a temperature
             readings and the time the reading was taken

        Returns
        -------
        string
            A string of summary details on the temperature readings
        """
        temp_dict = {}

        # first make sure all readings are up to date
        temp_dict['average'] = self.average()
        temp_dict['minimum'] = self.minimum()
        temp_dict['maximum'] = self.maximum()
        temp_dict['count'] = self.count()
        temp_dict['start_timestamp'] = self.start_timestamp
        temp_dict['stop_timestamp'] = self.start_timestamp

        if temp_dict['start_timestamp'] is None:
            return "The temperature tracker has not yet been started"
        else:
            summary_string = "The temperature tracker was started at: " + \
                             time.strftime('%Y-%m-%d %H:%M:%S',
                                           temp_dict['start_timestamp']) + "\n"
            summary_string += "A total of " + \
                str(temp_dict['count']) + " have been gathered\n"
            summary_string += "The readings so far are: \n"

            for i in range(0, len(temp_time_list)):
                summary_string += "\t\t" + "{:1.2f}C/{:1.2f}F at time {}\n".format(temp_time_list[i][0],
                                                                                   (((temp_time_list[i][0] * (9 / 5)) + 32)),
                                                                                   time.strftime('%Y-%m-%d %H:%M:%S', temp_time_list[i][1]))

            summary_string += "The average temperature was: {:1.2f}C/{:1.2f}F".format(
                temp_dict['average'], (((temp_dict['average'] * (9 / 5)) + 32))) + "\n"

            summary_string += "The maximum temperature was: {:1.2f}C/{:1.2f}F".format(
                temp_dict['maximum'], (((temp_dict['maximum'] * (9 / 5)) + 32))) + "\n"

            summary_string += "The minimum temperature was: {:1.2f}C/{:1.2f}F".format(
                temp_dict['minimum'], (((temp_dict['minimum'] * (9 / 5)) + 32))) + "\n"

            if temp_dict['stop_timestamp'] is not None:
                summary_string += "The temperature tracker was stopped at time: " + \
                                  time.strftime('%Y-%m-%d %H:%M:%S',temp_dict['stop_timestamp']) + "\n"

            else:
                summary_string += "The temperature tracker is still on.\n"


        return summary_string



    def summary(self):
        """
        Prints out a summary of the temperature readings in easy to read format.

        Includes average temperature, the number of readings,
        the maximum temperature and the minimum temperature.

        Calls summary_from() with the instance list as input to gather summary data

        Returns
        -------
        string
            A string of summary details on the temperature readings
        """

        return self.summary_from(self.temp_time_list)
