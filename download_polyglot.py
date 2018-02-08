import os

from polyglot.downloader import downloader


def download():
    # downloader.download('sgns2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('unipos.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('ner2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('counts2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    downloader.download('embeddings2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('uniemb.en', os.path.join(os.getcwd(), 'polyglot_data'))
    downloader.download('pos2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('sentiment2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    # downloader.download('tsne2.en', os.path.join(os.getcwd(), 'polyglot_data'))
    downloader.download('morph2.en', os.path.join(os.getcwd(), 'polyglot_data'))


if __name__ == '__main__':
    os.path.sep = '/'
    download()
