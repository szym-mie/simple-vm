TARGET = svm

SRCP = src/
OBJP = obj/
OUTP = bin/

SRCS = $(wildcard $(SRCP)*.c)
OBJS = $(patsubst $(SRCP)%.c,$(OBJP)%.o,$(filter-out $(SRCP)$(TARGET).c,$(SRCS)))

CC = clang
CCF += -Wall
CCF += -std=c99
LBF = $(foreach LIB,$(LIBS),-l$(LIB))

.PHONY: all
all:
	@echo please select release/debug build
	@echo use \'make release\' or \'make debug\'

.PHONY: release
release: $(OUTP)$(TARGET)

.PHONY: debug
debug: XCCF += -g
debug: $(OUTP)$(TARGET)
	

$(OBJS): $(OBJP)%.o: $(SRCP)%.c
	@mkdir -p $(@D)
	$(CC) $(CCF) $(XCCF) -c -o $@ $<

$(OUTP)$(TARGET): $(OUTP)%: $(SRCP)%.c $(OBJS) $(LBF)
	@mkdir -p $(@D)
	$(CC) $(CCF) $(XCCF) -o $@ $^

.PHONY: install
install:
	cp $(OUTP)* /bin

.PHONY: clean
clean:
	rm -rf $(OBJP)*
	rm -rf $(OUTP)*

