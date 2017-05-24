

all: $(EXPKIT_TARGET)


.PHONY: open clean

clean:
	rm -rf $(EXPKIT_RESULT_DIR)

open: $(EXPKIT_TARGET)
	$(EXPKIT_OPEN_CMD) $<


$(RESULT_DIR)/experiments_done: $(EXPKIT_EXPERIMENTS_CFG)
	$(EXPKIT_PYTHON) $<
	touch $@

$(RESULT_DIR)/results_outputed: $(EXPKIT_RESULTS_CFG) $(EXPKIT_RESULT_DIR)/experiments_done
	$(EXPKIT_PYTHON) $<
	touch $@

%.pdf: $(EXPKIT_RESULT_DIR)/results_outputed
	cd $(EXPKIT_RESULT_DIR) && $(EXPKIT_LATEX) $(patsubst %.pdf,%.tex,$(notdir $@))
	rsync $(EXPKIT_RESULT_DIR)/$(notdir $@) $@
