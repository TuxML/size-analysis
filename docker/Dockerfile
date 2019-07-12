FROM frolvlad/alpine-python3

RUN apk add --no-cache \
        --virtual=.build-dependencies \
        g++ gfortran file binutils \
        musl-dev python3-dev cython openblas-dev && \
    apk add libstdc++ openblas && \
    \
    ln -s locale.h /usr/include/xlocale.h && \
    \
    pip install numpy==1.14.3 && \
    pip install pandas && \
    pip install scipy && \
    pip install scikit-learn && \
    \
    rm -r /root/.cache && \
    find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' + && \
    find /usr/lib/python3.*/site-packages/ -name '*.so' -print -exec sh -c 'file "{}" | grep -q "not stripped" && strip -s "{}"' \; && \
    \
    rm /usr/include/xlocale.h && \
    \
    apk del .build-dependencies

# Add pycddlib and cvxopt with GLPK
RUN cd /tmp && \
    apk add --no-cache \
        --virtual=.build-dependencies \
        gcc make file binutils \
        musl-dev python3-dev cython gmp-dev suitesparse-dev openblas-dev && \
    apk add gmp suitesparse && \
    \
    pip install pycddlib && \
    \
    wget "ftp://ftp.gnu.org/gnu/glpk/glpk-4.65.tar.gz" && \
    tar xzf "glpk-4.65.tar.gz" && \
    cd "glpk-4.65" && \
    ./configure --disable-static && \
    make -j4 && \
    make install-strip && \
    CVXOPT_BLAS_LIB=openblas CVXOPT_LAPACK_LIB=openblas CVXOPT_BUILD_GLPK=1 pip install --global-option=build_ext --global-option="-I/usr/include/suitesparse" cvxopt && \
    \
    rm -r /root/.cache && \
    find /usr/lib/python3.*/site-packages/ -name '*.so' -print -exec sh -c 'file "{}" | grep -q "not stripped" && strip -s "{}"' \; && \
    \
    apk del .build-dependencies && \
    rm -rf /tmp/*

RUN apk add git
RUN apk --no-cache --update-cache add freetype-dev libpng-dev openblas-dev
RUN apk --no-cache --update-cache add build-base
RUN apk --no-cache --update-cache add python3-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install matplotlib seaborn Jinja2
RUN git clone https://github.com/TuxML/size-analysis
COPY all_size_withyes.pkl size-analysis/