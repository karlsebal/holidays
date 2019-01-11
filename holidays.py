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


        # common
        self.new_year = date(year, 1, 1)
        self.labor_day = date(year, 5, 1)
        self.german_unification_day = date(year, 10, 3)
        self.first_christmas_holiday = date (year, 12, 25)
        self.second_christmas_holiday = date (year, 12, 26)
        self.good_friday = easter_sunday - timedelta(days=2)
        self.easter_monday = easter_sunday + timedelta(days=1)
        self.ascention = easter_sunday + timedelta(days=39)
        self.whit_monday = easter_sunday + timedelta(days=50)

        # state related
        if self.state in [None, 'BY', 'BW', 'ST']:
            self.epiphany = date(year, 1, 6)
        else:
            self.epiphany = None

        if self.state in [None, 'BB']:
            self.easter_sunday = easter_sunday
        else:
            self.easter_sunday = None

        if self.state in [None, 'BB']:
            self.whit_sunday = easter_sunday + timedelta(days=49)
        else:
            self.whit_sunday = None

        if self.state in [None, 'BY', 'SL']:
            self.assumption = date(year, 8, 15)
        else:
            self.assumption = None

        if self.state in [None, 'BB', 'MV', 'SN', 'ST', 'TH']:
            self.reformation_day = date(year, 10, 31)
        else:
            self.reformation_day = None

        if self.state in [None, 'BW', 'BY', 'NW', 'RP', 'SL']:
            self.all_saints = date(year, 11, 1)
        else:
            self.all_saints = None

        # repentance and prayer is wednesday between Nov. 16th and Nov. 22nd
        if self.state in [None, 'SN']:
            for day in range(16, 23):
                if date(year, 11, day).isoweekday() == 3:
                    self.repentance_and_prayer = date(year, 11, day)
        else:
            self.repentance_and_prayer = None

        if self.state in [None, 'BW', 'BY', 'HE', 'NW', 'RP', 'SL']:
            self.corpus_christi = easter_sunday + timedelta(days=60)
        else:
            self.corpus_christi = None


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
        return a tuple of all holidays.

        holidays not valid for the state set are None so
        the tuple returned will contain None elements in
        that case

        :return: a tuple containing all holidays. 
        """

        return (
            self.new_year,
            self.labor_day,
            self.german_unification_day,
            self.first_christmas_holiday,
            self.second_christmas_holiday,
            self.good_friday,
            self.easter_monday,
            self.ascention,
            self.whit_monday,
            self.epiphany,
            self.easter_sunday,
            self.whit_sunday,
            self.assumption,
            self.reformation_day,
            self.all_saints,
            self.repentance_and_prayer,
            self.corpus_christi
            )

    def get_workdays(self) -> int:
        """
        return the number of workdays for the year set

        :return: number of workdays for the year set
        """

        # we start with full non-leap-year
        # which is 365
        # minus minimal occurance of weekend days
        # which is 104
        # totalling to 261.
        # we will adjust for leap-years in the end
        workdays = 261

        # if first (and thus last if no leap-year) day
        # is weekend we substract one more
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
