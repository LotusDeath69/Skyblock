import requests


def formatDecimal(x: object) -> object:
    try:
        x = ('%f' % x).rstrip('0').rstrip('.')
        return x
    except TypeError:
        return x


def uuid(ign):
    """Find the UUID of a player using Mojang's api"""
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    x = data["id"]
    return x


def profile_id(ign, profile, api):
    """Find the profile id of the player using the profile name"""
    data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={api}&"
                        f"uuid={uuid(ign)}").json()
    cute_names = []
    for i in data['profiles']:
        cute_names.append(i['cute_name'])

    id = []
    for i in data['profiles']:
        id.append(i['profile_id'])

    for i in range(len(cute_names)):
        if cute_names[i].lower() == profile.lower():
            return id[i]


def skill(api, profile, uuid):
    """Find the skill exp the player is currently at"""
    info = requests.get('https://api.hypixel.net/resources/skyblock/skills').json()
    exp_required = []
    for i in info['collections'][f'FARMING']['levels']:
        exp_required.append(i['totalExpRequired'])

    skills_60 = ['farming', 'mining', 'combat', 'enchanting']
    a = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api}&profile={profile}').json()
    lvl = []
    for i in skills_60:
        skill_exp = a['profile']['members'][uuid][f'experience_skill_{i.lower()}']
        lvl.append(skill_exp)
    for i in range(len(lvl)):
        print(f'{skills_60[i]}: {skill_lvl(lvl[i], exp_required)}')

    exp_required = []
    for i in info['collections'][f'FORAGING']['levels']:
        exp_required.append(i['totalExpRequired'])
    skills_50 = ['foraging', 'fishing', 'taming', 'alchemy']
    lvl = []
    for i in skills_50:
        skill_exp = a['profile']['members'][uuid][f'experience_skill_{i.lower()}']
        lvl.append(skill_exp)
    for i in range(len(lvl)):
        print(f'{skills_50[i]}: {skill_lvl(lvl[i], exp_required)}')


def skill_lvl(lvl, exp_required):
    """Calculate the essential skills of the player"""
    for i in range(len(exp_required)):
        if lvl < exp_required[i]:
            return i
        if lvl > exp_required[len(exp_required) - 1]:
            if len(exp_required) == 50:
                return 50
            else:
                return 60
        if lvl == exp_required[i]:
            return i


def slayer(api, profile, uuid):
    """Find the player's slayer xp"""
    info = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api}&profile={profile}').json()
    exp = [10, 30, 250, 1500, 5000, 20_000, 100_000, 400_000, 1_000_000]
    slayer_type = ['wolf', 'spider', 'zombie']
    slayer_xp = []
    for i in slayer_type:
        slayer_xp.append(info['profile']['members'][uuid]['slayer_bosses'][i]['xp'])
    for i in range(len(slayer_xp)):
        print(f'{slayer_type[i]}: {slayer_lvl(slayer_xp[i], exp)}')


def slayer_lvl(slayer_xp, exp):
    """Calculate the player's slayer lvl"""
    for i in range(len(exp)):
        if slayer_xp < exp[i]:
            return i
        if slayer_xp > exp[len(exp) - 1]:
            return len(exp)
        if slayer_xp == exp[i]:
            return i


def dungeon(api, profile, uuid):
    """Find the player's catacomb's and classes' xp"""
    info = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api}&profile={profile}').json()
    experience = info['profile']['members'][uuid]['dungeons']['dungeon_types']['catacombs']['experience']
    print(f'Catacomb: {dungeonlvl(experience)}\n\nClasses:')

    classes_exp = []
    classes = ['healer', 'mage', 'berserk', 'archer', 'tank']
    class_names = ['Healer', 'Mage', 'Berserk', 'Archer', 'Tank']
    for i in classes:
        classes_exp.append(info['profile']['members'][uuid]['dungeons']['player_classes'][i]['experience'])
    for i in range(len(classes_exp)):
        print(f'{class_names[i]}: {dungeonlvl(classes_exp[i])}')

    print('\nDungeon Stats:')
    highest_floor_completed = info['profile']['members'][uuid]['dungeons']['dungeon_types']['catacombs'][
        'highest_tier_completed']
    if highest_floor_completed != 7:
        print("Hasn't complete floor 7 yet")
    if highest_floor_completed == 7:
        times_completed = info['profile']['members'][uuid]['dungeons']['dungeon_types']['catacombs'][
            'tier_completions']['7']
        print(f'Times beaten f7: {formatDecimal(times_completed)}')
        fastest = info['profile']['members'][uuid]['dungeons']['dungeon_types']['catacombs'][
            'fastest_time']['7']
        fastest /= 1000
        fastest /= 60
        print(f'Personal Best: {fastest}')
    info = requests.get(f'https://api.hypixel.net/player?key={api}&uuid={uuid}').json()
    secrets_found = info['player']['achievements']['skyblock_treasure_hunter']
    print(f'Secrets Found: {secrets_found}')


def dungeonlvl(experience):
    """Calculate the player's catacomb's and classes' lvl"""
    exp_required = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040,
                    70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640,
                    3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640,
                    51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640,
                    453559640, 569809640]
    for i in range(len(exp_required)):
        if experience < exp_required[i]:
            return i
        if experience > exp_required[len(exp_required) - 1]:
            return len(exp_required)
        if experience == exp_required[i]:
            return i


def stats(ign, profile, api):
    """Return the value of all of the aforementioned functions"""
    name = uuid(ign)
    profile__id = profile_id(ign, profile, api)
    print(f"{ign}'s stats:")
    skill(api, profile__id, name)
    print(f"\nSlayer:")
    slayer(api, profile__id, name)
    print('')
    dungeon(api, profile__id, name)


key = 'INSERT_YOUR_KEY_HERE'
profile_name = 'papaya'

stats('vndb', profile_name, key)
