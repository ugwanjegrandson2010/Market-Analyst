class ScoreNormalizer:

    @staticmethod 
    def normalize(score, maximum):

        if maximum == 0:
            return 0 
        return round(score / maximum, 4)

    