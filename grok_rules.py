from py3grok import GrokEnvironment

###
# grok_env = GrokEnvironment()
# pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age} years old and weighs %{NUMBER:weight} kilograms.'
#
# # Regex flags can be used, like: grok_env.create(pattern, flags=re.IGNORECASE)
# grok = grok_env.create(pattern)
#
# text = 'Gary is male, 25 years old and weighs 68.5 kilograms.'
# print(grok.match(text))
#
# # {'gender': 'male', 'age': '25', 'name': 'Gary', 'weight': '68.5'}###

rules = [
    {"type": "falcon",
     "rule": '%{GREEDYDATA:timestamp} %{GREEDYDATA:source_file} src\:%{GREEDYDATA:src} dst\:%{GREEDYDATA:dst} %{GREEDYDATA:source_file}'},
    {"type": "nginx", "rule": ''}
]
