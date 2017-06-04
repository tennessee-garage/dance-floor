platform=$(shell uname)

CFLAGS=-O2 -g
ALL=bin/dummy_client bin/dummy_server bin/gl_server
ifeq ($(platform),Darwin)
  GL_OPTS=-framework OpenGL -framework GLUT -Wno-deprecated-declarations
else ifeq ($(platform),Linux)
  GL_OPTS=-lGL -lglut -lGLU -lm
endif

all: $(ALL)

clean:
	rm -rf bin/*

bin/dummy_client: src/dummy_client.c src/opc_client.c
	mkdir -p bin
	gcc ${CFLAGS} -o $@ $^

bin/dummy_server: src/dummy_server.c src/opc_server.c
	mkdir -p bin
	gcc ${CFLAGS} -o $@ $^

bin/gl_server: src/gl_server.c src/opc_server.c src/cJSON.c
	mkdir -p bin
	gcc ${CFLAGS} -o $@ $^ $(GL_OPTS)
