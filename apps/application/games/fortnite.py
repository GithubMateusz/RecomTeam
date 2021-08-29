import fortnite_api

from recomteam.config import app_config


class Fortnite:
    def __init__(self):
        self.api = fortnite_api.FortniteAPI(api_key=app_config.FORTNITE_API_KEY)

    def get_points(self, account_name):
        account = self.get_account_by_name(account_name)
        stats = account.raw_data.get("stats").get("all")
        return self.__calculate_points(stats)

    def get_account_by_name(self, account_name):
        return self.api.stats.fetch_by_name(name=account_name)

    def __calculate_points(self, stats):
        overall_kd = self.__get_kd_or_none(stats, "overall")
        solo_kd = self.__get_kd_or_none(stats, "solo")
        duo_kd = self.__get_kd_or_none(stats, "duo")
        trio_kd = self.__get_kd_or_none(stats, "trio")
        squad_kd = self.__get_kd_or_none(stats, "squad")

        game_mode_with_kd = self.__game_mode_with_kd(stats)

        points = 1000 * overall_kd if overall_kd else 0
        points += 1000 * solo_kd if solo_kd else 0
        points += 900 * duo_kd if duo_kd else 0
        points += 800 * trio_kd if trio_kd else 0
        points += 700 * squad_kd if squad_kd else 0

        points = points / game_mode_with_kd

        return round(points)

    @staticmethod
    def __get_kd_or_none(stats, game_mode):
        try:
            return stats.get(game_mode).get("kd")
        except Exception as e:
            print(str(e))
            return None

    def __game_mode_with_kd(self, stats):
        game_mode_with_kd = 0
        if self.__get_kd_or_none(stats, "overall"):
            game_mode_with_kd +=1
        if self.__get_kd_or_none(stats, "solo"):
            game_mode_with_kd +=1
        if self.__get_kd_or_none(stats, "duo"):
            game_mode_with_kd +=1
        if self.__get_kd_or_none(stats, "trio"):
            game_mode_with_kd +=1
        if self.__get_kd_or_none(stats, "squad"):
            game_mode_with_kd +=1
        return game_mode_with_kd


fortnite = Fortnite()
