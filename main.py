""" Requires installing the requests library: pip3 install requests """
import requests
import json
import interaction

base_url = "http://0.0.0.0:5000/"

def get_something(url_request):
    url = base_url + url_request
    response = requests.get(url)
    data = response.text
    return json.loads(data)


def get_ontology():
    return get_something('ontology/alreadyLoaded')


def get_dataset_list():
    return get_something('dataset/alreadyLoaded')


def post_request(url, data='', headers=None):
    if headers is None:
        headers = dict(accept='*application/json*')
    if data != '':
        headers['Content-Type'] = "application/json"
        r = requests.post(url, data, headers=headers)
    else:
        r = requests.post(url)
    return r.content.decode()


def post_ontology(type_of, path, name=''):
    url = base_url + 'ontology/' + type_of
    if name != '':
        url += '/' + name
    with open(path) as f:
        data = f.read()
    return post_request(url, data)


def post_dataset(datatype, path):
    url = base_url + 'dataset/' + datatype
    with open(path) as f:
        data = f.read()
    return post_request(url, data)


def team_formation_url(ont_id='', students_file='', proj_file='', pref_file=''):
    ''' Auxiliary function to build the URL properly, depending on what files are available. '''
    url = base_url + 'team_formation'
    if ont_id != '' and students_file != '' and proj_file != '':
        url += '/' + ont_id + '/' + students_file + '/' + proj_file
        if pref_file != '':
            url += '/' + pref_file
    return url


def call_with_loaded(preferences=True) -> object:
    ''' Asks the Docker container to execute the team formation algorithm using uploaded data.
    Note: I was not able to make it work properly when trying to upload different data than the one already
    present in the container. '''
    import os
    graphs = get_ontology()
    datasets = get_dataset_list()
    if not preferences:
        a = team_formation_url(os.path.splitext(graphs[1])[0],
                               os.path.splitext(datasets[2])[0],
                               os.path.splitext(datasets[17])[0])
    else:
        a = team_formation_url(os.path.splitext(graphs[1])[0],
                               os.path.splitext(datasets[2])[0],
                               os.path.splitext(datasets[17])[0],
                               os.path.splitext(datasets[4])[0])
    return post_request(a)


def generate_data(students_path, projects_path, preferences_path='', ontology_id='Precalc-ESCO-demo'):
    ''' Merges all information from JSON files into a string. Auxiliary function for call_uploading_data'''
    with open(students_path) as f:
        data_students = f.read()
    dict_a = json.loads(data_students)
    with open(projects_path) as f:
        projects_data = f.read()
    dict_b = json.loads(projects_data)
    if preferences_path != '':
        with open(preferences_path) as f:
            preferences_data = f.read()
        dict_c = json.loads(preferences_data)
        merged = {**dict_a, **dict_b, **dict_c}
    else:
        merged = {**dict_a, **dict_b, 'Preferences': {}}
    merged['OntologyID'] = ontology_id
    # string dump of the merged dict
    json_string_merged = json.dumps(merged)
    return json_string_merged


def call_uploading_data_paths(students_path, projects_path, preferences_path='', ontology_id='Precalc-ESCO-demo'):
    ''' Calls the Docker container taking data stored in given paths'''
    data = generate_data(students_path, projects_path, preferences_path, ontology_id)
    return json.loads(post_request(team_formation_url(), data))


def call_uploading_data(data):
    ''' Calls the Docker container using the provided data (as a Python dictionary)'''
    return json.loads(post_request(team_formation_url(), data))

def store_json(output_path, dic):
    with open(output_path, 'w') as outfile:
        outfile.write(json.dumps(dic, indent=4))
