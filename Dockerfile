FROM debian:8

MAINTAINER Kamil Kwiek <kamil.kwiek@continuum.io>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

RUN apt-get install -y icu-devtools libicu-dev libicu52 python3-icu gcc g++ make

RUN curl https://pypi.python.org/packages/bb/ef/3a7fcbba81bfd213e479131ae21445a2ddd14b46d70ef0109640b580bc5d/PyICU-2.0.3.tar.gz | tar zxvf -


RUN wget http://download.icu-project.org/files/icu4c/58.2/icu4c-58_2-src.tgz && tar -zxvf icu4c-58_2-src.tgz && \
    wget http://www.linuxfromscratch.org/patches/blfs/8.0/icu4c-58.2-fix_enumeration-1.patch

RUN cd icu && patch -p1 -i ../icu4c-58.2-fix_enumeration-1.patch && cd source && ./configure --prefix=/usr && make && \
    ./configure --prefix=/usr && make VERBOSE=1 all-local

# RUN cd PyICU-2.0.3 && python setup.py build

RUN apt-get install -y python-setuptools python-dev build-essential python-pip python-dev

RUN pip install pyicu

RUN pip install pycld2

ENV PATH /opt/conda/bin:$PATH

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
