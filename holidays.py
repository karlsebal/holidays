# -*- coding: utf8 -*-

"""
Module Holiday

contains only one class calculating the holidays
for a particular year in a particular german state
using Lichtenberg’s easter algorithm

purpose is to calculate the working days for a
particular year


State codes used are

Baden-Württemberg: BW
Bayern: BY
Berlin: BE
Brandenburg: BB
Bremen: HB
Hamburg: HH
Hessen: HE
Mecklenburg-Vorpommern: MV
Niedersachsen: NI
Nordrhein-Westfalen: NW
Rheinland-Pfalz: RP
Saarland: SL
Sachsen: SN
Sachsen-Anhalt: ST
Schleswig-Holstein: SH
Thüringen: TH
"""


from datetime import date
from datetime import timedelta


class UnknownStateCodeException(Exception):
    pass


class Holidays:
    """
    Calculate holidays for year in state.
    If state is not given, calculate all.

    :param year: year to calculate holidays for
    :param state: state to calculate holidays for
    """

    def __init__(self, year:int, state:str=None): 

        # prepare
        easter_sunday = Holidays.get_easter_sunday(year)

        self.state = state.upper() if state else None
        self.year = year
        
        if self.state and self.state not in ( 
                                    'BW', 'BY', 'BE', 'BB', 
                                    'HB', 'HH', 'HE', 'MV', 
                                    'NI', 'NW', 'RP', 'SL', 
                                    'SN', 'ST', 'SH', 'TH'):

            raise UnknownStateCodeException

        self._holidays={}

        # common
        self._holidays['new year'] = date(year, 1, 1)
        self._holidays['labor day'] = date(year, 5, 1)
        self._holidays['german unification day'] = date(year, 10, 3)
        self._holidays['first christmas holiday'] = date(year, 12, 25)
        self._holidays['second christmas holiday'] = date(year, 12, 26)
        self._holidays['good friday'] = easter_sunday - timedelta(days=2)
        self._holidays['easter monday'] = easter_sunday + timedelta(days=1)
        self._holidays['ascention'] = easter_sunday + timedelta(days=39)
        self._holidays['whit monday'] = easter_sunday + timedelta(days=50)

        # state related
        if self.state:
            if self.state in ['BY', 'BW', 'ST']:
                self._holidays['epiphany'] = date(year, 1, 6)

            if self.state in ['BE']:
                self._holidays['womens day'] = date(year, 3, 8)

            if self.state in ['BB']:
                self._holidays['easter sunday'] = easter_sunday

            if self.state in ['BB']:
                self._holidays['whit_sunday'] = easter_sunday + timedelta(days=49)

            if self.state in ['BY', 'SL']:
                self._holidays['assumption'] = date(year, 8, 15)

            if self.state in ['BB', 'HB', 'HH', 'MV', 'NI', 'SN', 'ST', 'SH', 'TH']:
                self._holidays['reformation day'] = date(year, 10, 31)

            if self.state in ['BW', 'BY', 'NW', 'RP', 'SL']:
                self._holidays['all saints'] = date(year, 11, 1)

            # repentance and prayer is wednesday between Nov. 16th and Nov. 22nd
            if self.state in ['SN']:
                for day in range(16, 23):
                    if date(year, 11, day).isoweekday() == 3:
                        self._holidays['repentance and prayer'] = date(year, 11, day)

            if self.state in ['BW', 'BY', 'HE', 'NW', 'RP', 'SL']:
                self._holidays['corpus christi'] = easter_sunday + timedelta(days=60)


    def __repr__(self):
        return f"Holidays({self.year}, '{self.state}')"

    def __str__(self):
        string = ''

        swapped_dict = sorted(
            [(self._holidays[holiday], holiday) for holiday in self._holidays])

        for item in swapped_dict:
            string += f'\n{item[0].strftime("%d.%m.%Y")}: {item[1]}'

        # omit first newline
        return string[1:]
            

    def __getitem__(self, item):
        return self._holidays['item']

    def __contains__(self, item):
        return self._holidays.__contains__(item)

    def __iter__(self):
        return self._holidays.__iter__()

    def __len__(self):
        return self._holidays.__len__()

    def items(self):
        return self._holidays.items()

    def keys(self):
        return self._holidays.keys()

    def values(self):
        return self._holidays.values()


    def get_easter_sunday(year:int) -> date:
        """
        return date of easter sunday

        :param year: year to calculate easter sunday for
        :return: easter sunday as date
        :rtype: datetime.date
        """

        x = year
        # Säkularzahl
        k = x // 100
        # säkulare Mondschaltung
        m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
        # säkulare Sonnenschaltung
        s = 2 - (3 * k + 3) // 4
        # Mondparameter
        a = x % 19
        # Keim für den ersten Vollmond im Frühling
        d = (19 * a + m) % 30
        # kalendarische Korrekturgröße
        r = (d + a // 11) // 29
        # Ostergrenze
        og = 21 + d - r
        # erster Sonntag im März
        sz = 7 - (x + x // 4 + s) % 7
        # Entfernung des Ostersonntags von der Ostergrenze (Osterentfernung)
        oe = 7 - (og - sz) % 7
        # Datum des Ostersonntags als Märzdatum
        os = og + oe

        if os > 31:
            return date(year, 4, os - 31)
        else:
            return date(year, 3, os)


    def get_all(self) -> tuple:
        """
        return all holidays dates.

        :return: a tuple containing all holidays dates as datetime.date 
        """

        return self._holidays.values()


    def get_working_days(self) -> int:
        """
        return the number of working days for the year set

        :return: number of working days for the year set
        """

        # we start with full non-leap-year
        # which is 365
        # minus minimal occurrence of weekend days
        # which is 104
        # totalling to 261.
        # we will adjust for leap-years in the end
        workdays = 261

        # if first (and thus last if no leap-year) day
        # is weekend we subtract one more
        if date(self.year, 1, 1).isoweekday() >= 6:
            workdays -= 1

        # if this is a leap-year and the last day of the year
        # is no weekend, we have to add one
        try:
            date(self.year, 2, 29)
            if date(self.year, 12, 31).isoweekday() < 6:
                workdays += 1
        except ValueError:
            pass

        # in the end we substract the holidays not on a weekend
        for holiday in self.get_all():
            if holiday and holiday.isoweekday() < 6:
                workdays -= 1

        # done
        return workdays

# vim: set ai sts=4 ts=4 sw=4 et:
