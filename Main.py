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


def skill(api, profile, uuid):
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


def stats(ign, profile, api):
    name = uuid(ign)
    profile__id = profile_id(ign, profile, api)
    print(f"{ign}'s stats:")
    skill(api, profile__id, name)


key = 'Enter_your_key here'
profile_name = 'papaya'

stats('vndb', profile_name, key)
