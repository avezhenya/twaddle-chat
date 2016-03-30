.PHONY: deploy_dev

deploy_dev:
	ssh chat.dev "cd /home/itv-chat/; \
	              git pull origin v2; \
	              docker-compose stop; \
	              docker-compose rm; \
	              docker-compose build; \
	              docker-compose up -d;"
	@echo "Develop is done!"

deploy_prod:
	ssh chat.prod "cd /home/itv-chat/; \
	              git pull origin master; \
	              docker-compose stop; \
	              docker-compose rm; \
	              docker-compose build; \
	              docker-compose up -d;"
	@echo "Production is done!"