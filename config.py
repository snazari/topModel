config_saving = {
    'dir_name': r'C:\Users\user\Documents\project\python_git_user_topic_modelling\data',
}

config_processing = {
    'delete_punctuation_marks': True,
    'delete_numeral': True,
    'delete_single_words': True,
    'initial_form': False,
    'stop_words': ['for', 'a', 'of', 'the', 'and', 'to', 'in']
}

config_models = \
    {
        'TfIdf': {
            'normalize': True
        },
        'LSI': {
            'num_topics': 5,
            'power_iters': 2,
            'extra_samples': 100
        },
        'RP': {
            'num_topics': 5
        },
        'LDA': {
            'num_topics': 5,
            'distributed': False,
            'alpha': 'symmetric',
            'eta': None
        },
        'HDP': {
            'gamma': 1,
            'kappa': 1.0,
            'tau': 64.0,
            'K': 15,
            'T': 150,
            'eta': 0.01,
            'num_topics': 5
        }
    }