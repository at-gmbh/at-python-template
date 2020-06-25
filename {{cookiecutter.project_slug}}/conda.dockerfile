ARG PYTHON_IMAGE_TAG=4.8.2

FROM continuumio/miniconda3:${PYTHON_IMAGE_TAG}
WORKDIR /{{cookiecutter.module_name}}
COPY . . 

RUN conda config --set channel_priority strict && \
    conda env create -n {{cookiecutter.module_name}}_env -f environment.yml && \
    echo "source activate {{cookiecutter.module_name}}_env" > ~/.bashrc && \
    source activate {{cookiecutter.module_name}}_env && \
    python setup.py install

ENTRYPOINT ["python", "-OO", "-m", "{{ cookiecutter.module_name }}"]

##
## First stage: get dependencies, build the project, store binaries (whl)
##
#
#FROM continuumio/miniconda3:${PYTHON_IMAGE_TAG} as py-build
#WORKDIR /build
## install and store the requirements (this stage will be re-used unless requirements.txt changes)
#COPY requirements.txt .
#RUN pip install -r requirements.txt && pip wheel -r requirements.txt -w deps
## add all other source files, force rebuild only from here
#COPY . .
#RUN python setup.py install && python setup.py bdist_wheel
#
##
## Second stage: create the smallest possible image for deployment
##
#
#FROM python:${PYTHON_IMAGE_TAG}
#LABEL maintainer="Alexander Thamm GmbH"
#WORKDIR /app
## install all dependencies from wheel packages in the 'deps' folder
#COPY --from=py-build /build/deps/ deps/
#RUN [ -n "$(ls -A deps)" ] && pip install deps/*.whl && rm -rf deps || echo "no dependencies to install"
## install the application from a wheel package in the 'dist' folder
#COPY --from=py-build /build/dist/ dist/
#RUN pip install dist/*.whl && rm -rf dist
#ENTRYPOINT ["python", "-OO" , "-m", "{{ cookiecutter.module_name }}"]
