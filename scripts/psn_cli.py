from psnawp_api import PSNAWP
from pprint import pprint
import datetime
import json
from scripts.config import NPSSO

psnawp = PSNAWP(NPSSO)

client = psnawp.me()
print(f"ME - {client.online_id}")
print(f"ME - {client.account_id}")


def convert_date(lastTime, time_available=False):
    lastUpdateDay = int(lastTime.strftime("%d"))
    if (4 <= lastUpdateDay % 10 <= 9) or \
            (11 <= lastUpdateDay % 10 <= 19) or \
            lastUpdateDay % 10 == 0:
        nmSuffix = "th"
    elif lastUpdateDay % 10 == 1:
        nmSuffix = "st"
    elif lastUpdateDay % 10 == 2:
        nmSuffix = "nd"
    elif lastUpdateDay % 10 == 3:
        nmSuffix = "rd"
    dictToReturn = {
        "day": lastUpdateDay,
        "suffix": nmSuffix,
        "month": lastTime.strftime("%B"),
        "year": lastTime.strftime("%Y")
    }
    if time_available:
        dictToReturn["time"] = lastTime.strftime("%H:%M:%S")
    return dictToReturn


def countTrophies(trophies):
    return f"{trophies.platinum + trophies.gold + trophies.silver + trophies.bronze:,d}"


def defineTrophies(trophies):
    return {
        "platinum": f"{trophies.platinum:,d}",
        "gold": f"{trophies.gold:,d}",
        "silver": f"{trophies.silver:,d}",
        "bronze": f"{trophies.bronze:,d}"
    }


def getUsersTitles(nickname):
    finalUser = psnawp.user(online_id=nickname)
    userProfile = finalUser.profile()
    userTrophySummary = finalUser.trophy_summary()

    # pprint(finalUser.profile())
    # print(finalUser.trophy_summary())

    # language
    # lng = finalUser.profile()['languages'][0].split("-")[0]
    # print(lng)
    # print(f'https://hatscripts.github.io/circle-flags/flags/{lng}.svg')

    for dictionary in userProfile["avatars"]:
        if dictionary["size"] == "l":
            avatar_url = dictionary["url"]

    user_dict = {
        "onlineId": userProfile["onlineId"],
        "aboutMe": userProfile["aboutMe"],
        "avatar_url": avatar_url,
        "languages": userProfile["languages"],
        "isPlus": userProfile["isPlus"],
        "tier": userTrophySummary.tier,
        "trophy_level": userTrophySummary.trophy_level,
        "progress": userTrophySummary.progress,
        "total": countTrophies(userTrophySummary.earned_trophies),
        "platinum": f"{userTrophySummary.earned_trophies.platinum:,d}",
        "gold": f"{userTrophySummary.earned_trophies.gold:,d}",
        "silver": f"{userTrophySummary.earned_trophies.silver:,d}",
        "bronze": f"{userTrophySummary.earned_trophies.bronze:,d}",
        # "": userTrophySummary.,
        # "": userProfile[""],
    }
    # return user_dict

    usersTitles = list(finalUser.trophy_titles(limit=200))
    user_dict["total_items"] = usersTitles[0].total_items_count
    titles_list = []
    closest = datetime.timedelta(days=36500)
    closest_np_id = None
    for title in usersTitles:
        title_dict = {}
        rank = {
            "S": "100-100",
            "A": "80-99",
            "B": "60-79",
            "C": "40-59",
            "D": "20-39",
            "E": "1-19",
            "F": "0-0",
        }
        for rankL, rangeN in rank.items():
            minN = int(rangeN.split("-")[0])
            maxN = int(rangeN.split("-")[1])
            if minN <= title.progress <= maxN:
                rankR = rankL
                break
        title_dict["name"] = title.title_name
        title_dict["icon"] = title.title_icon_url
        title_dict["platforms"] = [i.value for i in title.title_platform]
        title_dict["progress"] = title.progress
        title_dict["rank"] = rankR
        title_dict["earned_trophies_total"] = countTrophies(title.earned_trophies)
        title_dict["earned_trophies"] = defineTrophies(title.earned_trophies)
        title_dict["defined_trophies_total"] = countTrophies(title.defined_trophies)
        title_dict["defined_trophies"] = defineTrophies(title.defined_trophies)
        title_dict["last_update"] = convert_date(title.last_updated_date_time)

        now_t = datetime.datetime.strptime(str(datetime.datetime.now()).split('.')[0], "%Y-%m-%d %H:%M:%S")
        update_t = datetime.datetime.strptime(str(title.last_updated_date_time).split('+')[0], "%Y-%m-%d %H:%M:%S")
        # print(update_t, "+", now_t-update_t, "=", now_t, closest)
        if now_t - update_t < closest:
            closest = now_t - update_t
            user_dict["latest_name"] = title.title_name
            closest_np_id = title.np_communication_id

        # title_dict[""] = title.
        titles_list.append(title_dict)
    user_dict["titles"] = titles_list
    closest_id = psnawp.search().get_title_id(user_dict["latest_name"])[1]
    closest_game = psnawp.game_title(title_id=closest_id, np_communication_id=closest_np_id).get_details()[0]
    for dictionary in closest_game["media"]["images"]:
        if dictionary["type"] == "GAMEHUB_COVER_ART":
            user_dict["latest_img"] = dictionary["url"]
            break
    return user_dict


def getTitlesTrophies(nickname, title_to_search):
    # print(nickname, title_to_search)
    finalUser = psnawp.user(online_id=nickname)
    userProfile = finalUser.profile()
    allTitles = list(finalUser.trophy_titles())
    for dictionary in userProfile["avatars"]:
        if dictionary["size"] == "l":
            avatar_url = dictionary["url"]
            break
    title_info = {
        "onlineId": userProfile["onlineId"],
        "aboutMe": userProfile["aboutMe"],
        "avatar_url": avatar_url,
        "languages": userProfile["languages"],
        "isPlus": userProfile["isPlus"],
    }
    for title in allTitles:
        if title.title_name.strip() != title_to_search:
            continue
        rank = {
            "S": "100-100",
            "A": "80-99",
            "B": "60-79",
            "C": "40-59",
            "D": "20-39",
            "E": "1-19",
            "F": "0-0",
        }
        for rankL, rangeN in rank.items():
            minN = int(rangeN.split("-")[0])
            maxN = int(rangeN.split("-")[1])
            if minN <= title.progress <= maxN:
                rankR = rankL
                break
        title_info["title_name"] = title.title_name
        title_info["np_communication_id"] = title.np_communication_id
        title_info["title_icon_url"] = title.title_icon_url
        title_info["progress"] = title.progress
        title_info["rank"] = rankR
        title_info["earned_trophies_total"] = countTrophies(title.earned_trophies)
        title_info["earned_trophies"] = defineTrophies(title.earned_trophies)
        title_info["defined_trophies_total"] = countTrophies(title.defined_trophies)
        title_info["defined_trophies"] = defineTrophies(title.defined_trophies)
        title_info["last_update"] = convert_date(title.last_updated_date_time)
        title_info["platforms"] = [str(i.value) for i in title.title_platform]

        if "PS5" in title_info["platforms"]:
            title_info["best_platform"] = "PS5"
        elif "PS4" in title_info["platforms"]:
            title_info["best_platform"] = "PS4"
        elif "PS3" in title_info["platforms"]:
            title_info["best_platform"] = "PS3"

        title_info["has_groups"] = title.has_trophy_groups

        title_info["title_id"] = psnawp.search().get_title_id(title.title_name)[1]

    # psnGameTitle = psnawp.game_title(title_id=title_info["title_id"], np_communication_id=title_info["np_communication_id"])
    psnGameTitle = psnawp.game_title(title_id=title_info["title_id"],
                                     np_communication_id=title_info["np_communication_id"])

    gameDetails = psnGameTitle.get_details()[0]
    # print(json.dumps(gameDetails, indent=2))

    title_info["publisherName"] = gameDetails["publisherName"]
    title_info["synonyms"] = title_info["title_name"]
    try:
        title_info["synonyms"] = gameDetails["synonyms"]
    except:
        pass
    # print(json.dumps(gameDetails["media"]["images"], indent=2))
    # gameDetails["media"]["images"]["GAMEHUB_COVER_ART"]
    for dictionary in gameDetails["media"]["images"]:
        if dictionary["type"] == "MASTER":
            title_info["master_img"] = dictionary["url"]
            break
    for dictionary in gameDetails["media"]["images"]:
        if dictionary["type"] == "GAMEHUB_COVER_ART":
            title_info["background_img"] = dictionary["url"]
            break
    title_info["minimumAge"] = gameDetails["minimumAge"]
    title_info["genres"] = set()
    for g in set(gameDetails["defaultProduct"]["genres"] + gameDetails["defaultProduct"]["subGenres"]):
        if g == "N/A":
            continue
        title_info["genres"].add(g)

    title_info["trophies_list"] = [
        {'group_name': 'Base Game',
         'group_id': 'default',
         'progress': title_info["progress"],
         'group_icon': title_info["title_icon_url"],
         "earned_trophies_total": title_info["earned_trophies_total"],
         "earned_trophies": title_info["earned_trophies"],
         "defined_trophies_total": title_info["defined_trophies_total"],
         "defined_trophies": title_info["defined_trophies"],
         "last_update": title_info["last_update"],
         }
    ]
    if title_info["has_groups"]:
        title_info["trophies_list"] = []
        try:
            userTrophyGroups = finalUser.trophy_groups_summary(np_communication_id=title_info["np_communication_id"],
                                                               platform=title_info["best_platform"],
                                                               include_metadata=True).trophy_groups
        except:
            userTrophyGroups = finalUser.trophy_groups_summary(np_communication_id=title_info["np_communication_id"],
                                                               platform=title_info["best_platform"]).trophy_groups
        for group in userTrophyGroups:
            group_dict = {}
            group_dict["group_name"] = "Base Game" if str(
                group.trophy_group_id) == "default" else group.trophy_group_name
            group_dict["group_id"] = group.trophy_group_id
            group_dict["progress"] = group.progress
            group_dict["group_icon"] = group.trophy_group_icon_url
            if group_dict["group_icon"] == None:
                group_dict["group_icon"] = title_info["title_icon_url"]
            group_dict["earned_trophies_total"] = countTrophies(group.earned_trophies)
            group_dict["earned_trophies"] = defineTrophies(group.earned_trophies)
            group_dict["defined_trophies_total"] = countTrophies(group.defined_trophies)
            group_dict["defined_trophies"] = defineTrophies(group.defined_trophies)
            group_dict["last_update"] = None if group.last_updated_datetime is None else convert_date(
                group.last_updated_datetime)
            title_info["trophies_list"].append(group_dict)
    # return title_info

    for group in title_info["trophies_list"]:
        groupTrophiesTypes = finalUser.trophies(np_communication_id=title_info["np_communication_id"],
                                                platform=title_info["best_platform"],
                                                trophy_group_id=group["group_id"])
        groupTrophiesDetail = psnGameTitle.trophies(platform=title_info["best_platform"],
                                                    trophy_group_id=group["group_id"])
        group["trophies"] = []
        for etdt, etd in zip(groupTrophiesTypes, groupTrophiesDetail):
            try:
                last_update_str = convert_date(etdt.progressed_date_time, True)
            except:
                last_update_str = "None"
            try:
                earned_date_time_str = convert_date(etdt.earned_date_time, True)
            except:
                earned_date_time_str = "None"
            trophy = {
                "type": etd.trophy_type.name,
                "trophy_hidden": etdt.trophy_hidden,
                "rarity": etdt.trophy_rarity.name.replace("_", " "),
                "rarity_class": etdt.trophy_rarity.name.lower(),
                "earn_rate": float(etdt.trophy_earn_rate),
                "name": etd.trophy_name,
                "detail": etd.trophy_detail,

                "progress_available": True if etd.trophy_progress_target_value is not None else False,
                "progress_rate": etdt.progress_rate,
                "progress": etdt.progress,
                "progress_target": etd.trophy_progress_target_value,
                "update_date": last_update_str,

                "icon_url": etd.trophy_icon_url,
                "earned": etdt.earned,
                "earned_date": earned_date_time_str
            }
            group["trophies"].append(trophy)

    return title_info


if __name__ == "__main__":
    pprint(getUsersTitles("PowerPyx"))
    pprint(getTitlesTrophies("PowerPyx", "Horizon Forbidden West"))
