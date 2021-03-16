import requests


def uuid(ign):
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    x = data["id"]
    return x


def profile_id(ign, profile, api):
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


def skill_lvl(skill, api, profile, uuid):
    info = requests.get('https://api.hypixel.net/resources/skyblock/skills').json()
    exp_required = []
    for i in info['collections'][f'{skill.upper()}']['levels']:
        exp_required.append(i['totalExpRequired'])

    levels = {}
    for i in range(len(exp_required)):
        levels[i + 1] = exp_required[i]

    a = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api}&profile={profile}').json()
    lvl = a['profile']['members'][f'{uuid}'][f'experience_skill_{skill.lower()}']
    for i in range(len(exp_required)):
        if lvl < exp_required[i]:
            current_lvl = i
            return current_lvl
        if lvl > exp_required[len(exp_required) - 1]:
            return len(exp_required)
        if lvl == exp_required[len(exp_required) - 1]:
            return len(exp_required)


def stats(ign, profile, api):
    print(f"farming: {skill_lvl('farming', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"mining: {skill_lvl('mining', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"combat: {skill_lvl('combat', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"alchemy: {skill_lvl('alchemy', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"foraging: {skill_lvl('foraging', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"fishing: {skill_lvl('fishing', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"enchanting: {skill_lvl('enchanting', api, profile_id(ign, profile, api), uuid(ign))}")
    print(f"taming: {skill_lvl('taming', api, profile_id(ign, profile, api), uuid(ign))}")


key = 'YOUR_API_KEY_HERE'
profile_name = 'papaya'

"""
Example:
stats('vndb', profile_name, key)
""""
