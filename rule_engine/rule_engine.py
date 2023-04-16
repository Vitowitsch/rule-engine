import numpy as np
import logging


class RuleEngine:

    not_enough_data_available = "not_enough_data"

    def __init__(self, params):
        """Create instance."""
        self.EXPRESSION = params['Expression']
        self.RESPONSE_VALUE = params['ResponseValue']
        self.RESPONSE_DEFAULT = params['ResponseDefault']
        self.RESPONSE_COLUMN = params['ResponseColumn']
        self.MIN_DAYS = params['MinimumDaysRequired']

    def apply(self, df):
        """Apply expression and write output column."""

        # now this is a bit complex:
        # you can apply multiple times on the same column.
        # if the expr does not apply, the previous value is kept
        # we use it to question the dataframe for multiple classifications
        # which are exclusive against each other.

        if self.RESPONSE_COLUMN not in df:
            df[self.RESPONSE_COLUMN] = self.RESPONSE_DEFAULT

        if (df.index.nunique() < self.MIN_DAYS):
            df[self.RESPONSE_COLUMN] = self.not_enough_data_available
            return df

        df['tmp'] = df.eval(self.EXPRESSION)
        update = df.apply(
            lambda x: self.RESPONSE_VALUE if x['tmp'] == True else x[self.RESPONSE_COLUMN], axis=1)
        df[self.RESPONSE_COLUMN] = update
        return df.fillna(0).drop(columns=['tmp'])
