from riotwatcher import LolWatcher

from recomteam.config import app_config

RANKED_TIER = {
    "IRON": 0,
    "BRONZE": 500,
    "SILVER": 1000,
    "GOLD": 2000,
    "PLATINUM": 3000,
    "DIAMOND": 4000,
    "MASTER": 4600,
    "GRANDMASTER": 5200,
    "CHALLENGER": 6000,
}

RANKED_DIVISION = {
    "I": 400,
    "II": 300,
    "III": 200,
    "IV": 100
}


class LeagueOfLegends:
    def __init__(self):
        self.watcher = LolWatcher(app_config.RIOT_API_KEY)

    def get_points(self, account_name, region):
        account = self.watcher.summoner.by_name(region, account_name)
        account_id = account.get('accountId')
        summoner_id = account.get('id')

        matches = self.watcher.match.matchlist_by_account(region, account_id)

        normal_matches = self.__find_first_ten_normal_match(region, matches)

        points = self.__calculate_points(account_name, summoner_id, region, normal_matches)

        return round(points)

    def __find_match_by_id(self, region, match_id):
        try:
            return self.watcher.match.by_id(region, match_id)
        except Exception as e:
            print(str(e))
            return None

    def __find_first_ten_normal_match(self, region, matches):
        matches = matches.get("matches")

        normal_matches = []

        for match in matches:
            if self.__is_not_aram(match):
                match = self.__find_match_by_id(region, match.get("gameId"))
                if self.__is_classic(match):
                    normal_matches.append(match)

            if len(normal_matches) == 5:
                break

        return normal_matches

    def __get_player_ranked_stats(self, region, summoner_id):
        try:
            ranked_stats = self.watcher.league.by_summoner(region, summoner_id)
    
            if ranked_stats and isinstance(ranked_stats, dict) and \
                    ranked_stats.get("tier") in RANKED_TIER and ranked_stats.get("rank") in RANKED_DIVISION:
                return ranked_stats
            return None
        except Exception as e:
            print(str(e))
            return None

    def __calculate_points(self, account_name, summoner_id, region, matches):
        average_scores = 0
        account_scores = 0
        number_of_matches = len(matches)
        number_of_matches_with_rank = 0
        average_mmr = 0

        mmr = None

        for match in matches:
            average_scores += self.__calculate_the_average_score(match)
            account_participant_id = self.__get_account_participant_id(account_name, match)
            account_scores += self.__calculate_the_account_score(account_participant_id, match)

            mmr_in_game = self.__calculate_average_mmr_in_match(match)
            if mmr_in_game and mmr_in_game > 0:
                average_mmr += mmr_in_game
                number_of_matches_with_rank += 1

        average_scores = average_scores / number_of_matches
        account_scores = account_scores / number_of_matches

        if average_mmr:
            average_mmr = average_mmr / number_of_matches_with_rank

        ranked_stats = self.__get_player_ranked_stats(region, summoner_id)
        if ranked_stats:
            mmr = RANKED_TIER.get(ranked_stats.get("tier")) + RANKED_DIVISION.get(ranked_stats.get("rank"))
        if mmr:
            return mmr + (average_mmr * (account_scores - average_scores) / 100)
        else:
            if average_mmr:
                return average_mmr + (average_mmr * (account_scores - average_scores) / 100)
            return 1000 + (1000 * (account_scores - average_scores) / 100)

    def __calculate_average_mmr_in_match(self, match):
        sum_mmr = 0
        player_with_rank = 0
        for participant in match.get("participantIdentities"):
            player = participant.get("player")
            ranked_stats = self.__get_player_ranked_stats(player.get("platformId"), player.get("summonerId"))
            if ranked_stats:
                player_with_rank += 1
                sum_mmr += RANKED_TIER.get(ranked_stats.get("tier")) + RANKED_DIVISION.get(ranked_stats.get("rank"))

        return sum_mmr / player_with_rank if sum_mmr > 0 else None

    @staticmethod
    def __calculate_the_average_score(match):
        kills = 0
        assists = 0
        deaths = 0
        for participant in match.get("participants"):
            stats = participant.get("stats")
            kills += stats.get("kills")
            assists += stats.get("assists")
            deaths += stats.get("deaths")

        # CALCULATE AVERAGE
        average_kills = 10 / kills
        average_assists = 10 / assists
        average_deaths = 10 / deaths

        return (average_kills + (average_assists / 2)) / average_deaths

    @staticmethod
    def __calculate_the_account_score(account_participant_id, match):
        stats = next(participant.get("stats")
                     for participant in match.get("participants")
                     if participant.get("participantId") == account_participant_id)

        kills = stats.get("kills")
        assists = stats.get("assists")
        deaths = stats.get("deaths")

        return (kills + (assists / 2)) / deaths

    @staticmethod
    def __get_account_participant_id(account_name, match):
        return next(participant.get("participantId")
                    for participant in match.get("participantIdentities")
                    if participant.get("player").get("summonerName") == account_name)

    @staticmethod
    def __is_classic(match):
        if not isinstance(match, dict):
            return False

        if match.get("gameMode") == "CLASSIC" and match.get("gameType") == "MATCHED_GAME":
            return True
        return False

    @staticmethod
    def __is_not_aram(match):
        # MID LANE
        if match.get("lane") == "MID" and match.get("role") == 'SOLO':
            return True

        # TOP LANE
        elif match.get("lane") == "TOP" and match.get("role") == 'SOLO':
            return True

        # JUNGLE
        elif match.get("lane") == "JUNGLE" and match.get("role") == 'NONE':
            return True

        # BOTTOM LANE
        elif match.get("lane") == "BOTTOM" and (match.get("role") == 'DUO_CARRY' or match.get("role") == 'DUO_SUPPORT'):
            return True

        return False


lol = LeagueOfLegends()
