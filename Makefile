SHELL := /bin/bash

setup:

	@echo -e "\e[34m####### Setup for Garuda #######\e[0m"
	@[ -d config ] || mkdir config || exit 1
	@echo -n "{}" > config/settings.json
	@read -p "Instagram Username: " uservar; \
	read -sp "Instagram Password: " passvar; \
	echo -en "[Credentials]\nusername = $$uservar\npassword = $$passvar"  > config/credentials.ini || exit 1
	@echo ""
	@echo -e "\e[32mSetup Successful - config/credentials.ini created\e[0m"